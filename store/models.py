from django.db import models

class Image(models.Model):
	img = models.ImageField(upload_to='img')

class Product(models.Model):
	name = models.CharField(max_length=200)
	images = models.ManyToManyField(Image)
	price = models.FloatField()
	description = models.TextField()

	def __str__(self) -> str:
		return self.name
