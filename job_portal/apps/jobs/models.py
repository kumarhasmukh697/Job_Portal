from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "full-time", "Full-time"
        PART_TIME = "part-time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    company = models.CharField(max_length=150)
    company_logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    location = models.CharField(max_length=120)
    is_remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs"
    )
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated skills")
    apply_email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.title}-{self.company}")
            slug = base
            counter = 1
            while Job.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_absolute_url(self):
        return reverse("jobs:job_detail", kwargs={"slug": self.slug})

    @property
    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,} – ${self.salary_max:,}"
        if self.salary_min:
            return f"From ${self.salary_min:,}"
        if self.salary_max:
            return f"Up to ${self.salary_max:,}"
        return "Not specified"

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @property
    def company_initials(self):
        parts = self.company.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        return self.company[:2].upper()


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        INTERVIEW = "interview", "Interview"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to="application_resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("job", "applicant")]

    def __str__(self):
        return f"{self.full_name} → {self.job.title}"


class SavedJob(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_jobs"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "job")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} saved {self.job}"
