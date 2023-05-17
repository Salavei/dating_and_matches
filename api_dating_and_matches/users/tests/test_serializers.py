from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.request import Request

from users.serializers import MyTokenObtainPairSerializer, UserSerializer, UserRegistrationAndRatingSerializer, \
    UserLoginSerializer


class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            gender='female',
            birthday=30,
            avatar=SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
            bio='New bio information'
        )

    def test_valid_credentials(self):
        serializer = UserLoginSerializer(data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.assertIn('refresh', data)
        self.assertIn('access', data)
        self.assertEqual(data['user_id'], self.user.id)
        self.assertEqual(data['email'], self.user.email)

    def test_invalid_credentials(self):
        serializer = UserLoginSerializer(data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class UserRegistrationAndRatingSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_valid_serializer(self):
        serializer = UserRegistrationAndRatingSerializer(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'gender': 'male',
            'birthday': 25,
            'avatar': SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
        })
        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        serializer = UserRegistrationAndRatingSerializer(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'gender': 'invalid',
            'birthday': 16,
            'avatar': None
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 3)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            username='testuser',
            gender='male',
            birthday=25,
            avatar=SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg')
        )

    def test_valid_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.fields.keys()),
                         {'username', 'email', 'password', 'old_password', 'gender', 'birthday', 'avatar', 'bio'})

    def test_update_serializer(self):
        new_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': "efefefe",
            'old_password': self.user.password,
            'gender': 'female',
            'birthday': 30,
            'avatar': SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
            'bio': 'New bio information'
        }
        serializer = UserSerializer(instance=self.user, data=new_data)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, new_data['username'])
        self.assertEqual(updated_user.email, new_data['email'])
        self.assertEqual(updated_user.gender, new_data['gender'])
        self.assertEqual(updated_user.birthday, new_data['birthday'])
        self.assertEqual(updated_user.avatar, new_data['avatar'])
        self.assertEqual(updated_user.bio, new_data['bio'])
        self.assertTrue(updated_user.check_password(new_data['password']))

    def test_invalid_serializer(self):
        serializer = UserSerializer(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'test',
            'old_password': self.user.password,
            'gender': 'invalid',
            'birthday': 16,
            'avatar': None,
            'bio': 'New bio information'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 3)

    class MyTokenObtainPairSerializerTest(TestCase):
        def test_username_field(self):
            serializer = MyTokenObtainPairSerializer()
            self.assertEqual(serializer.username_field, 'email')
