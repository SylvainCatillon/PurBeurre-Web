from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import tag

from selenium import webdriver

from .utils import log_user_in


class TestLoginSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    #  test the login
    @tag('selenium')
    def test_login(self):
        log_user_in(self.selenium, self.live_server_url)
        my_account = self.live_server_url+reverse("accounts:my_account")
        self.assertURLEqual(my_account, self.selenium.current_url)
