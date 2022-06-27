from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import (TestCase, Client)
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from store.models import Product

class StoreViewsTestCase(TestCase):
	def setUp(self):
		self.client = Client(SERVER_NAME='localhost')
		image_path='store/tests/test_img.jpg'
		self.image = SimpleUploadedFile(name='test_image.jpg',
																		content=open(image_path,'rb').read(),
																		content_type='image/jpeg')
		self.product = Product.objects.create(name='Paracetamol', price=12.5, image=self.image, stock=3)
		self.product.save()
		self.user = User.objects.create(username='test')
		self.user.set_password('12345')
		self.user.save()

	def test_home_page_render(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "home.html")
	def test_cart_detail_page_not_render(self):
		url = reverse('cart_detail')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
	def test_cart_add_not_works(self):
		url = reverse('cart_add', args=(0,))
		response=self.client.get(url)
		self.assertEqual(response.status_code, 302)
	def test_cart_detail_page_render(self):
		url = reverse('cart_detail')
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'cart_detail.html')
	def test_cart_add_item(self):
		id=self.product.id
		url=reverse('cart_add', args=(id,))
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		response=self.client.get(url)
		self.assertEqual(len(self.client.session['cart']),1)
	def test_cart_clear_all_items(self):
		url=reverse('cart_clear')
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		response=self.client.get(url)
		self.assertEqual(len(self.client.session['cart']),0)
	def test_cart_quantity_increment(self):
		id=self.product.id
		url=reverse('cart_add', args=(id,))
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		response1=self.client.get(url)
		response2=self.client.get(url)
		self.assertEqual(len(self.client.session.get('cart')),1)
	def test_item_increment(self):
		id=self.product.id
		url=reverse('cart_inc', args=(id,))
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		response=self.client.get(url)
		self.assertEqual(len(self.client.session.get('cart')),1)
	def test_item_decrement(self):
		id=self.product.id
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		url=reverse('cart_add', args=(id,))
		response=self.client.get(url)
		quantity=self.client.session.get('cart').get('1')['quantity']
		self.assertEqual(quantity,1)
		url=reverse('cart_dec', args=(id,))
		response=self.client.get(url)
		quantity=self.client.session.get('cart').get('1')['quantity']
		self.assertNotEqual(quantity,0)
	def test_item_remove(self):
		id=self.product.id
		self.client.force_login(User.objects.get_or_create(username='test')[0])
		url=reverse('cart_add', args=(id,))
		self.client.get(url)
		url=reverse('cart_rem', args=(id,))
		response=self.client.get(url)
		self.assertEqual(response.url, '/cart/cart-detail/')
		product=self.client.session.get('cart')
		self.assertEqual(product, {})
	def test_item_decrement_fail(self):
		id=self.product.id
		# self.client.force_login(User.objects.get_or_create(username='test')[0])
		# url=reverse('cart_dec', args=(id,))
		# response=self.client.get(url)
		# quantity=self.client.session.get('

	# def test_cart_quantity_add(self):
	# 	id=self.product.id
	# 	url=reverse('cart_add', args=(id,))
	# 	self.client.force_login(User.objects.get_or_create(username='test')[0])
	# 	response=self.client.get(url)
	# 	self.product.stock=0
	# 	response=self.client.get(url)
	# 	self.assertEqual(len(self.client.session['cart']),1)
