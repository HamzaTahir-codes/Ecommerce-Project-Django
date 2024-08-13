from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your UserName", "class" : "form-group"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Bio Here!"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password!"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}))

    class Meta:
        model = User
        fields = ["username", "email", "bio"]

class ProfileUpdateForm(forms.ModelForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))

    class Meta:
        model = Profile
        fields = ["full_name", "image", "bio", "phone"]