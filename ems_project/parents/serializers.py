from rest_framework import serializers
from .models import ParentProfile

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = "__all__"
