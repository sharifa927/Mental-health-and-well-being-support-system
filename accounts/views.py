from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import CustomUser
from .serializers import RegisterSerializer


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        data = {
            "email": request.POST.get("email"),
            "full_name": request.POST.get("full_name"),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password"),
            "terms": request.POST.get("terms") == "on",
        }
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save(role="user")
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        messages.error(request, str(serializer.errors))
    return render(request, "register.html")


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            dj_login(request, user)
            messages.success(request, "Login successful.")
            return redirect("dashboard")
        messages.error(request, "Invalid email or password.")
    return render(request, "login.html")


@login_required
def logout_view(request):
    dj_logout(request)
    messages.success(request, "Logged out.")
    return redirect("home")

