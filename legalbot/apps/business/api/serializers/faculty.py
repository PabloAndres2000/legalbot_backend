from rest_framework import serializers

from legalbot.apps.business.models import Faculty


class FacultyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["name", "is_active"]
