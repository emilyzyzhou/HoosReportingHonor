from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponse
from .models import Report, File
import boto3
from urllib.parse import urlparse


# Create your views here.
def home(request):
    return render(request, "shared/home.html")


def is_site_admin(user):
    return user.is_authenticated and (user.is_staff or user.profile.is_admin)


@login_required
@user_passes_test(is_site_admin)
def admin_report_list(request):
    completed_reports = Report.objects.prefetch_related('file_set').all()
    return render(request, 'history/dashboard.html', {'reports': completed_reports})


@login_required
@user_passes_test(is_site_admin)
def report_detail(request, report_id):
    report = get_object_or_404(Report.objects.prefetch_related('file_set'), pk=report_id)
    return render(request, 'shared/report_details.html', {'report': report})


def render_object_from_s3(request, s3_object_url):
    s3 = boto3.client('s3')
    parsed_url = urlparse(s3_object_url)
    bucket_name = 'honor-code-reporting-a-22'
    object_key = parsed_url.path.lstrip('/')
    file = s3.get_object(Bucket=bucket_name, Key=object_key)
    object_data = file['Body'].read()
    content_type = file['ContentType']
    response = HttpResponse(object_data, content_type=content_type)
    return response
