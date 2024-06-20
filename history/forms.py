from django import forms
from shared.models import Report, User


class CaseSearchForm(forms.Form):
    report_hash = forms.UUIDField(label="Case ID",
                                  widget=forms.TextInput(attrs={'placeholder': 'Enter Your Case ID Here',
                                                                'class': 'form-control',
                                                                'required': True}))

    class Meta:
        model = Report
        fields = ["report_hash"]
        labels = {"id": "Case ID"}
        widgets = {
            'id': forms.TextInput(attrs={'placeholder': 'Case ID',
                                         'class': 'form-control',
                                         'required': True})
        }
