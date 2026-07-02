"""
core/admin.py
==============
Django admin configuration for AI-Solution models.
All models are registered with customised list displays, filters, and search.
"""

from django.contrib import admin
from .models import (
    ContactInquiry, Solution, CaseStudy,
    Testimonial, Article, GalleryImage, PromotionalEvent, ChatMessage
)

admin.site.site_header = "AI Solutions CRM"
admin.site.site_title = "AI Solutions CRM"
admin.site.index_title = "Content and Queries"


# ── Contact Inquiries ─────────────────────────

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'company', 'country', 'job_title', 'submitted_at', 'is_read')
    list_filter   = ('is_read', 'country', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'company', 'country', 'job_title', 'job_details')
    readonly_fields = ('submitted_at',)
    ordering      = ('-submitted_at',)
    list_editable = ('is_read',)


# ── Solutions ─────────────────────────────────

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_featured', 'display_order')
    list_editable = ('is_featured', 'display_order')
    search_fields = ('title', 'summary', 'description')


# ── Case Studies ──────────────────────────────

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display  = ('client_name', 'industry', 'metric_value', 'metric_label', 'is_published', 'published_at')
    list_filter   = ('industry', 'is_published')
    search_fields = ('client_name', 'industry', 'challenge', 'solution', 'outcome')
    list_editable = ('is_published',)


# ── Testimonials ──────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('author_name', 'author_title', 'rating', 'is_approved', 'submitted_at')
    list_filter   = ('rating', 'is_approved')
    list_editable = ('rating', 'is_approved')
    search_fields = ('author_name', 'author_title', 'quote')


# ── Articles ──────────────────────────────────

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display   = ('title', 'category', 'author', 'is_published', 'published_at')
    list_filter    = ('category', 'is_published')
    search_fields  = ('title', 'excerpt', 'body', 'author')
    prepopulated_fields = {'slug': ('title',)}
    list_editable  = ('is_published',)
    readonly_fields = ('published_at', 'updated_at')
    exclude = ('cover_image',)


# ── Gallery ───────────────────────────────────

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'event_type', 'event_date', 'location', 'is_upcoming')
    list_filter   = ('event_type', 'is_upcoming', 'event_date')
    search_fields = ('title', 'location', 'description')
    list_editable = ('is_upcoming',)


@admin.register(PromotionalEvent)
class PromotionalEventAdmin(admin.ModelAdmin):
    list_display  = ('title', 'event_type', 'event_date', 'location', 'is_published')
    list_filter   = ('event_type', 'is_published', 'event_date')
    search_fields = ('title', 'location', 'description')
    list_editable = ('is_published',)


# ── Chat Messages ─────────────────────────────

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ('session_id', 'user_msg', 'timestamp')
    search_fields = ('user_msg', 'bot_reply', 'session_id')
    readonly_fields = ('session_id', 'user_msg', 'bot_reply', 'timestamp')
