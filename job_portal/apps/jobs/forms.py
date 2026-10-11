from django import forms

from .models import Application, Job, Category


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "location",
            "is_remote",
            "job_type",
            "category",
            "salary_min",
            "salary_max",
            "description",
            "requirements",
            "benefits",
            "tags",
            "apply_email",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "e.g. Senior Frontend Engineer"}),
            "company": forms.TextInput(attrs={"class": "input", "placeholder": "Acme Corp"}),
            "location": forms.TextInput(attrs={"class": "input", "placeholder": "Remote / City"}),
            "is_remote": forms.CheckboxInput(),
            "job_type": forms.Select(attrs={"class": "select"}),
            "category": forms.Select(attrs={"class": "select"}),
            "salary_min": forms.NumberInput(attrs={"class": "input", "placeholder": "80000"}),
            "salary_max": forms.NumberInput(attrs={"class": "input", "placeholder": "120000"}),
            "description": forms.Textarea(attrs={"class": "textarea", "rows": 8}),
            "requirements": forms.Textarea(attrs={"class": "textarea", "rows": 4}),
            "benefits": forms.Textarea(attrs={"class": "textarea", "rows": 3}),
            "tags": forms.TextInput(attrs={"class": "input", "placeholder": "React, TypeScript, Figma"}),
            "apply_email": forms.EmailInput(attrs={"class": "input", "placeholder": "careers@company.com"}),
            "status": forms.Select(attrs={"class": "select"}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["full_name", "email", "phone", "resume", "cover_letter"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "Jane Doe"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "jane@example.com"}),
            "phone": forms.TextInput(attrs={"class": "input", "placeholder": "+1 555 000 0000"}),
            "resume": forms.ClearableFileInput(attrs={"class": "input"}),
            "cover_letter": forms.Textarea(attrs={"class": "textarea", "rows": 4, "placeholder": "Why are you a great fit?"}),
        }


class JobSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Job title or keyword"}),
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Location"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories",
        widget=forms.Select(attrs={"class": "select"}),
    )
    job_type = forms.ChoiceField(
        choices=[("", "All types")] + list(Job.JobType.choices),
        required=False,
        widget=forms.Select(attrs={"class": "select"}),
    )
