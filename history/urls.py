from django.urls import path
from . import views

app_name = "history"
urlpatterns = [
    path("lookup/", views.lookup, name="lookup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("report/", views.report, name="report"),
    path("delete/", views.delete, name="delete"),
    path("report-details/", views.report_details, name="report_details"),
    path("update-report-status/", views.update_report_status, name="update_report_status"),
    path('set_timezone/', views.set_timezone, name='set_timezone'),
]
