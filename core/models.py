"""
core/models.py
===============
Database models for the AI Solutions platform.

Tables:
  - ContactInquiry    : Lead generation form submissions
  - Solution          : Software solution descriptions
  - CaseStudy         : Industry case studies
  - Testimonial       : Customer testimonials with star ratings
  - Article           : Knowledge Hub blog/news articles
  - GalleryImage      : Media gallery photos for events
  - ChatMessage       : Logged chatbot conversations (optional analytics)
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# ──────────────────────────────────────────────
# LEAD GENERATION
# ──────────────────────────────────────────────

class ContactInquiry(models.Model):
    """
    Captures every inbound lead from the public Contact Us form.
    No user account needed — collected anonymously.
    """
    # Personal & professional details
    name        = models.CharField(max_length=120, verbose_name="Full Name")
    email       = models.EmailField(verbose_name="Email Address")
    phone       = models.CharField(max_length=30, blank=True, verbose_name="Phone Number")
    company     = models.CharField(max_length=150, blank=True, verbose_name="Company / Organisation")
    country     = models.CharField(max_length=80, verbose_name="Country")
    job_title   = models.CharField(max_length=120, verbose_name="Job Title")
    job_details = models.TextField(verbose_name="How can we help?")

    # Internal tracking
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")
    is_read      = models.BooleanField(default=False, verbose_name="Marked as Read")

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return f"{self.name} ({self.company}) — {self.submitted_at:%d %b %Y}"


# ──────────────────────────────────────────────
# SOFTWARE SOLUTIONS
# ──────────────────────────────────────────────

class Solution(models.Model):
    """
    Describes each AI-powered software product/service offered.
    """
    ICON_CHOICES = [
        ('robot',        'Staff Help Desk'),
        ('chart',        '📊 Analytics'),
        ('shield',       '🛡️ Security'),
        ('workflow',     '⚙️ Workflow'),
        ('integration',  '🔗 Integration'),
        ('support',      '💬 Support'),
    ]

    title       = models.CharField(max_length=160)
    icon        = models.CharField(max_length=20, choices=ICON_CHOICES, default='robot')
    summary     = models.CharField(max_length=300, help_text="One-line pitch shown on cards")
    description = models.TextField(help_text="Full rich-text description")
    features    = models.TextField(
        help_text="Bullet points, one per line",
        blank=True
    )
    is_featured  = models.BooleanField(default=False, help_text="Show prominently on homepage")
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"

    def __str__(self):
        return self.title

    def feature_list(self):
        """Returns features as a Python list for template iteration."""
        return [f.strip() for f in self.features.splitlines() if f.strip()]


# ──────────────────────────────────────────────
# CASE STUDIES
# ──────────────────────────────────────────────

class CaseStudy(models.Model):
    """
    Showcases successful client deployments and measurable outcomes.
    """
    client_name  = models.CharField(max_length=160, verbose_name="Client / Organisation")
    industry     = models.CharField(max_length=100)
    challenge    = models.TextField(verbose_name="The Challenge")
    solution     = models.TextField(verbose_name="Our Solution")
    outcome      = models.TextField(verbose_name="Results & Impact")
    metric_label = models.CharField(max_length=60, blank=True,
                                    help_text="e.g. 'Reduction in handling time'")
    metric_value = models.CharField(max_length=20, blank=True,
                                    help_text="e.g. '42%'")
    logo         = models.ImageField(upload_to='case_studies/', blank=True, null=True)
    published_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Highlight"
        verbose_name_plural = "Highlights"

    def __str__(self):
        return f"{self.client_name} — {self.industry}"


# ──────────────────────────────────────────────
# TESTIMONIALS
# ──────────────────────────────────────────────

class Testimonial(models.Model):
    """
    Customer testimonials with a 1–5 star rating.
    """
    author_name    = models.CharField(max_length=120)
    author_title   = models.CharField(max_length=160, verbose_name="Job Title & Company",
                                      help_text="e.g. 'Head of IT, Acme Corp'")
    author_photo   = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote          = models.TextField()
    rating         = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Star Rating (1–5)"
    )
    is_approved    = models.BooleanField(default=True)
    submitted_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', '-submitted_at']
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.author_name} — {'★' * self.rating}"

    @property
    def star_range(self):
        """Used in templates: {% for s in testimonial.star_range %} ★ {% endfor %}"""
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)


# ──────────────────────────────────────────────
# KNOWLEDGE HUB (Blog / News)
# ──────────────────────────────────────────────

class Article(models.Model):
    """
    Promotional articles and news for the Knowledge Hub section.
    """
    CATEGORY_CHOICES = [
        ('news',        'Company News'),
        ('insight',     'Industry Insight'),
        ('tutorial',    'How-To Guide'),
        ('case-study',  'Case Study Spotlight'),
        ('event',       'Event Announcement'),
    ]

    title         = models.CharField(max_length=220)
    slug          = models.SlugField(max_length=240, unique=True)
    category      = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='insight')
    excerpt       = models.CharField(max_length=320, help_text="Short preview shown in card")
    body          = models.TextField(help_text="Full article content (HTML allowed)")
    cover_image   = models.ImageField(upload_to='articles/', blank=True, null=True)
    author        = models.CharField(max_length=120, default='AI Solutions Team')
    is_published  = models.BooleanField(default=True)
    published_at  = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    read_time_min = models.PositiveSmallIntegerField(default=5, verbose_name="Read time (minutes)")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'slug': self.slug})


# ──────────────────────────────────────────────
# MEDIA GALLERY
# ──────────────────────────────────────────────

class GalleryImage(models.Model):
    """
    Photos for past and upcoming promotional events.
    """
    EVENT_TYPE_CHOICES = [
        ('conference',  'Conference'),
        ('workshop',    'Workshop'),
        ('launch',      'Product Launch'),
        ('networking',  'Networking Event'),
        ('award',       'Award Ceremony'),
        ('other',       'Other'),
    ]

    title       = models.CharField(max_length=200)
    image       = models.ImageField(upload_to='gallery/')
    event_type  = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    event_date  = models.DateField(help_text="Date of the event")
    location    = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_upcoming = models.BooleanField(default=False, verbose_name="Is Upcoming Event?")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date']
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def __str__(self):
        return f"{self.title} ({self.event_date})"


# ──────────────────────────────────────────────
# CHATBOT CONVERSATION LOG (Analytics)
# ──────────────────────────────────────────────

class PromotionalEvent(models.Model):
    title = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=20,
        choices=GalleryImage.EVENT_TYPE_CHOICES,
        default='other',
    )
    event_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    registration_label = models.CharField(max_length=80, default='Register interest')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} ({self.event_date})"


class ChatMessage(models.Model):
    """
    Optional: logs each chatbot exchange for analytics and QA.
    Session-based — no personal data stored by default.
    """
    session_id  = models.CharField(max_length=64, db_index=True)
    user_msg    = models.TextField(verbose_name="User Message")
    bot_reply   = models.TextField(verbose_name="Bot Reply")
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Chat Message"

    def __str__(self):
        return f"[{self.timestamp:%d %b %H:%M}] {self.user_msg[:60]}"
