from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from datetime import datetime


class User(AbstractUser):
    name = models.CharField(max_length=20, verbose_name='имя', default='')
    birthday = models.IntegerField(verbose_name='ваш возраст', null=True)
    # address = models.CharField(max_length=50, verbose_name='address', default= '')
    # mobile = models.CharField(max_length=11, verbose_name='mobile phone', default='')
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(upload_to=f'{email}', default='avatar.svg', verbose_name='фотография')
    gender = models.CharField(verbose_name='Ваш пол', choices=(('парень', 'парень'), ('девушка', 'девушка')), max_length=20, null=True)
    bio = models.TextField(null=True)
    likes = models.IntegerField(null=True)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Photo(models.Model):
    name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(null=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    from_id = models.ForeignKey(User, related_name='from_id', on_delete=models.CASCADE)
    to_id = models.ForeignKey(User, related_name='to_id', on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    received_at = models.DateTimeField(auto_now_add=True)
    # session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # is_read = models.BooleanField()


class EmailVeriRecord(models.Model):
    # Код подтверждения
    code = models.CharField(max_length=20, verbose_name='Проверочный код')
    # Почтовый ящик пользователя
    email = models.EmailField(max_length=50, verbose_name='почтовый ящик пользователя')
    # datetime.now При создании объекта выполнить функцию, чтобы получить время
    # Время отправки
    send_time = models.DateTimeField(default=datetime.now, verbose_name='время отправки', null=True, blank=True)
    # Срок действия
    exprie_time = models.DateTimeField(null=True)
    # Тип почты
    # вариантов перечисления вариантов, один должен быть выбран из указанных элементов
    email_type = models.CharField(choices=(
    ('зарегистрироваться', 'зарегистрировать адрес электронной почты'), ('забыть', ' восстановить пароль ')),
                                  max_length=20)

    def __str__(self):
        return self.email



