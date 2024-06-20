from django.urls import path
from . import views

app_name = "submit"
urlpatterns = [
    path("", views.start_submission, name="start_submission"),
    path("report", views.report, name="report"),
    path("submission_complete", views.submission_complete, name="submission_complete"),
    path("incident_categories", views.incident_categories, name="incident_categories"),
]
