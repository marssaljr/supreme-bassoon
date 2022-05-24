from django.db import models

# Create your models here.
class Image(models.Model):
	img = models.ImageField(upload_to='img')
	#def __str__(self) -> str:
		#return self.img.url

class Product(models.Model):
	name = models.CharField(max_length=200)
	images = models.ManyToManyField(Image)
	price = models.FloatField()
	description = models.TextField()

	def __str__(self) -> str:
		return self.name