from django.test import AsyncClient, TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from unittest.mock import patch

from user.views import CustomLoginView, delete
from user.forms import RegisterForm, UpdateUserForm, UpdateProfileForm
from user.models import Profile


class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client(SERVER_NAME="localhost")
        self.async_client = AsyncClient(SERVER_NAME="localhost")
        self.factory = RequestFactory()
        self.jacob = {
            "username": "jacob",
            "email": "jacob@...",
            "password": "top_secret",
        }
        self.testUser = User.objects.create_user(
            username=self.jacob["username"],
            email=self.jacob["email"],
            password=self.jacob["password"],
        )
        self.testUser.is_active = True
        self.testUser.save()

    def test_register_page_returns(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_page_redirect(self):
        url = reverse("register")
        self.client.force_login(User.objects.get_or_create(username="test")[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_register_page_create_user(self):
        url = reverse("register")
        data = {
            "first_name": "vicky1",
            "last_name": "vickesty",
            "username": "vicky1",
            "email": "vicky@gmail.com",
            "password1": "vicky12321312321",
            "password2": "vicky12321312321",
        }
        form = RegisterForm(data=data)
        self.assertEquals(form.is_bound, True)
        response = self.client.post(url, data)
        self.assertRedirects(response, "/user/login")

    def test_register_page_user_already_exists(self):
        url = reverse("register")
        data = ["vicky", "test@test.com", "test"]
        user = User.objects.create(username=data[0], email=data[1], password=data[2])
        response = self.client.post(
            url, {"username": data[0], "email": data[1], "password": data[2]}
        )
        self.assertEquals(response.headers["X-Frame-Options"], "DENY")

    def test_register_page_fail_parse(self):
        url = reverse("register")
        data = ["", "", "test"]
        response = self.client.post(
            url, {"username": data[0], "email": data[1], "password": data[2]}
        )
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_register_page_fail_unexpected(self):
        url = reverse("register")
        data = ["vicky", "test@test.com", "test"]
        user = User.objects
        with patch.object(user, "create_user") as mock_user:
            mock_user.side_effect = Exception("Unexpected Error")
            res = self.client.post(
                url, {"username": data[0], "email": data[1], "password": data[2]}
            )
            self.assertEqual(res.headers["X-Frame-Options"], "DENY")

    def test_login_page_user_already_logged_in(self):
        self.client.force_login(self.testUser)
        res = self.client.get("/user/login")
        self.assertRedirects(res, "/user/profile")

    def test_login_page_newuser(self):
        url = reverse("login")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "login.html")

    def test_login_page_user_loggin(self):
        url = reverse("login")
        res = self.client.post(url, self.jacob)
        self.assertRedirects(res, "/user/profile")

    def test_login_page_user_loggin_fail(self):
        url = reverse("login")
        res = self.client.post(url, {"username": "", "password": ""})
        self.assertEqual(res.headers["X-Frame-Options"], "DENY")
        self.assertEqual(res.status_code, 200)

    def test_user_logout(self):
        url = reverse("logout")
        res = self.client.get(url)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, False)
        self.assertRedirects(res, "/user/login")

    def test_user_profile_returns(self):
        url = reverse("profile")
        self.client.force_login(self.testUser)
        req = self.client.get(url)
        req.user = self.testUser
        user_form = UpdateUserForm(instance=req.user)
        profile_form = UpdateProfileForm(instance=req.user.profile)
        self.assertEquals(req.context["user_form"].instance, user_form.instance)
        self.assertEquals(
            req.context["profile_form"].fields.keys(), profile_form.fields.keys()
        )

    def test_delete_user_page_fails(self):
        url = reverse("delete")
        res = self.client.get(url)
        self.assertRedirects(res, "/user/login")

    def test_delete_user_page_returns(self):
        self.client.force_login(self.testUser)
        res = self.client.get("/user/delete")
        self.assertContains(res, "Tem certeza que deseja deletar a sua conta?")
        self.assertTemplateUsed(res, "delete.html")

    def test_delete_user_fails(self):
        res = self.client.post("/user/delete")
        self.assertRedirects(res, "/user/login")

    def test_delete_user_succeed(self):
        self.client.force_login(self.testUser)
        profile = Profile.objects.filter(user=self.testUser)
        user = User.objects.filter(pk=self.testUser.id)
        res = self.client.post("/user/delete")
        self.assertEqual(profile.exists(), False)
        self.assertEqual(user.exists(), False)
        self.assertEqual(res.context["success"], "ok")
        # https://stackoverflow.com/questions/48968016/django-tests-user-authenticate-fails


# https://stackoverflow.com/questions/70426709/unit-testing-an-authenticated-user-in-django
