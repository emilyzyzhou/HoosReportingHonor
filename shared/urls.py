from django.urls import path
from . import views

app_name = "shared"
urlpatterns = [
    path("", views.home, name="home"),
    path("reports/admin", views.admin_report_list, name="admin_report_list"),
    path("render_object_from_s3/<path:s3_object_url>", views.render_object_from_s3, name="render_object_from_s3"),
]
