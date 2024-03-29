from django import forms
from .models import User


class searchUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'surname',
        ]

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'surname',
            'username',
            'password',
            'isAdmin'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }