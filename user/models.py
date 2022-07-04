from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, default="", null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default="Cliente gente boa :)", blank=True)
    location = models.CharField(max_length=30, default="Lugar nenhum", blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)

    def __str__(self):
        return str(self.user)
