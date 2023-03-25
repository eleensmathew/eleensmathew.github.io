from django import forms

from .models import CustomUser,Admin_info,PriorityQueue

class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)