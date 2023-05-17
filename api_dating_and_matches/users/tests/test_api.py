from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photos.models import Photo
from ratings.models import MatchGroup
from users.models import User


class UserRegistrationAndRatingViewTestCase(APITestCase):
    def setUp(self):
        # Creating test user
        self.user = User.objects.create(username="newusername",
                                        email="newemail@example.com",
                                        password="efefefe",
                                        gender="female",
                                        birthday=30,
                                        avatar=SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'))
        # Creating test photos
        self.photo1 = Photo.objects.create(
            name='Test photo 1',
            photo='test_photo_1.jpg'
        )

        self.photo2 = Photo.objects.create(
            name='Test photo 2',
            photo='test_photo_2.jpg'
        )

        self.photo3 = Photo.objects.create(
            name='Test photo 3',
            photo='test_photo_3.jpg'
        )

    def test_user_registration_and_rating_creation(self):
        url = reverse('user-registration-and-rating')
        data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'gender': 'male',
            'birthday': 25,
            'avatar': SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
            'ratings': [
                {'photo_id': self.photo1.id, 'rating': 3},
                {'photo_id': self.photo2.id, 'rating': 4},
                {'photo_id': self.photo3.id, 'rating': 2},
            ]
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_exists = User.objects.filter(email=data['email'], username=data['username']).exists()
        self.assertTrue(user_exists)

    def test_user_update(self):
        url = reverse('user-update', kwargs={'pk': self.user.pk})
        self.client.force_authenticate(user=self.user)
        new_data = {
            'username': '12345',
            'email': "newemail@example.com",
            'password': "1234567",
            'old_password': "efefefe",
            'gender': 'female',
            'birthday': 23,
            'avatar': SimpleUploadedFile('avatar.jpg', open('users/tests/omg.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
            'bio': 'New bio information'
        }
        response = self.client.patch(url, new_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.username, self.user.username)
        self.assertEqual(response.email, self.user.email)
        self.assertEqual(response.gender, self.user.gender)
        self.assertEqual(response.birthday,self.user.birthday)
        self.assertEqual(response.avatar, self.user.avatar)
        self.assertEqual(response.bio, self.user.bio)
        self.assertTrue(response.check_password("vvyvvhgvj"))


    def test_user_registration_and_rating_creation_invalid_data(self):
        url = reverse('user-registration-and-rating')
        data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'gender': 'male',
            'birthday': 25,
            'ratings': [
                {'photo_id': self.photo1.id, 'rating': 6},
                {'photo_id': self.photo2.id, 'rating': 'invalid_rating'},
                {'photo_id': self.photo3.id, 'rating': -1},
            ],
            'invalid_field': 'invalid_data'
        }
        response = self.client.post(url, data, format='multipart')
        exists_in_group = MatchGroup.objects.filter(users__email=data['email']).first()
        self.assertIsNone(exists_in_group)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_registration_and_rating_creation_missing_required_field(self):
        url = reverse('user-registration-and-rating')
        data = {
            'email': 'testuser',
            'password': 'testpassword',
            'ratings': [
                {'photo_id': self.photo1.id, 'rating': 3},
                {'photo_id': self.photo2.id, 'rating': 4},
                {'photo_id': self.photo3.id, 'rating': 2},
            ]
        }
        response = self.client.post(url, data, format='multipart')
        exists_in_group = MatchGroup.objects.filter(users__email=data['email']).first()
        self.assertIsNone(exists_in_group)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_registration_and_rating_creation_missing_optional_field(self):
        url = reverse('user-registration-and-rating')
        data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists_in_group = MatchGroup.objects.filter(users__email=data['email']).first()
        self.assertIsNone(exists_in_group)
        user_exists = User.objects.filter(email=data['email'], username=data['username']).exists()
        self.assertFalse(user_exists)
