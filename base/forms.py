from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm
from captcha.fields import CaptchaField


class MyUserCreationForm(UserCreationForm):
    captcha = CaptchaField(required=True, error_messages={'invalid': 'Confirmation code error'})

    class Meta:
        model = User
        fields = ['username', 'birthday', 'email', 'gender', 'avatar', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'birthday', 'email', 'bio']
