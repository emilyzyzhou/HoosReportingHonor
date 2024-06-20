from django import forms
from .models import Report, File

class ReportForm(forms.ModelForm):
    # enforce data validation in forms even if it is also mentioned in html
    students_involved = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "abc1de, fgh2ij, klm3no"}))
    class Meta:
        model = Report
        fields = ["incident_date", "incident_category", "incident_location", "students_involved", "report_summary"]


# class FileForm(forms.Form): # not a ModelForm since uploading multiple files
#     file_field = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
class FileForm(forms.Form):
    file_field = forms.FileField(required=False) # changed to only handle single form submitted for simplicity since FileInput does not accept multiple files
    # model = File
    # fields = ["file"]
    # file_field = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
