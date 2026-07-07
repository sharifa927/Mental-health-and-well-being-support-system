from rest_framework import serializers

from .models import Quote, Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            "id",
            "title",
            "type",
            "category",
            "description",
            "file",
            "url",
            "added_by",
            "created_at",
        )
        read_only_fields = ("added_by", "created_at")


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ("id", "text", "category", "status", "added_by", "created_at")
        read_only_fields = ("added_by", "created_at")

