from django.test import TestCase, Client
from django.urls import reverse

class BasicTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status(self):
        """Test that home page returns 200 status code"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """Test that home page uses correct template"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html') 