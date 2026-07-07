from django.conf import settings
from django.db import models


class Resource(models.Model):
    class Type(models.TextChoices):
        ARTICLE = "article", "Article"
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF Guides"
        AUDIO = "audio", "Audio"

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=Type.choices)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Optional file/link support
    file = models.FileField(upload_to="resources/%Y/%m/%d/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="resources_added")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quote(models.Model):
    class Category(models.TextChoices):
        MOTIVATION = "motivation", "Motivation"
        INSPIRATION = "inspiration", "Inspiration"
        WELLNESS = "wellness", "Wellness"
        HOPE = "hope", "Hope"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    text = models.TextField()
    category = models.CharField(max_length=30, choices=Category.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes_added")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:40]

