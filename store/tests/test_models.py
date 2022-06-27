from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from store.models import *

class StoreModelsTestCase(TestCase):
	def setUp(self):
		#self.newImage = Image()
		image_path = 'store/tests/test_img.jpg'
		#self.newImage.image = SimpleUploadedFile(name='test_img.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
		#self.newImage.save()
		self.product1 = Product.objects.create(name='Test Product', price=24.4, description='Test product sucks')

	def test_create_product(self):		
		self.assertEqual(str(self.product1), self.product1.name)

	#def test_image_upload(self):		
		#self.assertEqual(Image.objects.count(), 1)
		#self.assertEqual(isinstance(Image.objects.values()[0]['img'], str), True)

	#def test_add_image_to_product(self):
		#count = self.product1.images.count
		#self.product1.images.add(self.newImage)
		#self.assertNotEqual(self.product1.images.count, count)
		#self.assertEqual(self.product1.images.all()[0], self.newImage)
