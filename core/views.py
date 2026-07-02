"""
core/views.py
==============
View functions for all public pages and the staff dashboard.

Public Views:
  - home           : Landing page with hero, solutions, testimonials
  - solutions      : Full solutions listing
  - case_studies   : Industry case study grid
  - knowledge_hub  : Articles / news listing
  - article_detail : Single article reader
  - gallery        : Media gallery (past + upcoming events)
  - contact        : Lead-generation form (GET + POST)
  - chatbot_api    : AJAX endpoint for AI chatbot responses

Staff Views (login required):
  - staff_login    : Password login page
  - staff_logout   : Session termination
  - dashboard      : KPI dashboard — inquiry count + recent leads
"""

import json
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from .models import (
    Solution, CaseStudy, Testimonial,
    Article, GalleryImage, PromotionalEvent, ContactInquiry, ChatMessage
)
from .forms import (
    ArticleForm, CaseStudyForm, ContactForm, GalleryImageForm,
    PromotionalEventForm, SolutionForm, StaffLoginForm, TestimonialForm
)
from .chatbot import get_bot_reply   # AI chatbot logic module


# ══════════════════════════════════════════════
# PUBLIC VIEWS
# ══════════════════════════════════════════════

def home(request):
    """
    Homepage: hero section + featured solutions + latest testimonials + CTA.
    """
    context = {
        'featured_solutions': Solution.objects.filter(is_featured=True)[:6],
        'testimonials':       Testimonial.objects.filter(is_approved=True)[:6],
        'latest_articles':    Article.objects.filter(is_published=True)[:3],
        'stats': {
            'clients':    '4',
            'uptime':     '1 day',
            'savings':    '7 days',
            'nps':        'UK',
        }
    }
    return render(request, 'core/home.html', context)


def solutions(request):
    """
    Full catalogue of AI-powered software solutions.
    """
    all_solutions = Solution.objects.all()
    return render(request, 'core/solutions.html', {'solutions': all_solutions})


def case_studies(request):
    """
    Grid of published industry case studies.
    """
    studies = CaseStudy.objects.filter(is_published=True)
    return render(request, 'core/case_studies.html', {'case_studies': studies})


def feedback(request):
    """
    Public customer feedback page with approved ratings and testimonials.
    """
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'core/feedback.html', {'testimonials': testimonials})


def knowledge_hub(request):
    """
    Article / news listing with optional category filter.
    """
    category = request.GET.get('category', '')
    articles = Article.objects.filter(is_published=True)
    if category:
        articles = articles.filter(category=category)

    categories = Article.CATEGORY_CHOICES
    return render(request, 'core/knowledge_hub.html', {
        'articles':          articles,
        'categories':        categories,
        'active_category':   category,
    })


def article_detail(request, slug):
    """
    Full article reader view.
    """
    article  = get_object_or_404(Article, slug=slug, is_published=True)
    related  = Article.objects.filter(
        is_published=True, category=article.category
    ).exclude(pk=article.pk)[:3]
    return render(request, 'core/article_detail.html', {
        'article': article,
        'related': related,
    })


def gallery(request):
    """
    Media gallery split into past events and upcoming events.
    """
    today = timezone.localdate()
    upcoming_events = PromotionalEvent.objects.filter(
        is_published=True,
        event_date__gte=today,
    )
    past_images = GalleryImage.objects.filter(is_upcoming=False)
    upcoming_images = GalleryImage.objects.filter(is_upcoming=True)
    return render(request, 'core/gallery.html', {
        'upcoming_events': upcoming_events,
        'past_images': past_images,
        'upcoming_images': upcoming_images,
    })


def contact(request):
    """
    Lead-generation form.
    GET  → renders blank form
    POST → validates, saves inquiry, sends confirmation, redirects with message
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            # Optionally trigger email notification here
            messages.success(
                request,
                f"Thank you, {inquiry.name}! We'll be in touch within one business day."
            )
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


# ══════════════════════════════════════════════
# AI CHATBOT API ENDPOINT
# ══════════════════════════════════════════════

@require_POST
def chatbot_api(request):
    """
    AJAX endpoint consumed by the frontend chatbot widget.
    Accepts JSON: { "message": "...", "session_id": "..." }
    Returns JSON: { "reply": "..." }

    Conversation history is session-based; no personal data stored unless
    analytics logging is enabled below.
    """
    try:
        payload    = json.loads(request.body)
        user_msg   = payload.get('message', '').strip()
        session_id = payload.get('session_id') or str(uuid.uuid4())
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    if not user_msg:
        return JsonResponse({'error': 'Empty message'}, status=400)

    recent_messages = ChatMessage.objects.filter(
        session_id=session_id,
    ).order_by('-timestamp')[:6]
    conversation_history = [
        {'user': message.user_msg, 'bot': message.bot_reply}
        for message in reversed(recent_messages)
    ]

    # Generate response from chatbot module
    bot_reply = get_bot_reply(user_msg, conversation_history=conversation_history)

    # ── Optional analytics logging ──────────────
    ChatMessage.objects.create(
        session_id=session_id,
        user_msg=user_msg,
        bot_reply=bot_reply,
    )
    # ────────────────────────────────────────────

    return JsonResponse({'reply': bot_reply, 'session_id': session_id})


# ══════════════════════════════════════════════
# STAFF DASHBOARD VIEWS
# ══════════════════════════════════════════════

def staff_login(request):
    """
    Renders and processes the staff login form.
    On success → redirect to dashboard.
    On failure → re-render with error message.
    """
    # Already logged in? Staff go straight to dashboard; everyone else returns public.
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        messages.error(request, "Staff access is required.")
        return redirect('home')

    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials or insufficient permissions.")
    else:
        form = StaffLoginForm()

    return render(request, 'core/staff_login.html', {'form': form})


def staff_logout(request):
    """Terminates the authenticated session and returns to staff login."""
    logout(request)
    return redirect('staff_login')


staff_required = user_passes_test(
    lambda user: user.is_active and (user.is_staff or user.is_superuser),
    login_url='staff_login',
)


STAFF_CRM = {
    'solutions': {
        'model': Solution,
        'form': SolutionForm,
        'title': 'Solutions',
        'singular': 'Solution',
        'description': 'Manage the software solutions shown on the public Solutions page.',
        'list_url': 'staff_solutions',
        'create_url': 'staff_solution_create',
        'edit_url': 'staff_solution_edit',
        'delete_url': 'staff_solution_delete',
        'columns': ['Title', 'Featured', 'Order'],
    },
    'highlights': {
        'model': CaseStudy,
        'form': CaseStudyForm,
        'title': 'Highlights',
        'singular': 'Highlight',
        'description': 'Manage public industry highlights and case-study results.',
        'list_url': 'staff_highlights',
        'create_url': 'staff_highlight_create',
        'edit_url': 'staff_highlight_edit',
        'delete_url': 'staff_highlight_delete',
        'columns': ['Client', 'Industry', 'Published', 'Date'],
    },
    'feedback': {
        'model': Testimonial,
        'form': TestimonialForm,
        'title': 'Feedback',
        'singular': 'Feedback',
        'description': 'Manage customer feedback, ratings and approval status.',
        'list_url': 'staff_feedback',
        'create_url': 'staff_feedback_create',
        'edit_url': 'staff_feedback_edit',
        'delete_url': 'staff_feedback_delete',
        'columns': ['Author', 'Rating', 'Approved', 'Submitted'],
    },
    'articles': {
        'model': Article,
        'form': ArticleForm,
        'title': 'Articles',
        'singular': 'Article',
        'description': 'Manage company articles shown in the public Articles section.',
        'list_url': 'staff_articles',
        'create_url': 'staff_article_create',
        'edit_url': 'staff_article_edit',
        'delete_url': 'staff_article_delete',
        'columns': ['Title', 'Category', 'Published', 'Date'],
    },
    'photos': {
        'model': GalleryImage,
        'form': GalleryImageForm,
        'title': 'Photos',
        'singular': 'Photo',
        'description': 'Manage promotional event photos shown in the public gallery.',
        'list_url': 'staff_photos',
        'create_url': 'staff_photo_create',
        'edit_url': 'staff_photo_edit',
        'delete_url': 'staff_photo_delete',
        'columns': ['Title', 'Type', 'Date', 'Location'],
    },
    'events': {
        'model': PromotionalEvent,
        'form': PromotionalEventForm,
        'title': 'Events',
        'singular': 'Event',
        'description': 'Manage upcoming promotional events shown on the public Events page.',
        'list_url': 'staff_events',
        'create_url': 'staff_event_create',
        'edit_url': 'staff_event_edit',
        'delete_url': 'staff_event_delete',
        'columns': ['Title', 'Type', 'Date', 'Location', 'Published'],
    },
}


def staff_base_context(active='dashboard'):
    return {'active_staff_nav': active}


def crm_row(section, obj):
    if section == 'solutions':
        return [obj.title, 'Featured' if obj.is_featured else 'Standard', obj.display_order]
    if section == 'highlights':
        return [obj.client_name, obj.industry, 'Published' if obj.is_published else 'Draft', obj.published_at]
    if section == 'feedback':
        return [obj.author_name, obj.rating, 'Approved' if obj.is_approved else 'Pending', obj.submitted_at]
    if section == 'articles':
        return [obj.title, obj.get_category_display(), 'Published' if obj.is_published else 'Draft', obj.published_at]
    if section == 'photos':
        return [obj.title, obj.get_event_type_display(), obj.event_date, obj.location or '-']
    if section == 'events':
        return [obj.title, obj.get_event_type_display(), obj.event_date, obj.location or '-', 'Published' if obj.is_published else 'Draft']
    return [str(obj)]


def staff_crm_list(request, section):
    config = STAFF_CRM[section]
    objects = config['model'].objects.all()
    rows = [{'object': obj, 'cells': crm_row(section, obj)} for obj in objects]
    context = {
        **staff_base_context(section),
        **config,
        'rows': rows,
    }
    return render(request, 'core/staff/object_list.html', context)


def staff_crm_form(request, section, pk=None):
    config = STAFF_CRM[section]
    instance = get_object_or_404(config['model'], pk=pk) if pk else None
    if request.method == 'POST':
        form = config['form'](request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"{config['singular']} saved.")
            return redirect(config['list_url'])
        messages.error(request, "Please correct the errors below.")
    else:
        form = config['form'](instance=instance)

    context = {
        **staff_base_context(section),
        **config,
        'form': form,
        'object': instance,
        'form_title': f"{'Edit' if instance else 'Add'} {config['singular']}",
        'submit_label': 'Save changes' if instance else 'Create',
    }
    return render(request, 'core/staff/object_form.html', context)


def staff_crm_delete(request, section, pk):
    config = STAFF_CRM[section]
    obj = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{config['singular']} deleted.")
        return redirect(config['list_url'])
    context = {
        **staff_base_context(section),
        **config,
        'object': obj,
    }
    return render(request, 'core/staff/object_confirm_delete.html', context)


@staff_required
def dashboard(request):
    """
    Staff-only KPI dashboard.
    Displays total inquiry count, unread count, and recent submissions.
    Only accessible to authenticated staff members.
    """
    # Guard: only staff-flagged accounts can access
    if not request.user.is_staff:
        return redirect('home')

    total_inquiries  = ContactInquiry.objects.count()
    unread_inquiries = ContactInquiry.objects.filter(is_read=False).count()
    recent_inquiries = ContactInquiry.objects.order_by('-submitted_at')[:20]

    # Daily inquiry counts for the last 7 days (for a mini chart)
    from django.db.models import Count
    from django.utils.timezone import now
    from datetime import timedelta

    today  = now().date()
    week   = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_counts = {
        row['submitted_at__date']: row['count']
        for row in ContactInquiry.objects.filter(
            submitted_at__date__gte=week[0]
        ).values('submitted_at__date').annotate(count=Count('id'))
    }
    chart_data = [daily_counts.get(d, 0) for d in week]
    chart_labels = [d.strftime('%a') for d in week]

    # Mark selected inquiry as read via POST
    if request.method == 'POST' and 'mark_read' in request.POST:
        inquiry_id = request.POST.get('mark_read')
        ContactInquiry.objects.filter(pk=inquiry_id).update(is_read=True)
        return redirect('dashboard')

    context = {
        **staff_base_context('dashboard'),
        'total_inquiries':  total_inquiries,
        'unread_inquiries': unread_inquiries,
        'recent_inquiries': recent_inquiries,
        'chart_data':       json.dumps(chart_data),
        'chart_labels':     json.dumps(chart_labels),
        'software_solutions_count': Solution.objects.count(),
        'published_industry_highlights_count': CaseStudy.objects.filter(is_published=True).count(),
        'approved_customer_feedback_count': Testimonial.objects.filter(is_approved=True).count(),
        'published_company_articles_count': Article.objects.filter(is_published=True).count(),
        'event_gallery_photos_count': GalleryImage.objects.count(),
        'upcoming_events_count': PromotionalEvent.objects.filter(
            is_published=True,
            event_date__gte=today,
        ).count(),
        'chatbot_messages_count': ChatMessage.objects.count(),
    }
    return render(request, 'core/staff/dashboard.html', context)


@staff_required
def staff_solutions(request):
    return staff_crm_list(request, 'solutions')


@staff_required
def staff_solution_create(request):
    return staff_crm_form(request, 'solutions')


@staff_required
def staff_solution_edit(request, pk):
    return staff_crm_form(request, 'solutions', pk)


@staff_required
def staff_solution_delete(request, pk):
    return staff_crm_delete(request, 'solutions', pk)


@staff_required
def staff_highlights(request):
    return staff_crm_list(request, 'highlights')


@staff_required
def staff_highlight_create(request):
    return staff_crm_form(request, 'highlights')


@staff_required
def staff_highlight_edit(request, pk):
    return staff_crm_form(request, 'highlights', pk)


@staff_required
def staff_highlight_delete(request, pk):
    return staff_crm_delete(request, 'highlights', pk)


@staff_required
def staff_feedback(request):
    return staff_crm_list(request, 'feedback')


@staff_required
def staff_feedback_create(request):
    return staff_crm_form(request, 'feedback')


@staff_required
def staff_feedback_edit(request, pk):
    return staff_crm_form(request, 'feedback', pk)


@staff_required
def staff_feedback_delete(request, pk):
    return staff_crm_delete(request, 'feedback', pk)


@staff_required
def staff_articles(request):
    return staff_crm_list(request, 'articles')


@staff_required
def staff_article_create(request):
    return staff_crm_form(request, 'articles')


@staff_required
def staff_article_edit(request, pk):
    return staff_crm_form(request, 'articles', pk)


@staff_required
def staff_article_delete(request, pk):
    return staff_crm_delete(request, 'articles', pk)


@staff_required
def staff_photos(request):
    return staff_crm_list(request, 'photos')


@staff_required
def staff_photo_create(request):
    return staff_crm_form(request, 'photos')


@staff_required
def staff_photo_edit(request, pk):
    return staff_crm_form(request, 'photos', pk)


@staff_required
def staff_photo_delete(request, pk):
    return staff_crm_delete(request, 'photos', pk)


@staff_required
def staff_events(request):
    return staff_crm_list(request, 'events')


@staff_required
def staff_event_create(request):
    return staff_crm_form(request, 'events')


@staff_required
def staff_event_edit(request, pk):
    return staff_crm_form(request, 'events', pk)


@staff_required
def staff_event_delete(request, pk):
    return staff_crm_delete(request, 'events', pk)


@staff_required
def staff_queries(request):
    queries = ContactInquiry.objects.order_by('-submitted_at')
    return render(request, 'core/staff/query_list.html', {
        **staff_base_context('queries'),
        'queries': queries,
    })


@staff_required
def staff_query_detail(request, pk):
    query = get_object_or_404(ContactInquiry, pk=pk)
    return render(request, 'core/staff/query_detail.html', {
        **staff_base_context('queries'),
        'query': query,
    })


@staff_required
@require_POST
def staff_query_mark_read(request, pk):
    ContactInquiry.objects.filter(pk=pk).update(is_read=True)
    messages.success(request, "Query marked as read.")
    return redirect('staff_query_detail', pk=pk)


@staff_required
@require_POST
def staff_query_mark_unread(request, pk):
    ContactInquiry.objects.filter(pk=pk).update(is_read=False)
    messages.success(request, "Query marked as unread.")
    return redirect('staff_query_detail', pk=pk)


@staff_required
def staff_query_delete(request, pk):
    query = get_object_or_404(ContactInquiry, pk=pk)
    if request.method == 'POST':
        query.delete()
        messages.success(request, "Query deleted.")
        return redirect('staff_queries')
    return render(request, 'core/staff/query_confirm_delete.html', {
        **staff_base_context('queries'),
        'query': query,
    })
