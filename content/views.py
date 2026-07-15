from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from content.models import Quote, Resource

@require_http_methods(["GET", "POST"])
def resources(request):
    resources_list = Resource.objects.order_by("-created_at")
    return render(request, "resources.html", {"resources": resources_list})


@require_http_methods(["GET", "POST"])
def quotes(request):
    quotes_list = Quote.objects.filter(status=Quote.Status.ACTIVE).order_by("-created_at")
    return render(request, "quotes.html", {"quotes": quotes_list})


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

