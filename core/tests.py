from django.test import TestCase
from django.urls import reverse

class TestCore(TestCase):

    # test that index page returns 200
    def test_index_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    # test that legal page returns 200
    def test_legal_returns_200(self):
        response = self.client.get(reverse("legal"))
        self.assertEqual(response.status_code, 200)
