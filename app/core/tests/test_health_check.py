"""
test for the health
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTest(TestCase):

    def test_health_check(self):
        client = APIClient()
        url = reverse('health-check')
        res = client.get(url)
    
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        