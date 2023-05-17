from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
       Custom token obtain pair serializer to use email as the username field for authentication.

       Attributes:
           username_field (str): The field to use as the unique identifier for authentication (email).

       Example Usage:
           class MyTokenObtainPairView(TokenObtainPairView):
               serializer_class = MyTokenObtainPairSerializer
       """
    username_field = 'email'


class UserRegistrationAndRatingSerializer(serializers.ModelSerializer):
    """
        Serializer for user registration and rating.

        Attributes:
            Meta:
                model (User): The User model.
                fields (list): The fields to include in the serializer.
                extra_kwargs (dict): Additional keyword arguments for specific fields.

        Example Usage:
            class UserRegistrationAndRatingView(APIView):
                def post(self, request):
                    serializer = UserRegistrationAndRatingSerializer(data=request.data)
                    ...
        """

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'gender', 'birthday', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': True},
        }


class UserSerializer(serializers.ModelSerializer):
    """
      Serializer for user details and updates.

      Attributes:
          password (CharField): The user's password.
          old_password (CharField): The user's old password.

          Meta:
              model (User): The User model.
              fields (tuple): The fields to include in the serializer.

      Methods:
          validate: Validates the old password provided by the user.
          update: Updates the user instance with validated data.

      Example Usage:
          class UserUpdateAPIView(generics.UpdateAPIView):
              permission_classes = [IsAuthenticated, IsOwner]
              serializer_class = UserSerializer
      """
    password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'old_password', 'gender', 'birthday', 'avatar', 'bio')

    def validate(self, attrs):
        """
                Validates the old password provided by the user.

                Args:
                    attrs (dict): The dictionary containing the serializer attributes.

                Returns:
                    dict: The validated attributes.

                Raises:
                    serializers.ValidationError: If the old password is missing or incorrect.
        """
        old_password = attrs.get('old_password', None)
        if old_password is None:
            raise serializers.ValidationError('Please provide your old password')

        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Old password does not match')

        return attrs

    def update(self, instance, validated_data):
        """
           Updates the user instance with validated data.

           Args:
               instance (User): The user instance to update.
               validated_data (dict): The validated data.

           Returns:
               User: The updated user instance.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.bio = validated_data.get('bio', instance.bio)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Validates the user's email and password.

        Args:
            attrs (dict): Dictionary containing the email and password.

        Raises:
            serializers.ValidationError: If no active account is found with the given credentials
                                           or if the password is incorrect.

        Returns:
            dict: A dictionary containing the refresh token, access token, user ID, and email.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        # Retrieve the user instance associated with the given email
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No active account found with the given credentials")

        # Check if the provided password matches the user's password
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)

        # Prepare the response data
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email
        }
        return data
