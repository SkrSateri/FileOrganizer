from django import forms
from .models import File

class searchFormByAllInfo(forms.ModelForm):
    class Meta:
        model = File
        widgets = {
            'uploadDate': forms.TextInput(attrs={'placeholder': 'Add date with order year-month-day'}),
        }
        fields = [
            'fileName',
            'lastUploadBy',
            'uploadDate',
        ]

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'fileName',
            'fileDescription',
            'fileContent',
        ]