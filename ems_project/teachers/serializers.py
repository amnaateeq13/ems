from rest_framework import serializers
from .models import TeacherProfile

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = "__all__"
