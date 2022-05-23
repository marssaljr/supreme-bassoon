from store.views import home
from django.urls import reverse, resolve
from django.test import TestCase

class StoreUrlsTestCase(TestCase):

	def test_home_page_resolves(self):
		response = reverse("home")
		self.assertEqual(resolve(response).func.__name__, home.__name__)