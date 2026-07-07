from django.conf import settings
from django.db import models


class MoodEntry(models.Model):
    class Mood(models.TextChoices):
        HAPPY = "happy", "Happy"
        CALM = "calm", "Calm"
        NEUTRAL = "neutral", "Neutral"
        STRESSED = "stressed", "Stressed"
        SAD = "sad", "Sad"
        ANXIOUS = "anxious", "Anxious"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mood_entries")
    mood = models.CharField(max_length=20, choices=Mood.choices)
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.mood}"


class Assessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments")

    # Values 0..3 based on template radio options.
    q1 = models.PositiveSmallIntegerField()
    q2 = models.PositiveSmallIntegerField()
    q3 = models.PositiveSmallIntegerField()
    q4 = models.PositiveSmallIntegerField()
    q5 = models.PositiveSmallIntegerField()

    total_score = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_score = sum([self.q1, self.q2, self.q3, self.q4, self.q5])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assessment({self.user_id}) score={self.total_score}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_appointments")

    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("counselor", "date", "time")
        ordering = ["date", "time"]

    def __str__(self):
        return f"Appt({self.user_id})->{self.counselor_id} {self.date} {self.time} [{self.status}]"

