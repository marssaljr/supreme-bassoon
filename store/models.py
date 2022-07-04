from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="media")
    stock = models.IntegerField()
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name
