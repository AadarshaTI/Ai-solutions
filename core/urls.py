"""
core/urls.py
=============
URL routing for the AI-Solution core application.

Public routes  → no authentication required
Staff routes   → @login_required enforced in views.py
API route      → AJAX only (POST + CSRF)
"""

from django.urls import path
from . import views

urlpatterns = [

    # ── Public Pages ──────────────────────────
    path('',                    views.home,          name='home'),
    path('solutions/',          views.solutions,     name='solutions'),
    path('case-studies/',       views.case_studies,  name='case_studies'),
    path('feedback/',           views.feedback,      name='feedback'),
    path('knowledge-hub/',      views.knowledge_hub, name='knowledge_hub'),
    path('knowledge-hub/<slug:slug>/', views.article_detail, name='article_detail'),
    path('gallery/',            views.gallery,       name='gallery'),
    path('contact/',            views.contact,       name='contact'),

    # ── AI Chatbot API (AJAX) ─────────────────
    path('api/chat/',           views.chatbot_api,   name='chatbot_api'),

    # ── Staff Dashboard ───────────────────────
    path('staff/login/',        views.staff_login,   name='staff_login'),
    path('staff/logout/',       views.staff_logout,  name='staff_logout'),
    path('staff/dashboard/',    views.dashboard,     name='dashboard'),
    path('staff/solutions/', views.staff_solutions, name='staff_solutions'),
    path('staff/solutions/create/', views.staff_solution_create, name='staff_solution_create'),
    path('staff/solutions/<int:pk>/edit/', views.staff_solution_edit, name='staff_solution_edit'),
    path('staff/solutions/<int:pk>/delete/', views.staff_solution_delete, name='staff_solution_delete'),
    path('staff/highlights/', views.staff_highlights, name='staff_highlights'),
    path('staff/highlights/create/', views.staff_highlight_create, name='staff_highlight_create'),
    path('staff/highlights/<int:pk>/edit/', views.staff_highlight_edit, name='staff_highlight_edit'),
    path('staff/highlights/<int:pk>/delete/', views.staff_highlight_delete, name='staff_highlight_delete'),
    path('staff/feedback/', views.staff_feedback, name='staff_feedback'),
    path('staff/feedback/create/', views.staff_feedback_create, name='staff_feedback_create'),
    path('staff/feedback/<int:pk>/edit/', views.staff_feedback_edit, name='staff_feedback_edit'),
    path('staff/feedback/<int:pk>/delete/', views.staff_feedback_delete, name='staff_feedback_delete'),
    path('staff/articles/', views.staff_articles, name='staff_articles'),
    path('staff/articles/create/', views.staff_article_create, name='staff_article_create'),
    path('staff/articles/<int:pk>/edit/', views.staff_article_edit, name='staff_article_edit'),
    path('staff/articles/<int:pk>/delete/', views.staff_article_delete, name='staff_article_delete'),
    path('staff/photos/', views.staff_photos, name='staff_photos'),
    path('staff/photos/create/', views.staff_photo_create, name='staff_photo_create'),
    path('staff/photos/<int:pk>/edit/', views.staff_photo_edit, name='staff_photo_edit'),
    path('staff/photos/<int:pk>/delete/', views.staff_photo_delete, name='staff_photo_delete'),
    path('staff/events/', views.staff_events, name='staff_events'),
    path('staff/events/create/', views.staff_event_create, name='staff_event_create'),
    path('staff/events/<int:pk>/edit/', views.staff_event_edit, name='staff_event_edit'),
    path('staff/events/<int:pk>/delete/', views.staff_event_delete, name='staff_event_delete'),
    path('staff/queries/', views.staff_queries, name='staff_queries'),
    path('staff/queries/<int:pk>/', views.staff_query_detail, name='staff_query_detail'),
    path('staff/queries/<int:pk>/mark-read/', views.staff_query_mark_read, name='staff_query_mark_read'),
    path('staff/queries/<int:pk>/mark-unread/', views.staff_query_mark_unread, name='staff_query_mark_unread'),
    path('staff/queries/<int:pk>/delete/', views.staff_query_delete, name='staff_query_delete'),
]
