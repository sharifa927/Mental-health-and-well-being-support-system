from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import CustomUser


# Register - create a new user account
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        # Create the user
        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                role="user"
            )
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")

    return render(request, "register.html")


# Login - authenticate user and redirect to dashboard
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            dj_login(request, user)
            # Clear old messages (like "account created") before adding new ones
            storage = messages.get_messages(request)
            storage.used = True
            name = user.full_name or user.email or "user"
            messages.success(request, f"Login successful. Welcome back, {name}!")
            if user.is_superuser or getattr(user, 'role', None) == CustomUser.Role.ADMIN:
                return redirect("admin_dashboard")
            return redirect("dashboard")
        messages.error(request, "Invalid email or password.")
        return render(request, "login.html")
    return render(request, "login.html")

# Logout - log user out and go home
@login_required
def logout_view(request):
    dj_logout(request)
    messages.success(request, "Logged out.")
    return redirect("home")