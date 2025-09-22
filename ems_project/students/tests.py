from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import StudentProfile
from users.models import User   # adjust if your StudentProfile links differently

class StudentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for linking to student
        self.user = User.objects.create_user(
            username="student1",
            password="pass123",
            role="student"
        )
        self.student = StudentProfile.objects.create(
            user=self.user,
            roll_number="S001",
            class_name="BSCS",
            section="A"
        )
        # DRF reverse auto-resolves router URLs (basename="student")
        self.list_url = reverse("student-list")
        self.detail_url = reverse("student-detail", args=[self.student.id])

    def test_list_students(self):
        """Test GET all students"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_student(self):
        """Test POST create student"""
        new_user = User.objects.create_user(
            username="student2",
            password="pass123",
            role="student"
        )
        data = {
            "user": new_user.id,
            "roll_number": "S002",
            "class_name": "BSCS",
            "section": "B"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentProfile.objects.count(), 2)

    def test_update_student(self):
        """Test PUT update student"""
        data = {
            "user": self.student.user.id,
            "roll_number": "S001",
            "class_name": "MSCS",
            "section": "B"
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.class_name, "MSCS")

    def test_delete_student(self):
        """Test DELETE student"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StudentProfile.objects.count(), 0)
