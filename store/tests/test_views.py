from django.test import (TestCase, Client)
from django.urls import reverse

class StoreUrlsTestCase(TestCase):
	def setUp(self):
		self.client = Client(SERVER_NAME='localhost')

	def test_home_page_render(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "home.html")