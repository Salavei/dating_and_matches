from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from captcha.fields import CaptchaField


class MyUserCreationForm(UserCreationForm):
    """
    Custom user creation form that extends the UserCreationForm provided by Django's authentication framework.
    It includes additional fields for user registration and a captcha field for verification.
    """
    captcha = CaptchaField(required=True, error_messages={'invalid': 'Confirmation code error'})

    class Meta:
        model = User
        fields = ['username', 'birthday', 'email', 'gender', 'avatar', 'password1', 'password2', 'captcha']


class UserForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = User
        fields = ['avatar', 'username', 'birthday', 'email', 'bio']
