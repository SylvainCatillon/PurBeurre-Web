from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import tag

from selenium import webdriver

from accounts.tests.utils import log_user_in

from ..models import Product, Favory


class TestFavoriesSelenium(StaticLiveServerTestCase):
    fixtures = ['19products']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = log_user_in(self.selenium, self.live_server_url)

    @tag('selenium')
    def test_save(self):
        """Test if a product can be saved with and without a tag"""
        product = Product.objects \
                         .filter(categories__contains=["en:biscuits"]) \
                         .filter(nutriscore="d")[0]
        # assert that the user has no favories saved
        self.assertEqual(len(self.user.profile.favories.all()), 0)
        # save a favory without specifing a tag
        find_url = f"{reverse('substitut:find')}?product_id={product.pk}"
        self.selenium.get(self.live_server_url+find_url)
        self.selenium.find_elements_by_class_name("dropdownButton")[0].click()
        self.selenium.find_elements_by_class_name("save_submit")[0].click()
        # assert that the user has one favory saved, with the default tag
        self.assertEqual(len(self.user.profile.favories.all()), 1)
        self.assertEqual(Favory.objects.all()[0].tag, "Non classé")
        # save a favory with a specified tag
        self.selenium.find_elements_by_class_name("dropdownButton")[1].click()
        self.selenium.find_elements_by_name("fav_tag")[1].send_keys("Test")
        self.selenium.find_elements_by_class_name("save_submit")[1].click()
        # assert that the user has a second favory saved, with the choosen tag
        self.assertEqual(len(self.user.profile.favories.all()), 2)
        self.assertEqual(Favory.objects.all()[1].tag, "Test")

    @tag('selenium')
    def test_see_favories(self):
        """Test if a favory saved with a tag can be seen"""
        product = Product.objects.all()[0]
        Favory.objects.create(
            user_profile=self.user.profile, product=product, tag="Test")
        self.selenium.get(self.live_server_url+reverse('substitut:favories'))
        self.selenium.find_element_by_xpath("//button[@value='Test']").click()
        favory = self.selenium.find_element_by_class_name("card-title")
        self.assertEqual(favory.text, product.name)
        self.assertTrue(favory.is_displayed())
