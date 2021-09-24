from django import forms
from .models import File

class SearchForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'fileName',
        ]
    
class searchFormByUploader(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'lastUploadBy'
        ]

class searchFormByUploadDate(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'uploadDate'
        ]

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'fileName',
            'fileDescription',
            'fileContent',
        ]