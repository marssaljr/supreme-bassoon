from django.test import TestCase

# Create your tests here.
class CartTestCase(TestCase):
		def test_init(self):
				self.client.get('/cart/add/1')
				session=self.client.session
#				self.assertEqual(session['cart'], )
