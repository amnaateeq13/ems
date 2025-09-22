from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from courses.models import Course
from .models import TimeTable, TimeSlot

class TimetableAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create teacher user
        self.teacher = User.objects.create_user(
            username="teacher1", password="pass123", role="teacher"
        )

        # Create a course
        self.course = Course.objects.create(
            name="Math",
            code="MATH101",
            description="Basic Mathematics",
            teacher=self.teacher
        )

        # Create a timeslot
        self.time_slot = TimeSlot.objects.create(
            start_time="09:00",
            end_time="10:00"
        )

        # Create a timetable entry
        self.timetable = TimeTable.objects.create(
            day="monday",
            course=self.course,
            teacher=self.teacher,
            class_name="BSCS",
            section="A",
            room="R101",
            time_slot=self.time_slot,
        )

        # DRF router endpoints (assuming basename="timetable")
        self.list_url = reverse("timetable-list")
        self.detail_url = reverse("timetable-detail", args=[self.timetable.id])

    def test_list_timetables(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_timetable(self):
        data = {
            "day": "tuesday",
            "course": self.course.id,
            "teacher": self.teacher.id,
            "class_name": "BSCS",
            "section": "B",
            "room": "R102",
            "time_slot": self.time_slot.id,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_timetable(self):
        data = {
            "day": "wednesday",
            "course": self.course.id,
            "teacher": self.teacher.id,
            "class_name": "BSCS",
            "section": "C",
            "room": "R103",
            "time_slot": self.time_slot.id,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.timetable.refresh_from_db()
        self.assertEqual(self.timetable.day, "wednesday")
        self.assertEqual(self.timetable.section, "C")

    def test_delete_timetable(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TimeTable.objects.count(), 0)
