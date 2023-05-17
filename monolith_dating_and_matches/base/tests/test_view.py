import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from base.models import Photo, ChatName, Message, User


class PhotoModelTest(TestCase):
    def test_photo_creation(self):

        expected_name = f'test{datetime.datetime.now().microsecond}.jpg'
        photo = Photo.objects.create(name='Test Photo', photo=SimpleUploadedFile(expected_name,
        open('base/tests/omg.jpg', 'rb').read(),content_type='image/jpeg'))
        self.assertEqual(photo.name, 'Test Photo')
        self.assertEqual(photo.photo.name, expected_name)


class UserModelTest(TestCase):
    def test_user_creation(self):
        expected_name = f'avatar{datetime.datetime.now().microsecond}.jpg'
        user = User.objects.create_user(
            username='testuser',
            birthday=25,
            email='test@example.com',
            avatar=SimpleUploadedFile(expected_name, open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='male',
            bio='Test bio',
            likes=10,
            password='testpassword'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.birthday, 25)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.avatar.name.split('/')[-1], expected_name)
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.bio, 'Test bio')
        self.assertEqual(user.likes, 10)
        self.assertTrue(user.check_password('testpassword'))


class ChatNameModelTest(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='testuser1',
            birthday=25,
            email='test0@example.com',
            avatar=SimpleUploadedFile('avatar2.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='male',
            bio='Test bio',
            likes=10,
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            birthday=19,
            email='test1@example.com',
            avatar=SimpleUploadedFile('avatar3.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='female',
            bio='Test bio',
            likes=20,
            password='testpassword'
        )

    def test_chat_name_creation(self):
        chat_name = ChatName.objects.create(name='Test Chat', user_first=self.user1, user_second=self.user2)
        self.assertEqual(chat_name.name, 'Test Chat')
        self.assertEqual(chat_name.user_first, self.user1)
        self.assertEqual(chat_name.user_second, self.user2)


class MessageModelTest(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='testuser1',
            birthday=25,
            email='test0@example.com',
            avatar=SimpleUploadedFile('avatar4.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='male',
            bio='Test bio',
            likes=10,
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            birthday=19,
            email='test1@example.com',
            avatar=SimpleUploadedFile('avatar5.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='female',
            bio='Test bio',
            likes=20,
            password='testpassword'
        )

    def test_message_creation(self):
        message = Message.objects.create(from_id=self.user1, to_id=self.user2, message='Test message')
        self.assertEqual(message.from_id, self.user1)
        self.assertEqual(message.to_id, self.user2)
        self.assertEqual(message.message, 'Test message')


class ViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            birthday=25,
            email='test0@example.com',
            avatar=SimpleUploadedFile('avatar6.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='male',
            bio='Test bio',
            likes=10,
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            birthday=42,
            email='test10@example.com',
            avatar=SimpleUploadedFile('avatar6.jpg', open('base/tests/omg.jpg', 'rb').read(),
                                      content_type='image/jpeg'),
            gender='male',
            bio='Test bio',
            likes=10,
            password='testpassword'
        )

    def test_profile_view(self):
        self.client.login(email='test0@example.com', password='testpassword')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/user_profile.html')

    def test_chat_view(self):
        self.client.login(email='test0@example.com', password='testpassword')
        response = self.client.get(f'/chat/{self.user2.hash}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/chat.html')
