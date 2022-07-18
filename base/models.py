from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
import hashlib


class Photo(models.Model):
    name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name='Name', default='')
    birthday = models.IntegerField(verbose_name='Your age', null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(upload_to='users', null=True, verbose_name='Photo')
    gender = models.CharField(verbose_name='Your gender', choices=(('male', 'male'), ('female', 'female')),
                              max_length=20, null=True)
    bio = models.TextField(null=True)
    likes = models.IntegerField(null=True)
    hash = models.CharField(max_length=64, unique=True, default=None, null=True)
    ph = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.hash is None:
            self.hash = hashlib.sha256(self.email.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class ChatName(models.Model):
    name = models.CharField(max_length=150)
    user_first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_first')
    user_second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_second')

    def __str__(self):
        return self.name


class Message(models.Model):
    from_id = models.ForeignKey(User, related_name='from_id', on_delete=models.CASCADE)
    to_id = models.ForeignKey(User, related_name='to_id', on_delete=models.CASCADE)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

