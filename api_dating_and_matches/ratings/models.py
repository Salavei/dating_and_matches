from django.db import models
from users.models import User


class MatchGroup(models.Model):
    """
    Model representing a group of matches.

    Each match group has a name and can have multiple users associated with it.

    Fields:
    - name: CharField representing the name of the match group.
    - users: ManyToManyField representing the users associated with the match group.

    Methods:
    - __str__: Returns a string representation of the match group (name).

    """

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __str__(self):
        """
        Returns a string representation of the match group.
        """
        return self.name
