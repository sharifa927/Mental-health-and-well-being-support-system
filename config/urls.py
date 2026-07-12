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