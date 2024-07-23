from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Bio Here!"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password!"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}))

    class Meta:
        model = User
        fields = ["username", "email", "bio"]