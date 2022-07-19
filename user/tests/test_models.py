from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from user.models import *
import tempfile


class UserModelsTestCase(TestCase):
    def setUp(self):
        newProfile = Profile.objects.create()
