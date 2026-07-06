from django.contrib import admin
from django.urls import path
from django.shortcuts import render


# VIEWS -connect URLs to HTML files
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def about(request):                     # ✅ NEW - About page view
    return render(request, 'about.html')

def assessment(request):
    return render(request, 'assessment.html')

def mood_tracker(request):
    return render(request, 'mood_tracker.html')

def counselors(request):
    return render(request, 'counselors.html')

def book_appointment(request):
    return render(request, 'book_appointment.html')

def appointments(request):
    return render(request, 'appointments.html')

def resources(request):
    return render(request, 'resources.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def counselor_dashboard(request):
    return render(request, 'counselor_dashboard.html')

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

def admin_users(request):
    return render(request, 'admin_users.html')

def admin_counselors(request):
    return render(request, 'admin_counselors.html')

def admin_resources(request):
    return render(request, 'admin_resources.html')

def admin_quotes(request):
    return render(request, 'admin_quotes.html')

# URL PATTERNS -Map URLs to views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),              # ✅ NEW - About page URL
    path('assessment/', assessment, name='assessment'),
    path('mood-tracker/', mood_tracker, name='mood_tracker'),
    path('counselors/', counselors, name='counselors'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('appointments/', appointments, name='appointments'),
    path('resources/', resources, name='resources'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('counselor-dashboard/', counselor_dashboard, name='counselor_dashboard'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
    path('admin-users/', admin_users, name='admin_users'),
    path('admin-counselors/', admin_counselors, name='admin_counselors'),
    path('admin-resources/', admin_resources, name='admin_resources'),
    path('admin-quotes/', admin_quotes, name='admin_quotes'),
]