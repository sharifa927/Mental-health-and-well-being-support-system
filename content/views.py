from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from content.models import Quote

@require_http_methods(["GET", "POST"])
def resources(request):
    return render(request, "resources.html")


@require_http_methods(["GET", "POST"])
def quotes(request):
    return render(request, "quotes.html")


@require_http_methods(["GET", "POST"])
def about(request):
    return render(request, "about.html")


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        # No model in templates; store-less handling for now.
        messages.success(request, "Message sent. Thank you!")
        return redirect("contact")
    return render(request, "contact.html")

    from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MoodEntry, Assessment, Appointment
from content.models import Quote

@login_required
def dashboard(request):
    user = request.user
    
    # Get real data from database
    mood_count = MoodEntry.objects.filter(user=user).count()
    assessment_count = Assessment.objects.filter(user=user).count()
    appointment_count = Appointment.objects.filter(user=user, status='approved').count()
    
    # Get today's quote
    try:
        daily_quote = Quote.objects.filter(is_active=True).order_by('?').first()
    except:
        daily_quote = None
    
    # Get recent moods
    recent_moods = MoodEntry.objects.filter(user=user).order_by('-created_at')[:4]
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        user=user, 
        status__in=['pending', 'approved']
    ).order_by('date', 'time')[:2]
    
    context = {
        'mood_count': mood_count,
        'assessment_count': assessment_count,
        'appointment_count': appointment_count,
        'daily_quote': daily_quote,
        'recent_moods': recent_moods,
        'upcoming_appointments': upcoming_appointments,
    }
    
    return render(request, 'dashboard.html', context)

