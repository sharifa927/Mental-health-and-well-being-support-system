from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


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

