from django.test import TestCase
from django.urls import reverse

from .models import Quote, Resource


class PublicContentViewsTests(TestCase):
    def test_resources_page_shows_admin_added_resources(self):
        Resource.objects.create(
            title="Stress Relief Guide",
            type=Resource.Type.ARTICLE,
            category="Wellness",
            description="A helpful guide for stress management.",
            url="https://example.com/stress"
        )

        response = self.client.get(reverse("resources"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stress Relief Guide")

    def test_quotes_page_shows_only_active_quotes(self):
        Quote.objects.create(text="Keep going.", category=Quote.Category.MOTIVATION, status=Quote.Status.ACTIVE)
        Quote.objects.create(text="Pause and breathe.", category=Quote.Category.WELLNESS, status=Quote.Status.INACTIVE)

        response = self.client.get(reverse("quotes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Keep going.")
        self.assertNotContains(response, "Pause and breathe.")
