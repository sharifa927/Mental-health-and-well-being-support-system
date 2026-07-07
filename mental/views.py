from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_time

from accounts.models import CustomUser
from .models import Assessment, MoodEntry, Appointment


@login_required
@require_http_methods(["GET", "POST"])
def mood_tracker(request):
    if request.method == "POST":
        mood = request.POST.get("mood")
        note = request.POST.get("note", "")
        if not mood:
            messages.error(request, "Mood is required.")
            return redirect("mood_tracker")
        try:
            MoodEntry.objects.create(user=request.user, mood=mood, note=note)
            messages.success(request, "Mood entry saved.")
        except Exception as e:
            messages.error(request, f"Could not save mood entry: {e}")
        return redirect("mood_tracker")
    return render(request, "mood_tracker.html")


@login_required
@require_http_methods(["GET", "POST"])
def assessment(request):
    if request.method == "POST":
        try:
            qs = [int(request.POST.get(f"q{i}")) for i in range(1, 6)]
        except (TypeError, ValueError):
            messages.error(request, "All assessment answers must be selected.")
            return redirect("assessment")

        if any(q < 0 or q > 3 for q in qs):
            messages.error(request, "Assessment values must be between 0 and 3.")
            return redirect("assessment")

        Assessment.objects.create(
            user=request.user,
            q1=qs[0],
            q2=qs[1],
            q3=qs[2],
            q4=qs[3],
            q5=qs[4],
        )
        messages.success(request, "Assessment submitted. Thank you.")
        return redirect("assessment_results")

    return render(request, "assessment.html")


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
            messages.error(request, "Invalid counselor selected.")
            return redirect("book_appointment")

        try:
            appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Invalid date.")
            return redirect("book_appointment")

        t = parse_time(time_str) if time_str else None
        if not t:
            messages.error(request, "Invalid time slot.")
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
            messages.error(request, f"Could not create appointment: {e}")

        return redirect("appointments")

    return render(request, "book_appointment.html", {"counselors": counselors})


@login_required
@require_http_methods(["GET"])
def appointments(request):
    appts = Appointment.objects.filter(user=request.user)
    # Template is static; still return render.
    return render(request, "appointments.html", {"appointments": appts})

