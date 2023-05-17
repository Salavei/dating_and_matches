from django.db import models
from users.models import User


class ChatName(models.Model):
    """
    Model representing a chat between two users.

    Fields:
    - name: The name of the chat.
    - user_first: The first user in the chat.
    - user_second: The second user in the chat.

    Methods:
    - __str__: Returns a string representation of the chat name.

    """

    name = models.CharField(max_length=150)
    user_first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_first')
    user_second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_second')

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Model representing a chat message.

    Fields:
    - from_id: The user who sent the message.
    - to_id: The user who received the message.
    - message: The content of the message.
    - received_at: The timestamp when the message was received.

    Methods:
    - __str__: Returns a string representation of the message content.

    """

    from_id = models.ForeignKey(User, related_name='from_id', on_delete=models.CASCADE)
    to_id = models.ForeignKey(User, related_name='to_id', on_delete=models.CASCADE)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
