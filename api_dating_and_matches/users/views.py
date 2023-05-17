from django.views.generic.base import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from ratings.utils import calculate_grades_and_create_cache
from users.models import User
from users.permissions import IsOwner
from users.serializers import (
    UserLoginSerializer,
    UserSerializer,
    UserRegistrationAndRatingSerializer,
)
from ratings.models import MatchGroup
from users.utils.service import send_message__about_register
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class UserRegistrationAndRatingView(APIView):
    def post(self, request):
        """
        User registration and rating endpoint.
        """
        serializer = UserRegistrationAndRatingSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid:
            final_hash = calculate_grades_and_create_cache(request.data)
            try:
                user = serializer.save()
            except Exception as e:
                logger.exception(e)
                return Response(
                    {'message': 'User registration failed'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                group, created = MatchGroup.objects.get_or_create(name=final_hash)
                group.users.add(user)
            except Exception as e:
                logger.exception(e)
                user.delete()
                return Response(
                    {'message': 'User and photo ratings were not saved'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
            }
            # Sending message about successful register on email
            send_message__about_register(email=request.data.get('email'), password=request.data.get('password'))
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        User login endpoint.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken:
            raise AuthenticationFailed("Invalid token.")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
