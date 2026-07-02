"""
Forms for public contact capture, staff login, and staff CRM editing.
"""

from django import forms
from django.utils.text import slugify

from .models import (
    Article, CaseStudy, ContactInquiry, GalleryImage,
    PromotionalEvent, Solution, Testimonial,
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'company', 'country', 'job_title', 'job_details']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'you@organisation.co.uk',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+44 191 000 0000',
                'autocomplete': 'tel',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Organisation name',
                'autocomplete': 'organization',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'United Kingdom',
                'autocomplete': 'country-name',
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your role',
            }),
            'job_details': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Briefly describe your project or requirements...',
                'rows': 5,
            }),
        }
        labels = {
            'name': 'Full Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number',
            'company': 'Company / Organisation',
            'country': 'Country *',
            'job_title': 'Job Title *',
            'job_details': 'How Can We Help? *',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and len(phone) < 7:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class StaffLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        }),
    )


class StaffModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-checkbox')
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault('class', 'form-input form-textarea')
                widget.attrs.setdefault('rows', 5)
            else:
                widget.attrs.setdefault('class', 'form-input')


class SolutionForm(StaffModelForm):
    class Meta:
        model = Solution
        fields = [
            'title', 'icon', 'summary', 'description', 'features',
            'is_featured', 'display_order',
        ]


class CaseStudyForm(StaffModelForm):
    class Meta:
        model = CaseStudy
        fields = [
            'client_name', 'industry', 'challenge', 'solution', 'outcome',
            'metric_label', 'metric_value', 'logo', 'is_published',
        ]


class TestimonialForm(StaffModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'author_name', 'author_title', 'author_photo', 'quote',
            'rating', 'is_approved',
        ]


class ArticleForm(StaffModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'category', 'excerpt', 'body', 'cover_image',
            'author', 'is_published', 'read_time_min',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = "Leave blank to generate this from the title."

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        title = self.cleaned_data.get('title', '').strip()
        return slugify(slug or title)

    def save(self, commit=True):
        instance = super().save(commit=False)
        base_slug = instance.slug or slugify(instance.title)
        slug = base_slug
        counter = 2
        queryset = Article.objects.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class GalleryImageForm(StaffModelForm):
    class Meta:
        model = GalleryImage
        fields = [
            'title', 'image', 'event_type', 'event_date', 'location',
            'description', 'is_upcoming',
        ]
        widgets = {
            'event_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class PromotionalEventForm(StaffModelForm):
    class Meta:
        model = PromotionalEvent
        fields = [
            'title', 'event_type', 'event_date', 'location', 'description',
            'is_published', 'registration_label',
        ]
        widgets = {
            'event_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
