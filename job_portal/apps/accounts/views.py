from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.jobs.models import Application, Job, SavedJob

from .forms import LoginForm, ProfileForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("accounts:dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get("next") or "accounts:dashboard"
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("jobs:home")


@login_required
def dashboard_view(request):
    user = request.user
    context = {
        "applications": Application.objects.filter(applicant=user).select_related("job")[:10],
        "saved_jobs": SavedJob.objects.filter(user=user).select_related("job")[:10],
        "app_count": Application.objects.filter(applicant=user).count(),
        "pending_count": Application.objects.filter(applicant=user, status="pending").count(),
        "interview_count": Application.objects.filter(applicant=user, status="interview").count(),
        "saved_count": SavedJob.objects.filter(user=user).count(),
    }
    if user.is_employer:
        my_jobs = Job.objects.filter(posted_by=user)
        context["my_jobs"] = my_jobs
        context["active_listings"] = my_jobs.filter(status="active").count()
        context["total_applications"] = Application.objects.filter(job__posted_by=user).count()
    return render(request, "accounts/dashboard.html", context)


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
