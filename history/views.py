from django.shortcuts import render, redirect, get_object_or_404
from shared.models import Report
from .forms import CaseSearchForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse


def lookup(request):
    if request.method == "POST":
        form = CaseSearchForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data['report_hash']
            report = get_object_or_404(Report, report_hash=uuid)
            return render(request, "history/report_details.html", {"report": report})
        else:
            return render(request, "history/lookup.html", {'form': form, 'error': "Invalid case ID"})
    else:
        form = CaseSearchForm()
        return render(request, "history/lookup.html", {'form': form})

@login_required
def dashboard(request):
    profile = request.user.profile
    user = request.user
    if user.is_superuser:
        reports = Report.objects.filter(user=user)
    elif hasattr(user, 'profile') and profile.is_admin:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(user=user)

    current_timezone = timezone.get_current_timezone_name()

    return render(request, "history/dashboard.html", {'reports': reports, 'current_timezone': current_timezone}, )


@login_required
@require_POST
def report(request):
    report_id = request.POST.get('report_id')
    if not report_id:
        return redirect("history:dashboard")

    report_model = get_object_or_404(Report, id=report_id)

    if request.user.profile.is_admin:
        if "notes" in request.POST:
            report_model.report_text = request.POST.get("notes")
            report_model.save()
            return redirect("history:report", id=report_model.id)

        if "change_status_to_pending" in request.POST and report_model.status == "NEW":
            report_model.status = "PENDING"
            report_model.save()

    request.session['viewing_report_id'] = str(report_model.id)
    return redirect("history:report_details")


@login_required
@require_POST
def update_report_status(request):
    report_id = request.POST.get('report_id')
    if not report_id:
        return redirect('history:dashboard')

    # handles whatever status is passed in the POST request e.g. 'REJECTED' or 'APPROVED'
    report = get_object_or_404(Report, id=report_id)
    if request.user.profile.is_admin:
        if 'status' in request.POST:
            report.status = request.POST.get('status')
            report.save()
            messages.success(request, "Status updated successfully.")
            request.session['viewing_report_id'] = str(report.id)
            return redirect('history:report_details')
        elif "notes" in request.POST:
            report.report_text = request.POST.get("notes")
            report.save()
            messages.success(request, "Notes added successfully.")
            request.session['viewing_report_id'] = str(report.id)
            return redirect("history:report_details")
    return redirect('history:report_details')


def report_details(request):
    report_id = request.session.get('viewing_report_id')
    if not report_id:
        # Handle case where no report ID is found in the session?
        return redirect("history:dashboard")

    report_model = get_object_or_404(Report, id=report_id)
    current_timezone = timezone.get_current_timezone_name()
    del request.session['viewing_report_id']
    return render(request, "history/report_details.html",
                  {"report": report_model, 'current_timezone': current_timezone})


@login_required
@require_POST
def delete(request):
    report_id = request.POST.get('report_id')
    if report_id:
        report = get_object_or_404(Report, id=report_id)
        report.delete()
        return redirect("history:dashboard")
    else:
        return redirect("history:dashboard")

    #  REFERENCES


#  AI Agent: ChatGPT4
#  Date: 2024-4-25
# Prompt: "how can I access a user's local timezone without manually prompting them for it in a Django project and send it to the server for processing and displaying a datetime?"
def set_timezone(request):
    if request.method == 'POST':
        timezone = request.POST.get('timezone')
        if timezone:
            request.session['django_timezone'] = timezone
            # print("Timezone received and set:", timezone)
            return JsonResponse({'status': 'success', 'message': 'Timezone updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No timezone provided.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
