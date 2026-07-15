from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_time

from accounts.models import CustomUser
from .models import Assessment, MoodEntry, Appointment
from content.models import Quote, Resource


# Mood tracker - save and view moods
@login_required
@require_http_methods(["GET", "POST"])
def mood_tracker(request):
    if request.method == "POST":
        mood = request.POST.get("mood")
        note = request.POST.get("note", "")
        
        if not mood:
            messages.error(request, "Please select a mood.")
            return redirect("mood_tracker")
        
        try:
            MoodEntry.objects.create(user=request.user, mood=mood, note=note)
            messages.success(request, "Mood saved successfully!")
        except Exception as e:
            messages.error(request, f"Error saving mood: {e}")
        
        return redirect("mood_tracker")
    
    # Get last 7 moods for the chart
    moods = MoodEntry.objects.filter(user=request.user).order_by('-created_at')[:7]
    
    context = {
        'moods': moods,
    }
    return render(request, 'mood_tracker.html', context)


# Assessment - mental health questionnaire
@login_required
@require_http_methods(["GET", "POST"])
def assessment(request):
    if request.method == "POST":
        try:
            qs = [int(request.POST.get(f"q{i}")) for i in range(1, 6)]
        except (TypeError, ValueError):
            messages.error(request, "Please answer all questions.")
            return redirect("assessment")

        if any(q < 0 or q > 3 for q in qs):
            messages.error(request, "Invalid answers. Please try again.")
            return redirect("assessment")

        Assessment.objects.create(
            user=request.user,
            q1=qs[0],
            q2=qs[1],
            q3=qs[2],
            q4=qs[3],
            q5=qs[4],
        )
        messages.success(request, "Assessment submitted successfully.")
        return redirect("dashboard")

    return render(request, "assessment.html")


# Book appointment - schedule a counseling session
@login_required
@require_http_methods(["GET", "POST"])
def book_appointment(request):
    counselors = CustomUser.objects.filter(role="counselor")

    if request.method == "POST":
        counselor_id = request.POST.get("counselor")
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")
        notes = request.POST.get("notes", "")

        counselor = CustomUser.objects.filter(id=counselor_id, role="counselor").first()
        if not counselor:
            messages.error(request, "Please select a valid counselor.")
            return redirect("book_appointment")

        try:
            appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Invalid date selected.")
            return redirect("book_appointment")

        t = parse_time(time_str) if time_str else None
        if not t:
            messages.error(request, "Please select a time slot.")
            return redirect("book_appointment")

        try:
            Appointment.objects.create(
                user=request.user,
                counselor=counselor,
                date=appt_date,
                time=t,
                notes=notes,
            )
            messages.success(request, "Appointment request submitted.")
        except Exception as e:
            messages.error(request, f"Could not book appointment: {e}")

        return redirect("appointments")

    return render(request, "book_appointment.html", {"counselors": counselors})


# Appointments - view user's appointments
@login_required
@require_http_methods(["GET"])
def appointments(request):
    user_appointments = Appointment.objects.filter(user=request.user).order_by('date', 'time')
    
    context = {
        'appointments': user_appointments,
    }
    return render(request, 'appointments.html', context)


# Dashboard - main user dashboard
@login_required
def dashboard(request):
    user = request.user
    
    # Get counts for the user
    mood_count = MoodEntry.objects.filter(user=user).count()
    assessment_count = Assessment.objects.filter(user=user).count()
    appointment_count = Appointment.objects.filter(user=user, status='approved').count()
    
    # Get a random active quote
    try:
        daily_quote = Quote.objects.filter(status=Quote.Status.ACTIVE).order_by('?').first()
    except Exception:
        daily_quote = None
    
    # Get recent moods
    recent_moods = MoodEntry.objects.filter(user=user).order_by('-created_at')[:4]
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        user=user
    ).exclude(status='cancelled').exclude(status='completed').order_by('date', 'time')[:2]
    
    context = {
        'mood_count': mood_count,
        'assessment_count': assessment_count,
        'appointment_count': appointment_count,
        'daily_quote': daily_quote,
        'recent_moods': recent_moods,
        'upcoming_appointments': upcoming_appointments,
    }
    
    return render(request, 'dashboard.html', context)


# Counselors - list all counselors
def counselors(request):
    counselors = CustomUser.objects.filter(role='counselor')
    
    context = {
        'counselors': counselors,
    }
    return render(request, 'counselors.html', context)


# Resources - list all educational resources
def resources(request):
    resources = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources})


# Logout - log user out and go home
def logout_view(request):
    logout(request)
    return redirect('home')