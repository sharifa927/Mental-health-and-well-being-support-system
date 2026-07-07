from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from accounts.permissions import IsAdminRole, IsOwner
from .models import Assessment, Appointment, MoodEntry
from .serializers import AssessmentSerializer, AppointmentSerializer, MoodEntrySerializer


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Assessment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "counselor", "date"]
    # Search on counselor and notes
    search_fields = ["notes", "counselor__full_name", "counselor__email"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "admin":
            return Appointment.objects.all()
        # Counselor dashboard not implemented; keep ownership by requester
        return Appointment.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

