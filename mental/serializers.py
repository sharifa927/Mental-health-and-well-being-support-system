from rest_framework import serializers

from .models import Assessment, Appointment, MoodEntry


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ("id", "mood", "note", "created_at")


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ("id", "q1", "q2", "q3", "q4", "q5", "total_score", "created_at")


class AppointmentSerializer(serializers.ModelSerializer):
    counselor_email = serializers.EmailField(source="counselor.email", read_only=True)

    class Meta:
        model = Appointment
        fields = ("id", "counselor", "counselor_email", "date", "time", "notes", "status", "created_at")

    def validate_counselor(self, value):
        if value.role != "counselor":
            raise serializers.ValidationError("Selected counselor must have role=counselor")
        return value

