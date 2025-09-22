from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from .models import Fee
from datetime import date

class FeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a student user
        self.student = User.objects.create_user(
            username="student1", password="pass123", role="student"
        )

        # Create one Fee record
        self.fee = Fee.objects.create(
            student=self.student,
            annual_fee=5000.00,
            year=date.today().year,
            due_date=date.today(),
            status="unpaid"
        )

        # Match urls.py → fees/api/fees/
        self.list_url = "/fees/api/fees/"
        self.detail_url = f"/fees/api/fees/{self.fee.id}/"

    def test_list_fees(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_fee(self):
        new_student = User.objects.create_user(
            username="student2", password="pass123", role="student"
        )
        data = {
            "student": new_student.id,
            "annual_fee": "6000.00",
            "year": date.today().year,
            "due_date": str(date.today()),
            "status": "paid",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Fee.objects.count(), 2)

    def test_update_fee(self):
        data = {
            "student": self.fee.student.id,
            "annual_fee": "5500.00",
            "year": self.fee.year,
            "due_date": str(self.fee.due_date),
            "status": "paid",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fee.refresh_from_db()
        self.assertEqual(str(self.fee.annual_fee), "5500.00")
        self.assertEqual(self.fee.status, "paid")

    def test_delete_fee(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Fee.objects.count(), 0)
