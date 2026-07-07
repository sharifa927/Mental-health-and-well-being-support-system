from rest_framework.routers import DefaultRouter

from content.viewsets import QuoteViewSet, ResourceViewSet
from mental.viewsets import AssessmentViewSet, AppointmentViewSet, MoodEntryViewSet

router = DefaultRouter()
router.register(r"moods", MoodEntryViewSet, basename="moods")
router.register(r"assessments", AssessmentViewSet, basename="assessments")
router.register(r"appointments", AppointmentViewSet, basename="appointments")
router.register(r"resources", ResourceViewSet, basename="resources")
router.register(r"quotes", QuoteViewSet, basename="quotes")

urlpatterns = router.urls

