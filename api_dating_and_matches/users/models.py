from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ("non-binary", "Non-binary"),
    ("genderqueer", "Genderqueer"),
    ("agender", "Agender")
]


class User(AbstractUser):
    """
    Custom user model representing a user in the system.

    Fields:
        username (CharField): The username of the user.
        birthday (IntegerField): The age of the user.
        email (EmailField): The email address of the user.
        avatar (ImageField): The user's profile photo.
        gender (CharField): The gender of the user.
        bio (TextField): The user's bio.
        hash (CharField): The unique hash value of the user's email.

    Additional Required Fields:
        username, gender, birthday, avatar

    Attributes:
        USERNAME_FIELD (str): The field to use as the unique identifier for authentication (email).
        REQUIRED_FIELDS (list): The fields required during user creation (username, gender, birthday, avatar).

    Methods:
        save: Overrides the save method to generate the user's hash value based on the email address.

    Example Usage:
        user = User.objects.create(username='JohnDoe', birthday=25, email='john.doe@example.com',
                                   avatar='path/to/avatar.jpg', gender='male', bio='Hello, I am John!')
    """

    username = models.CharField(max_length=20, verbose_name='Name')
    birthday = models.IntegerField(verbose_name='Your age', validators=[MinValueValidator(18), MaxValueValidator(100)])
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users', null=True, verbose_name='Photo')
    gender = models.CharField(verbose_name='Your gender', choices=GENDER_CHOICES, max_length=20)
    bio = models.TextField(null=True)
    hash = models.CharField(max_length=64, unique=True, default=None, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender', 'birthday', 'avatar']

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate the user's hash value based on the email address.
        """
        if self.hash is None:
            self.hash = hashlib.sha256(self.email.encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the username of the user.
        """
        return self.username
