from django.urls import path
from . import views

urlpatterns = [
    path("assessment/", views.assessment, name="assessment"),
    path("mood-tracker/", views.mood_tracker, name="mood_tracker"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("appointments/", views.appointments, name="appointments"),
    path('dashboard/', dashboard, name='dashboard'),
]