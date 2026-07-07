from django.contrib import admin

from .models import Quote, Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "category", "added_by", "created_at")
    search_fields = ("title", "category")
    list_filter = ("type", "category", "created_at")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "status", "created_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("text",)

