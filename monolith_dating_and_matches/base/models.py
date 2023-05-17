from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib


class Photo(models.Model):
    """
    Represents a photo uploaded by a user.

    Attributes:
        name (str): The name of the photo.
        photo (ImageField): The image file for the photo.
    """

    name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Represents a user in the system.

    Attributes:
        username (str): The username of the user.
        birthday (int): The age of the user.
        email (str): The email address of the user (unique).
        avatar (ImageField): The profile photo of the user.
        gender (str): The gender of the user.
        bio (str): The biography or additional information about the user.
        likes (int): The number of likes received by the user.
        hash (str): The hashed representation of the user's email address.
    """

    username = models.CharField(max_length=20, verbose_name='Name')
    birthday = models.IntegerField(verbose_name='Your age')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users', null=True, verbose_name='Photo')
    gender = models.CharField(
        verbose_name='Your gender',
        choices=(('male', 'male'), ('female', 'female')),
        max_length=20
    )
    bio = models.TextField(null=True)
    likes = models.IntegerField()
    hash = models.CharField(max_length=64, unique=True, default=None, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender', 'likes', 'birthday']

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a hash value for the user's email if it is not provided.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        if self.hash is None:
            self.hash = hashlib.sha256(self.email.encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class ChatName(models.Model):
    """
    Represents the name of a chat conversation between two users.

    Attributes:
        name (str): The name of the chat.
        user_first (ForeignKey): The first user in the chat.
        user_second (ForeignKey): The second user in the chat.
    """

    name = models.CharField(max_length=150)
    user_first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_first')
    user_second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_second')

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Represents a message in a chat conversation.

    Attributes:
        from_id (ForeignKey): The user who sent the message.
        to_id (ForeignKey): The user who received the message.
        message (str): The content of the message.
        received_at (DateTimeField): The timestamp when the message was received.
    """

    from_id = models.ForeignKey(User, related_name='from_id', on_delete=models.CASCADE)
    to_id = models.ForeignKey(User, related_name='to_id', on_delete=models.CASCADE)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
