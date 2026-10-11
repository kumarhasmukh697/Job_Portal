from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with role support."""

    class Role(models.TextChoices):
        SEEKER = "seeker", "Job Seeker"
        EMPLOYER = "employer", "Employer"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SEEKER,
    )
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_seeker(self):
        return self.role == self.Role.SEEKER

    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER
