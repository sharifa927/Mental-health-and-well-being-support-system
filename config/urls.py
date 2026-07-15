from django.contrib import admin, messages
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

# Import views from mental app
from mental.views import (
    dashboard, mood_tracker, assessment, book_appointment,
    appointments, counselors
)
from content.views import resources as content_resources, quotes as content_quotes


# Views - connect URLs to HTML files
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@login_required
def profile(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        dob = request.POST.get('dob', '').strip()

        user = request.user
        user.full_name = full_name
        user.phone = phone
        user.dob = dob if dob else None
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html', {'user': request.user})


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
    from django.contrib import messages
    from accounts.models import CustomUser

    # Handle delete user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            try:
                uid = request.POST.get('user_id')
                user = CustomUser.objects.get(pk=uid)
                # prevent deleting superuser or self
                if user.is_superuser or user == request.user:
                    messages.error(request, "Cannot delete this user.")
                else:
                    user.delete()
                    messages.success(request, "User deleted.")
            except Exception as e:
                messages.error(request, f"Could not delete user: {e}")
            return render(request, 'admin_users.html', {"users": CustomUser.objects.all()})

    users = CustomUser.objects.all()
    return render(request, 'admin_users.html', {"users": users})


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
            # Support new UI: availability can be posted as JSON in `availability_json`
            import json
            availability = []
            avail_json = request.POST.get("availability_json")
            if avail_json:
                try:
                    parsed = json.loads(avail_json)
                    # expect list of {day, start, end}
                    if isinstance(parsed, list):
                        availability = parsed
                except Exception:
                    availability = []
            else:
                avail_text = request.POST.get("availability", "")
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
                if not email:
                    messages.error(request, "Email is required to add a counselor.")
                else:
                    # If a user with this email exists, convert them to a counselor instead of creating duplicate
                    existing = CustomUser.objects.filter(email=email).first()
                    if existing:
                        if existing.role == CustomUser.Role.COUNSELOR:
                            messages.error(request, "A counselor with this email already exists.")
                        else:
                            existing.role = CustomUser.Role.COUNSELOR
                            existing.specialization = specialization or existing.specialization
                            existing.experience_years = int(experience_years) if experience_years else existing.experience_years
                            existing.is_counselor_active = True
                            existing.availability = availability
                            existing.save()
                            messages.success(request, "Existing user updated to counselor.")
                    else:
                        # create a new counselor account with a random password (admin can share with counselor later)
                        random_password = get_random_string(12)
                        user = CustomUser.objects.create_user(
                            email=email,
                            password=random_password,
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
    from django.contrib import messages
    from content.models import Resource

    # Handle add / delete
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            title = request.POST.get('title', '').strip()
            rtype = request.POST.get('type', '')
            category = request.POST.get('category', '').strip()
            description = request.POST.get('description', '').strip()
            url = request.POST.get('url', '').strip()
            file = request.FILES.get('file') if hasattr(request, 'FILES') else None

            if not title or not rtype:
                messages.error(request, 'Title and type are required.')
            else:
                try:
                    res = Resource.objects.create(
                        title=title,
                        type=rtype,
                        category=category,
                        description=description,
                        url=url or None,
                        added_by=request.user if request.user.is_authenticated else None,
                    )
                    if file:
                        res.file = file
                        res.save()
                    messages.success(request, 'Resource added.')
                except Exception as e:
                    messages.error(request, f'Could not add resource: {e}')
            return render(request, 'admin_resources.html', {"resources": Resource.objects.all()})

        if action == 'delete':
            try:
                rid = request.POST.get('resource_id')
                r = Resource.objects.get(pk=rid)
                r.delete()
                messages.success(request, 'Resource deleted.')
            except Exception as e:
                messages.error(request, f'Could not delete resource: {e}')
            return render(request, 'admin_resources.html', {"resources": Resource.objects.all()})

    resources = Resource.objects.all()
    return render(request, 'admin_resources.html', {"resources": resources})


def admin_quotes(request):
    from django.contrib import messages
    from content.models import Quote

    # Handle add / delete actions
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            text = request.POST.get('text', '').strip()
            category = request.POST.get('category', '')
            if not text:
                messages.error(request, 'Quote text cannot be empty.')
            else:
                try:
                    Quote.objects.create(text=text, category=category or Quote.Category.MOTIVATION, added_by=request.user)
                    messages.success(request, 'Quote added.')
                except Exception as e:
                    messages.error(request, f'Could not add quote: {e}')
            return render(request, 'admin_quotes.html', {"quotes": Quote.objects.all()})

        if action == 'delete':
            try:
                qid = request.POST.get('quote_id')
                q = Quote.objects.get(pk=qid)
                q.delete()
                messages.success(request, 'Quote deleted.')
            except Exception as e:
                messages.error(request, f'Could not delete quote: {e}')
            return render(request, 'admin_quotes.html', {"quotes": Quote.objects.all()})

    quotes = Quote.objects.all()
    return render(request, 'admin_quotes.html', {"quotes": quotes})


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
    path('resources/', content_resources, name='resources'),
    path('quotes/', content_quotes, name='quotes'),
    
    # Admin pages
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_users, name='admin_users'),
    path('admin-counselors/', admin_counselors, name='admin_counselors'),
    path('admin-resources/', admin_resources, name='admin_resources'),
    path('admin-quotes/', admin_quotes, name='admin_quotes'),
    
    # Counselor pages
    path('counselor-dashboard/', counselor_dashboard, name='counselor_dashboard'),
]