from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import BusinessCard

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["job_title", "phone", "company"]

class BusinessCardForm(forms.ModelForm):
    class Meta:
        model = BusinessCard
        fields = ["full_name", "email", "phone", "company", "position", "profile_picture"]
        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'})
        }