from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from content.views import about, contact, resources


# VIEWS -connect URLs to HTML files

def home(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def counselors(request):
    return render(request, 'counselors.html')


def profile(request):
    return render(request, 'profile.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def counselor_dashboard(request):
    return render(request, 'counselor_dashboard.html')


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


urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML routes
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    path('about/', about, name='about'),
    path('resources/', resources, name='resources'),
    path('counselors/', counselors, name='counselors'),
    path('profile/', profile, name='profile'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('counselor-dashboard/', counselor_dashboard, name='counselor_dashboard'),

    path('terms/', terms, name='terms'),
    path('contact/', contact, name='contact'),

    # Auth/mental HTML POST handlers
    path('', include('accounts.urls')),
    path('', include('mental.urls')),

    # Admin management pages
    path('admin-users/', admin_users, name='admin_users'),
    path('admin-counselors/', admin_counselors, name='admin_counselors'),
    path('admin-resources/', admin_resources, name='admin_resources'),
    path('admin-quotes/', admin_quotes, name='admin_quotes'),

    # DRF + JWT API
    path('api/', include('config.api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

