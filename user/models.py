from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, default="", null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default="Cliente gente boa :)", blank=True)
    location = models.CharField(max_length=30, default="Lugar nenhum", blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
