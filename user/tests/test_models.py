from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory

from user.forms import RegisterForm, UpdateProfileForm
import tempfile


class UserModelsTestCase(TestCase):
    def setUp(self):
        self.jacob = {
            "first_name": "jacob",
            "last_name": "mcdonalds",
            "username": "jacob",
            "email": "jacob@gmail.com",
            "password1": "top_secret123213",
            "password2": "top_secret123213",
        }
        self.form = RegisterForm(data=self.jacob)
        self.form.save()

    def test_user_has_a_profile(self):
        self.assertEquals(
            self.form.instance.profile.__str__(), self.form.instance.username
        )
