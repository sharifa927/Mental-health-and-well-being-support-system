from django.urls import path

from . import views

urlpatterns = [
    path("resources/", views.resources, name="resources"),
    path("quotes/", views.quotes, name="quotes"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import CustomUser
from mental.models import Appointment, Assessment, MoodEntry
from content.models import Resource, Quote

def admin_dashboard(request):
    # Get real counts from database
    total_users = CustomUser.objects.count()
    total_counselors = CustomUser.objects.filter(role='counselor').count()
    total_appointments = Appointment.objects.count()
    total_resources = Resource.objects.count()
    total_assessments = Assessment.objects.count()
    total_moods = MoodEntry.objects.count()
    total_quotes = Quote.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    context = {
        'total_users': total_users,
        'total_counselors': total_counselors,
        'total_appointments': total_appointments,
        'total_resources': total_resources,
        'total_assessments': total_assessments,
        'total_moods': total_moods,
        'total_quotes': total_quotes,
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'admin_dashboard.html', context)