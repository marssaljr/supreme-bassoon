from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from store.models import *

class StoreModelsTestCase(TestCase):
	def setUp(self):
		self.newImage = Image()
		image_path = 'store/tests/test_img.jpg'
		self.newImage.image = SimpleUploadedFile(name='test_img.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
		self.newImage.save()
	def test_image_upload(self):
		self.assertEqual(Image.objects.count(), 1)