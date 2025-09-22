from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Course

class CourseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        
        self.teacher_user = User.objects.create_user(
            username="teacher1",
            password="pass123",
            role="teacher"
        )

      
        self.course = Course.objects.create(
            name="Intro to CS",
            code="CS101",
            description="Basics of Computer Science",
            teacher=self.teacher_user
        )

        
        self.list_url = reverse("course-list")
        self.detail_url = reverse("course-detail", args=[self.course.id])

    def test_list_courses(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_course(self):
        new_teacher = User.objects.create_user(
            username="teacher2",
            password="pass123",
            role="teacher"
        )

        data = {
            "name": "Data Structures",
            "code": "CS102",
            "description": "Study of data structures",
            "teacher": new_teacher.id
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        data = {
            "name": "Intro to CS Updated",
            "code": "CS101",
            "description": "Updated course description",
            "teacher": self.teacher_user.id
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Intro to CS Updated")

    def test_delete_course(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
