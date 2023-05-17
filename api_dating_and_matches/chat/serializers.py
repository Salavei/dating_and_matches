from rest_framework.serializers import ModelSerializer

from chat.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('from_id', 'to_id', 'message', 'received_at')
