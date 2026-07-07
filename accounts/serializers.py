from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "dob",
            "role",
            "specialization",
            "experience_years",
            "is_counselor_active",
            "is_active",
            "date_joined",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "confirm_password", "terms", "role")
        extra_kwargs = {"terms": {"write_only": True}}

    terms = serializers.BooleanField(write_only=True)
    role = serializers.ChoiceField(choices=["user", "counselor"], default="user")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        if not attrs.get("terms"):
            raise serializers.ValidationError({"terms": "You must accept the terms"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        validated_data.pop("terms", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

