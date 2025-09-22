from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from students.models import StudentProfile
from .models import ParentProfile

class ParentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a parent user
        self.user = User.objects.create_user(
            username="parent1",
            password="pass123",
            role="parent"
        )

        # Create a child student user & profile (since ParentProfile has ManyToMany children)
        student_user = User.objects.create_user(
            username="student1",
            password="pass123",
            role="student"
        )
        self.student = StudentProfile.objects.create(
            user=student_user,
            roll_number="S001",
            class_name="BSCS",
            section="A"
        )

        # Create a parent profile
        self.parent = ParentProfile.objects.create(
            user=self.user,
            parent_id="parent0001",
            contact_number="1234567890",
            address="Somewhere"
        )
        self.parent.children.add(self.student)

        # API endpoints (from router basename="parent")
        self.list_url = reverse("parent-list")
        self.detail_url = reverse("parent-detail", args=[self.parent.id])

    def test_list_parents(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_parent(self):
        new_user = User.objects.create_user(
            username="parent2",
            password="pass123",
            role="parent"
        )

        data = {
            "user": new_user.id,
            "parent_id": "parent0002",  # normally generated
            "contact_number": "9876543210",
            "address": "Anywhere",
            "children": [self.student.id]  # link existing student
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParentProfile.objects.count(), 2)

    def test_update_parent(self):
        data = {
            "user": self.parent.user.id,
            "parent_id": self.parent.parent_id,
            "contact_number": "1111111111",
            "address": "Updated Address",
            "children": [self.student.id]
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.address, "Updated Address")

    def test_delete_parent(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ParentProfile.objects.count(), 0)
