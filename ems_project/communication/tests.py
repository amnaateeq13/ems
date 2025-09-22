from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Message

class MessageAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create two users (sender and receiver)
        self.sender = User.objects.create_user(
            username="sender1",
            password="pass123",
            role="student"
        )
        self.receiver = User.objects.create_user(
            username="receiver1",
            password="pass123",
            role="teacher"
        )

        # Create a message
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, how are you?"
        )

        # API endpoints (from router basename="message")
        self.list_url = reverse("message-list")
        self.detail_url = reverse("message-detail", args=[self.message.id])

    def test_list_messages(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_message(self):
        data = {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "content": "This is a new message"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

    def test_update_message(self):
        data = {
            "sender": self.message.sender.id,
            "receiver": self.message.receiver.id,
            "content": "Updated content",
            "read": True
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, "Updated content")
        self.assertTrue(self.message.read)

    def test_delete_message(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)
