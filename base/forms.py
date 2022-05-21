from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm
from captcha.fields import CaptchaField


class MyUserCreationForm(UserCreationForm):
    captcha = CaptchaField(required=True, error_messages={'invalid': 'Ошибка кода подтверждения'})

    class Meta:
        model = User
        fields = ['name', 'birthday', 'email', 'gender', 'avatar', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'birthday', 'email', 'bio']
