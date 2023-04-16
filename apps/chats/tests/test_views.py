import json

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from chats.models import Thread, Message

User = get_user_model()


class ThreadCreationViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = 'http://127.0.0.1:8000/api/v1/chats/thread/create/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_thread_created(self):
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        data = json.dumps(dict(participants=[1, 2]))
        response = self.client.post(
            self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(
            Thread.objects.first().participants.first(), self.user
        )
        self.assertEqual(
            Thread.objects.first().participants.last(), self.user2
        )

    def test_invalid_data_rejected(self):
        data = dict(participants=[1])
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ThreadDestroyViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        self.thread = Thread.objects.create()
        self.thread.participants.set([self.user, self.user2])
        self.url = f'http://127.0.0.1:8000/api/v1/chats/' \
                   f'thread/{self.thread.id}/destroy/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.delete(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_participant_required(self):
        self.thread.participants.remove(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_thread_destroyed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Thread.objects.count(), 0)


class ThreadListViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = 'http://127.0.0.1:8000/api/v1/chats/thread/list/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_empty_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_all_threads(self):
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        thread = Thread.objects.create()
        thread.participants.set([self.user, user2])
        thread2 = Thread.objects.create()
        thread2.participants.set([self.user])
        thread3 = Thread.objects.create()
        thread3.participants.set([user2])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], thread.id)
        self.assertEqual(response.data[1]['id'], thread2.id)
        self.assertEqual(Thread.objects.count(), 3)

    def test_get_threads_with_pagination(self):
        thread = Thread.objects.create()
        thread.participants.set([self.user])
        thread2 = Thread.objects.create()
        thread2.participants.set([self.user])
        response = self.client.get(f'{self.url}?limit=1&offset=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], thread2.id)
        self.assertEqual(Thread.objects.count(), 2)


class MessageCreationViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.thread = Thread.objects.create()
        self.thread.participants.set([self.user])
        self.url = f'http://127.0.0.1:8000/api/v1/chats/thread/{self.thread.id}/message/create/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_participant_required(self):
        self.thread.participants.remove(self.user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_new_message_created(self):
        data = json.dumps(dict(text="Test text"))
        response = self.client.post(
            self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.text, "Test text")

    def test_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MessageListViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.thread = Thread.objects.create()
        self.thread.participants.set([self.user])
        self.url = f'http://127.0.0.1:8000/api/v1/chats/thread/{self.thread.id}/message/list/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_participant_required(self):
        self.thread.participants.remove(self.user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_empty_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_all_messages(self):
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        thread2 = Thread.objects.create()
        thread2.participants.set([user2])
        message = Message.objects.create(
            text="Test text1", sender=self.user, thread=self.thread
        )
        message2 = Message.objects.create(
            text="Test text2", sender=user2, thread=self.thread)
        Message.objects.create(text="Test text3", sender=user2, thread=thread2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], message2.id)
        self.assertEqual(response.data[1]['id'], message.id)
        self.assertEqual(Thread.objects.count(), 2)
        self.assertEqual(Message.objects.count(), 3)

    def test_get_threads_with_pagination(self):
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        thread2 = Thread.objects.create()
        thread2.participants.set([user2])
        message = Message.objects.create(
            text="Test text1", sender=self.user, thread=self.thread
        )
        Message.objects.create(
            text="Test text2", sender=user2, thread=self.thread)
        Message.objects.create(text="Test text3", sender=user2, thread=thread2)
        response = self.client.get(f'{self.url}?limit=1&offset=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], message.id)
        self.assertEqual(Thread.objects.count(), 2)
        self.assertEqual(Message.objects.count(), 3)


class MessageMarkingAsReadViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.thread = Thread.objects.create()
        self.thread.participants.set([self.user])
        self.message = Message.objects.create(
            text="Test text1", sender=self.user, thread=self.thread
        )
        self.url = f'http://127.0.0.1:8000/api/v1/chats/' \
                   f'message/{self.message.id}/read/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_message_participant_required(self):
        self.thread.participants.remove(self.user)
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_sender_required(self):
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_marked_as_read(self):
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        self.message.sender = self.user2
        self.message.save()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().is_read, True)


class UnreadMessagesNumberViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = 'http://127.0.0.1:8000/api/v1/chats/message/number-unread/'

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_empty_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 0)

    def test_get_unread_messages_number(self):
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        thread = Thread.objects.create()
        thread.participants.set([self.user])
        thread2 = Thread.objects.create()
        thread2.participants.set([self.user, user2])
        Message.objects.create(
            text="Test text1", sender=self.user, thread=thread
        )
        Message.objects.create(
            text="Test text2", sender=self.user, thread=thread2)
        Message.objects.create(text="Test text3", sender=user2, thread=thread2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 1)
        self.assertEqual(Thread.objects.count(), 2)
        self.assertEqual(Message.objects.count(), 3)
