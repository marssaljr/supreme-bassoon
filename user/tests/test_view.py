from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from unittest.mock import patch
from user.views import login

class UserViewTestCase(TestCase):
		def setUp(self):
				self.client=Client(SERVER_NAME='localhost')
				self.factory=RequestFactory()
				self.jacob={
												'username':'jacob',
												'email':'jacob@...',
												'password':'top_secret'
				}
				self.testUser=User.objects.create_user(username=self.jacob['username'], email=self.jacob['email'], password=self.jacob['password'])
				self.testUser.is_activated=True
				self.testUser.save()
		def test_register_page_returns(self):
				url=reverse('register')
				response=self.client.get(url)
				self.assertEqual(response.status_code,200)
		def test_register_page_redirect(self):
				url=reverse('register')
				self.client.force_login(User.objects.get_or_create(username='test')[0])
				response=self.client.get(url)
				self.assertEqual(response.status_code, 302)
		def test_register_page_create_user(self):
				url=reverse('register')
				response=self.client.post(url, {'username':'vicky','email':'test@test.com','password':'test'})
				user=User.objects.filter(username='vicky')
				self.assertEqual(user.exists(), True)
		def test_register_page_user_already_exists(self):
				url=reverse('register')
				data=['vicky','test@test.com','test']
				user=User.objects.create(username=data[0],email=data[1],password=data[2])
				response=self.client.post(url, {'username':data[0],'email':data[1],'password':data[2]})
				self.assertEqual(response.status_code, 302)

		def test_register_page_fail_parse(self):
				url=reverse('register')
				data=['','','test']
				response=self.client.post(url, {'username': data[0], 'email':data[1],'password':data[2]})
				self.assertEqual(response.status_code, 302)
		def test_register_page_fail_unexpected(self):
				url=reverse('register')
				data=['vicky','test@test.com','test']
				user=User.objects
				with patch.object(user, 'create_user') as mock_user:
					mock_user.side_effect=Exception('Unexpected Error')
					res=self.client.post(url, {'username': data[0],'email':data[1],'password': data[2]})
					self.assertEqual(res.url, '/user/register')
		def test_login_page_user_already_logged_in(self):
				req=self.factory.get('/user/login')
				req.user=self.testUser
				res=login(req)
				self.assertEqual(res.url, '/')
		def test_login_page_newuser(self):
				url=reverse('login')
				res=self.client.get(url)
				self.assertEqual(res.status_code, 200)
				self.assertTemplateUsed(res,'login.html')
		def test_login_page_user_loggin(self):
				url=reverse('login')
				res=self.client.post(url, self.jacob)
				#req=self.factory.post('/user/login',self.jacob)
				#res=login(req)
				self.assertRedirects(res, '/')
				self.assertEqual(res.url, '/')
		def test_login_page_user_loggin_fail(self):
				url=reverse('login')
				res=self.client.post(url, {'username':'','password':''})
				self.assertRedirects(res, '/user/login')
				self.assertEqual(res.url, '/user/login')
		def test_user_logout(self):
				url=reverse('logout')
				res=self.client.get(url)				
				user=auth.get_user(self.client)
				self.assertEquals(user.is_authenticated, False)
				self.assertRedirects(res, '/user/login')
				#https://stackoverflow.com/questions/48968016/django-tests-user-authenticate-fails
#https://stackoverflow.com/questions/70426709/unit-testing-an-authenticated-user-in-django
