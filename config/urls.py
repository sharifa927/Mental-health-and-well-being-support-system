from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Import views from mental app
from mental.views import (
    dashboard, mood_tracker, assessment, book_appointment, 
    appointments, counselors, resources
)


# Views - connect URLs to HTML files
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def profile(request):
    return render(request, 'profile.html')


def admin_dashboard(request):
    from accounts.models import CustomUser
    from mental.models import Appointment, MoodEntry, Assessment
    from content.models import Resource, Quote

    context = {
        'total_users': CustomUser.objects.filter(role=CustomUser.Role.USER).count(),
        'total_counselors': CustomUser.objects.filter(role=CustomUser.Role.COUNSELOR, is_counselor_active=True).count(),
        'total_appointments': Appointment.objects.count(),
        'total_resources': Resource.objects.count(),
        'total_quotes': Quote.objects.count(),
        'total_mood_entries': MoodEntry.objects.count(),
        'total_assessments': Assessment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


def counselor_dashboard(request):
    return render(request, 'counselor_dashboard.html')


def contact(request):
    return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')


def admin_users(request):
    return render(request, 'admin_users.html')


def admin_counselors(request):
    from django.contrib import messages
    from accounts.models import CustomUser

    # Handle add / delete actions
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            specialization = request.POST.get("specialization")
            experience_years = request.POST.get("experience_years") or 0
            avail_text = request.POST.get("availability", "")
            availability = []
            for line in avail_text.splitlines():
                parts = line.strip()
                if not parts:
                    continue
                try:
                    day, times = parts.split()
                    start, end = times.split("-")
                    availability.append({"day": day, "start": start, "end": end})
                except Exception:
                    # ignore malformed lines
                    continue

            try:
                # create a counselor account with a random password (admin can share with counselor later)
                user = CustomUser.objects.create_user(
                    email=email,
                    password=CustomUser.objects.make_random_password(),
                    full_name=full_name,
                    role=CustomUser.Role.COUNSELOR,
                    specialization=specialization,
                    experience_years=int(experience_years) if experience_years else 0,
                    is_counselor_active=True,
                )
                user.availability = availability
                user.save()
                messages.success(request, "Counselor added successfully.")
            except Exception as e:
                messages.error(request, f"Could not add counselor: {e}")
            return render(request, 'admin_counselors.html', {"counselors": CustomUser.objects.filter(role=CustomUser.Role.COUNSELOR)})

        if action == "delete":
            try:
                cid = request.POST.get("counselor_id")
                c = CustomUser.objects.get(pk=cid, role=CustomUser.Role.COUNSELOR)
                c.delete()
                messages.success(request, "Counselor deleted.")
            except Exception as e:
                messages.error(request, f"Could not delete counselor: {e}")
            return render(request, 'admin_counselors.html', {"counselors": CustomUser.objects.filter(role=CustomUser.Role.COUNSELOR)})

    counselors = CustomUser.objects.filter(role=CustomUser.Role.COUNSELOR)
    return render(request, 'admin_counselors.html', {"counselors": counselors})


def admin_resources(request):
    return render(request, 'admin_resources.html')


def admin_quotes(request):
    return render(request, 'admin_quotes.html')


# URL Patterns - map URLs to views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # This handles login, register, logout
    
    # Public pages
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
    
    # User pages (require login)
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('assessment/', assessment, name='assessment'),
    path('mood-tracker/', mood_tracker, name='mood_tracker'),
    path('counselors/', counselors, name='counselors'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('appointments/', appointments, name='appointments'),
    path('resources/', resources, name='resources'),
    
    # Admin pages
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_users, name='admin_users'),
    path('admin-counselors/', admin_counselors, name='admin_counselors'),
    path('admin-resources/', admin_resources, name='admin_resources'),
    path('admin-quotes/', admin_quotes, name='admin_quotes'),
    
    # Counselor pages
    path('counselor-dashboard/', counselor_dashboard, name='counselor_dashboard'),
]