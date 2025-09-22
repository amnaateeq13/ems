from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from courses.models import Course
from .models import Attendance
from datetime import date

class AttendanceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a teacher user
        self.teacher = User.objects.create_user(
            username="teacher1",
            password="pass123",
            role="teacher"
        )

        # Create a student user
        self.student = User.objects.create_user(
            username="student1",
            password="pass123",
            role="student"
        )

        # Create a course taught by teacher
        self.course = Course.objects.create(
            name="Computer Networks",
            code="CN101",
            description="Networking basics",
            teacher=self.teacher
        )

        # Create an attendance record
        self.attendance = Attendance.objects.create(
            student=self.student,
            teacher=self.teacher,
            course=self.course,
            date=date.today(),
            status="present"
        )

        # API endpoints (from router basename="attendance")
        self.list_url = reverse("attendance-list")
        self.detail_url = reverse("attendance-detail", args=[self.attendance.id])

    def test_list_attendance(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)


    def test_update_attendance(self):
        data = {
            "student": self.attendance.student.id,
            "teacher": self.attendance.teacher.id,
            "course": self.attendance.course.id,
            "date": str(self.attendance.date),
            "status": "late"
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, "late")

    def test_delete_attendance(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)
