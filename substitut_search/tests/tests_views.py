from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Product, Favory
from ..views import NB_DISPLAYED_PRODUCTS


class TestSearchProduct(TestCase):
    fixtures = ['19products']

    # test search a product by name
    def test_find_a_product(self):
        response = self.client.get(
            f"{reverse('substitut:search')}?query=test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["products"]),
            len(Product.objects.filter(name__icontains='test')))

    # test search empty query
    def test_empty_query(self):
        response = self.client.get(
            f"{reverse('substitut:search')}?query=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["products"]),
            min(len(Product.objects.all()), NB_DISPLAYED_PRODUCTS))

    # test if the substituts have a better nutriscore and share a category
    def test_find_a_substitut(self):
        product = Product.objects \
                        .filter(categories__contains=["en:biscuits"]) \
                        .filter(nutriscore="d")[0]
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={product.pk}")
        for substitut in response.context['products']:
            self.assertLess(substitut.nutriscore, product.nutriscore)
            for category in substitut.categories:
                if category in product.categories:
                    break
            else:
                self.fail("A substitut doesn't share any"
                          " category with the initial product")


class TestProductPage(TestCase):
    fixtures = ['2products']

    # test product page contains the required informations
    def test_product_page(self):
        product = Product.objects.all()[0]
        product_pk = product.pk
        response = self.client.get(
            f"{reverse('substitut:detail')}?product_id={product_pk}")
        self.assertContains(response, product.name)
        self.assertContains(response, product.nutriscore)
        self.assertContains(response, product.link)
        for level in product.nutrient_levels:
            self.assertContains(response, level)


class TestFavories(TestCase):
    fixtures = ['2products']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_info = {
            "username": "test_user",
            "email": "user@test.com",
            "password": "test_user_password",
            "first_name": "Paul"}
        cls.user = User.objects.create_user(**cls.user_info)
        cls.product = Product.objects.all()[0]

    def setUp(self):
        self.client.login(
            username=self.user.username, password=self.user_info["password"])

    # test a favory is saved
    def test_save_favory(self):
        response = self.client.post(
            reverse("substitut:favories"), {"product_id": self.product.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, self.user.profile.favories.all())

    # test a favory is saved with the good tag
    def test_save_favory_with_tag(self):
        tag = "Test"
        response = self.client.post(
            reverse("substitut:favories"),
            {"product_id": self.product.pk, "fav_tag": tag})
        self.assertEqual(response.status_code, 200)
        favory = Favory.objects.get(user_profile=self.user.profile)
        self.assertEqual(favory.product, self.product)
        self.assertEqual(favory.tag, tag)

    def test_default_tag_in_find_context(self):
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={self.product.pk}")
        self.assertEqual(
            response.context["fav_tags"],
            ["Non classé"])

    def test_tags_in_find_context(self):
        Favory.objects.create(
            user_profile=self.user.profile,
            product=self.product,
            tag="A Test")
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={self.product.pk}")
        self.assertEqual(
            response.context["fav_tags"],
            ["A Test", "Non classé"])

    # test a user can see his favories
    def test_see_favories(self):
        Favory.objects.create(
            user_profile=self.user.profile,
            product=self.product,
            tag="Test")
        product2 = Product.objects.all()[1]
        Favory.objects.create(
            user_profile=self.user.profile,
            product=product2,
            tag="Test")
        response = self.client.get(reverse("substitut:favories"))
        self.assertEqual(
            response.context['fav_dict']['Test'], [self.product, product2])

    # test an unlogged user can't see his favories
    def test_see_favories_unlogged_user(self):
        self.client.logout()
        response = self.client.get(reverse("substitut:favories"))
        self.assertTemplateUsed(
            response, "substitut_search/favories_unlogged.html")
