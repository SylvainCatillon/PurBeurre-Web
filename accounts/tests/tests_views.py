from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

def redirected_to_myaccount(instance, response):
    """Test if a user is authenticated and redirected to 'my account'"""
    instance.assertTrue(response.wsgi_request.user.is_authenticated)
    instance.assertRedirects(
        response, "/accounts/myaccount/",
        msg_prefix="User not redirected to myaccount")

class CreateTestCase(TestCase):
    def setUp(self):
        self.user_info = {
            "username": "test_user",
            "email": "user@test.com",
            "password1": "test_user_password",
            "password2": "test_user_password",
            "first_name": "Paul"}


    # test create page returns 200 if user is not logged
    def test_get_create_unlogged_user(self):
        response = self.client.get(reverse("accounts:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="create_form"')

    # test create page don't show the form to a logged user
    def test_get_create_logged_user(self):
        username = "test_user"
        password = "test_user_password"
        User.objects.create_user(
            username=username,
            email="user@test.com",
            password=password)
        self.client.login(username=username, password=password)
        response = self.client.get(reverse("accounts:create"))
        self.assertNotContains(response, 'id="create_form"')

    # test unmatch password
    def test_unmatch_password(self):
        self.user_info["password2"] = "unmatch_password"
        response = self.client.post(reverse("accounts:create"), self.user_info)
        self.assertFormError(
            response, "form", "password2",
            _('The two password fields didn’t match.'))

    # test a user is created and the user is redirected to myaccount
    def test_user_created(self):
        self.assertIsNone(authenticate(
            username=self.user_info["username"], password=self.user_info["password1"]))
        response = self.client.post(reverse("accounts:create"), self.user_info)
        self.assertIsNotNone(authenticate(
            username=self.user_info["username"], password=self.user_info["password1"]))
        redirected_to_myaccount(self, response)


class MyAccountTestCase(TestCase):
    """Test the view 'accounts:my_account'"""
    def setUp(self):
        self.user_info = {
            "username": "test_user",
            "email": "user@test.com",
            "password": "test_user_password",
            "first_name": "Paul"}
        self.user = User.objects.create_user(**self.user_info)


    # test a user not logged is redirected
    def test_unlogged_user(self):
        response = self.client.get(reverse("accounts:my_account"))
        self.assertRedirects(response, "/accounts/login/")

    # test a user with firstname
    def test_logged_user(self):
        self.client.login(
            username=self.user.username, password=self.user_info["password"])
        response = self.client.get(reverse("accounts:my_account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    # test a user without first name
    def test_nofirstname_user(self):
        self.user.first_name = ""
        self.user.save()
        self.client.login(
            username=self.user.username, password=self.user_info["password"])
        response = self.client.get(reverse("accounts:my_account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anonyme")

class LoginTestCase(TestCase):
    def setUp(self):
        self.user_info = {
            "username": "test_user",
            "email": "user@test.com",
            "password": "test_user_password",
            "first_name": "Paul"}
        self.user = User.objects.create_user(**self.user_info)

    # test login page returns 200 if user is not logged
    def test_get_login_unlogged_user(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="login_form"')

    # test login page don't show the form to a logged user
    def test_get_login_logged_user(self):
        self.client.login(
            username=self.user.username,
            password=self.user_info["password"])
        response = self.client.get(reverse("accounts:login"))
        self.assertNotContains(response, 'id="login_form"')

    # test a valid user connexion and redirection
    def test_valid_login(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": self.user.username,
            "password": self.user_info["password"]})
        redirected_to_myaccount(self, response)

    # test a wrong username
    def test_wrong_username_when_logging(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "wrong_username",
            "password": self.user_info["password"]})
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # test a wrong password
    def test_wrong_password_when_logging(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": self.user.username,
            "password": "wrong_password"})
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # test a user can logout
    def test_logout(self):
        self.client.login(
            username=self.user.username,
            password=self.user_info["password"])
        response = self.client.get(reverse("index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.client.get(reverse("accounts:logout"))
        response = self.client.get(reverse("index"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
