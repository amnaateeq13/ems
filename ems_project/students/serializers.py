from rest_framework import serializers
from .models import StudentProfile   # adjust if your model name differs

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"
