from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from students.models import StudentProfile
from teachers.models import TeacherProfile
from .models import ExamResult

class ExamResultAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample users
        self.student_user = User.objects.create_user(
            username="student1", password="pass123", role="student"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher1", password="pass123", role="teacher"
        )

        # Related profiles
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user, roll_number="ST001", class_name="BSCS", section="A"
        )
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_id="faculty0001",
            department="CS",
            subject_specialization="AI",
        )

        # One ExamResult
        self.exam_result = ExamResult.objects.create(
            student=self.student_profile,
            teacher=self.teacher_profile,
            subject="Math",
            exam_name="midterm",
            total_marks=100,
            obtained_marks=85,
        )

        # Correct API endpoints from router
        self.list_url = reverse("exams:examresult-list")
        self.detail_url = reverse("exams:examresult-detail", args=[self.exam_result.id])

    def test_list_exam_results(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exam_result(self):
        data = {
            "student": self.student_profile.id,
            "teacher": self.teacher_profile.id,
            "subject": "Physics",
            "exam_name": "final",
            "total_marks": 100,
            "obtained_marks": 90,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_exam_result(self):
        data = {
            "student": self.student_profile.id,
            "teacher": self.teacher_profile.id,
            "subject": "Math",
            "exam_name": "midterm",
            "total_marks": 100,
            "obtained_marks": 95,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_exam_result(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
