from django.urls import path

from . import views

urlpatterns = [
    path("resources/", views.resources, name="resources"),
    path("quotes/", views.quotes, name="quotes"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

