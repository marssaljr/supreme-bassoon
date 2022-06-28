from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, default="", null=True, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='img/', null=True)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	def __str__(self):
			return str(self.user)
