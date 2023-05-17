from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chat.models import ChatName, Message
from users.models import User

from chat.serializers import MessageSerializer


class ChatView(APIView):
    """
    API view for handling chat-related operations.

    This view provides the functionality to retrieve chat messages and send new messages.

    Methods:
    - get: Retrieve chat messages between the authenticated user and another user.
    - post: Send a new chat message to another user.

    """

    def get(self, request, hash):
        """
        Retrieve chat messages between the authenticated user and another user.

        Parameters:
        - hash: The hash of the other user.

        Returns:
        - A response containing the serialized chat messages.

        """
        to_user = get_object_or_404(User, hash=hash)
        _, _ = ChatName.objects.get_or_create(
            name=request.user.email + to_user.email,
            user_first=request.user,
            user_second=to_user
        )
        queryset1 = Message.objects.select_related('from_id', 'to_id').filter(
            from_id=request.user.id, to_id=to_user
        )
        queryset2 = Message.objects.select_related('from_id', 'to_id').filter(
            from_id=to_user, to_id=request.user.id
        )
        messages_chat = queryset1.union(queryset2).order_by('received_at')

        serializer = MessageSerializer(messages_chat, many=True)

        return Response(serializer.data)

    def post(self, request, hash):
        """
        Send a new chat message to another user.

        Parameters:
        - hash: The hash of the other user.

        Returns:
        - A response containing the serialized chat message if the message is sent successfully,
          or the error messages if there are validation errors.

        """
        to_user = get_object_or_404(User, hash=hash)
        if request.data.get('message'):
            message_data = {
                'from_id': request.user.id,
                'to_id': to_user.id,
                'message': request.data['message']
            }
            serializer = MessageSerializer(data=message_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)
