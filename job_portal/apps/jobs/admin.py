from django.contrib import admin

from .models import Application, Category, Job, SavedJob


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "status", "posted_by", "created_at")
    list_filter = ("status", "job_type", "is_remote", "category")
    search_fields = ("title", "company", "description", "tags")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("posted_by",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "email")
    raw_id_fields = ("job", "applicant")


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at")
    raw_id_fields = ("user", "job")
