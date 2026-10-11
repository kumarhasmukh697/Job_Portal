from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("jobs/", views.job_list_view, name="job_list"),
    path("jobs/post/", views.job_post_view, name="job_post"),
    path("jobs/my/", views.my_jobs_view, name="my_jobs"),
    path("jobs/<slug:slug>/", views.job_detail_view, name="job_detail"),
    path("jobs/<slug:slug>/edit/", views.job_edit_view, name="job_edit"),
    path("jobs/<slug:slug>/delete/", views.job_delete_view, name="job_delete"),
    path("jobs/<slug:slug>/applications/", views.applications_view, name="applications"),
    path("jobs/<slug:slug>/save/", views.save_job_view, name="save_job"),
    path("applications/<int:pk>/<str:status>/", views.update_application_status, name="update_status"),
]
