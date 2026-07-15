from django.test import TestCase

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterSerializerTests(TestCase):
    def test_register_serializer_forces_user_role(self):
        data = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "password123",
            "confirm_password": "password123",
            "terms": True,
            "role": "counselor",
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.role, CustomUser.Role.USER)
