from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session


class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name='имя', default='')
    birthday = models.IntegerField(verbose_name='ваш возраст', null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, verbose_name='фотография')
    gender = models.CharField(verbose_name='Ваш пол', choices=(('парень', 'парень'), ('девушка', 'девушка')),
                              max_length=20, null=True)
    bio = models.TextField(null=True)
    likes = models.IntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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

    def __str__(self):
        return self.message
