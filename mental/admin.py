from django.contrib import admin

from .models import Assessment, Appointment, MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mood", "created_at")
    search_fields = ("user__email", "user__full_name")
    list_filter = ["mood", "created_at"]



@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_score", "created_at")
    search_fields = ("user__email", "user__full_name")
    list_filter = ["created_at"]



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "counselor", "date", "time", "status")
    search_fields = ("user__email", "counselor__email")
    list_filter = ("status", "date")

