from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import TeacherProfile

class TeacherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a teacher user
        self.user = User.objects.create_user(
            username="teacher1",
            password="pass123",
            role="teacher"
        )

        # Create a teacher profile
        self.teacher = TeacherProfile.objects.create(
            user=self.user,
            employee_id="faculty0001",
            department="Computer Science",
            subject_specialization="AI",
            qualification="PhD",
            contact_number="1234567890"
        )

        # API endpoints (from router basename="teacher")
        self.list_url = reverse("teacher-list")
        self.detail_url = reverse("teacher-detail", args=[self.teacher.id])

    def test_list_teachers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_teacher(self):
        # Need another teacher user
        new_user = User.objects.create_user(
            username="teacher2",
            password="pass123",
            role="teacher"
        )

        data = {
            "user": new_user.id,
            "employee_id": "faculty0002",  # normally auto-generated, but required for test
            "department": "Mathematics",
            "subject_specialization": "Statistics",
            "qualification": "MPhil",
            "contact_number": "9876543210"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_teacher(self):
        data = {
            "user": self.teacher.user.id,
            "employee_id": self.teacher.employee_id,
            "department": "Software Engineering",
            "subject_specialization": "Deep Learning",
            "qualification": "PhD",
            "contact_number": "1111111111"
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.department, "Software Engineering")

    def test_delete_teacher(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TeacherProfile.objects.count(), 0)
