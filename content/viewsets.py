from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter

from accounts.permissions import IsAdminRole
from .models import Quote, Resource
from .serializers import QuoteSerializer, ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminRole | permissions.AllowAny]

    queryset = Resource.objects.all().order_by("-created_at")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["type", "category"]
    search_fields = ["title", "description", "category"]

    def perform_create(self, serializer):
        if not (self.request.user and self.request.user.is_authenticated and getattr(self.request.user, "role", None) == "admin"):
            raise permissions.PermissionDenied("Admin only")
        serializer.save(added_by=self.request.user)


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Quote.objects.all().order_by("-created_at")

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "status"]
    search_fields = ["text", "category"]

    def perform_create(self, serializer):
        if not (self.request.user and self.request.user.is_authenticated and getattr(self.request.user, "role", None) == "admin"):
            raise permissions.PermissionDenied("Admin only")
        serializer.save(added_by=self.request.user)

