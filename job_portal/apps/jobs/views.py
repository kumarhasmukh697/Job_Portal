from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, JobForm, JobSearchForm
from .models import Application, Category, Job, SavedJob


def home_view(request):
    featured = Job.objects.filter(status=Job.Status.ACTIVE).select_related("category")[:6]
    categories = Category.objects.all()
    return render(request, "jobs/home.html", {"featured_jobs": featured, "categories": categories})


def job_list_view(request):
    qs = Job.objects.filter(status=Job.Status.ACTIVE).select_related("category", "posted_by")

    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    category_slug = request.GET.get("category", "").strip()
    job_type = request.GET.get("type", "").strip()
    # support multi checkbox from template
    locations = request.GET.getlist("location")
    categories = request.GET.getlist("category")
    types = request.GET.getlist("type")

    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(company__icontains=q)
            | Q(description__icontains=q)
            | Q(tags__icontains=q)
        )
    if locations:
        loc_q = Q()
        for loc in locations:
            if loc.lower() == "remote":
                loc_q |= Q(is_remote=True)
            else:
                loc_q |= Q(location__icontains=loc)
        qs = qs.filter(loc_q)
    elif location:
        if location.lower() == "remote":
            qs = qs.filter(is_remote=True)
        else:
            qs = qs.filter(location__icontains=location)

    if categories:
        qs = qs.filter(category__slug__in=categories)
    elif category_slug:
        qs = qs.filter(category__slug=category_slug)

    if types:
        qs = qs.filter(job_type__in=types)
    elif job_type:
        qs = qs.filter(job_type=job_type)

    paginator = Paginator(qs, 10)
    page = request.GET.get("page")
    jobs = paginator.get_page(page)

    context = {
        "jobs": jobs,
        "categories": Category.objects.all(),
        "total_count": qs.count(),
        "search_form": JobSearchForm(request.GET or None),
    }
    return render(request, "jobs/job_list.html", context)


def job_detail_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    form = ApplicationForm()
    if request.user.is_authenticated and request.user.get_full_name():
        form = ApplicationForm(
            initial={
                "full_name": request.user.get_full_name(),
                "email": request.user.email,
                "phone": request.user.phone,
            }
        )

    if request.method == "POST" and request.user.is_authenticated:
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            if already_applied:
                messages.warning(request, "You have already applied to this job.")
            else:
                app = form.save(commit=False)
                app.job = job
                app.applicant = request.user
                app.save()
                messages.success(request, "Application submitted successfully!")
                return redirect(job.get_absolute_url())
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        "job": job,
        "form": form,
        "already_applied": already_applied,
    }
    return render(request, "jobs/job_detail.html", context)


@login_required
def job_post_view(request):
    if not (request.user.is_employer or request.user.is_staff):
        messages.error(request, "Only employers can post jobs. Update your role in profile or register as employer.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("jobs:my_jobs")
    else:
        form = JobForm(initial={"status": Job.Status.ACTIVE})
    return render(request, "jobs/job_post.html", {"form": form})


@login_required
def job_edit_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if job.posted_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this job.")
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect("jobs:my_jobs")
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/job_post.html", {"form": form, "editing": True, "job": job})


@login_required
def job_delete_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if job.posted_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this job.")
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job listing deleted.")
        return redirect("jobs:my_jobs")
    return redirect("jobs:my_jobs")


@login_required
def my_jobs_view(request):
    jobs = Job.objects.filter(posted_by=request.user).prefetch_related("applications")
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def applications_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if job.posted_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot view these applications.")
    apps = job.applications.select_related("applicant").all()
    return render(request, "jobs/applications.html", {"job": job, "applications": apps})


@login_required
def update_application_status(request, pk, status):
    app = get_object_or_404(Application, pk=pk)
    if app.job.posted_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    if status in dict(Application.Status.choices):
        app.status = status
        app.save(update_fields=["status", "updated_at"])
        messages.success(request, f"Application marked as {app.get_status_display()}.")
    return redirect("jobs:applications", slug=app.job.slug)


@login_required
def save_job_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    SavedJob.objects.get_or_create(user=request.user, job=job)
    messages.success(request, "Job saved.")
    return redirect(job.get_absolute_url())
