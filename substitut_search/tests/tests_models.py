from django.test import TestCase

from ..models import Product, Favory
from accounts.tests.tests_models import create_user


def create_product():
    """Create a product for testing purpose"""
    product_info = {
        "code": "2159404",
        "nutriscore": "a",
        "categories": ["en:test"],
        "name": "test1",
        "image": "https//image_test.com",
        "link": "https//test.com",
        "nutrient_levels": [
            'Matières grasses en quantitée faible (0g)',
            'Acides gras saturés en quantitée faible (0g)',
            'Sucres en quantitée faible (0g)',
            'Sel en quantitée faible (0.02794g)']
        }
    return Product.objects.create(**product_info)


class ModelsCreation(TestCase):
    """Test the models Product and Favory"""

    def test_product_creation(self):
        """Test if a product is created"""
        product = create_product()
        self.assertIsInstance(product, Product)
        self.assertEqual(product.__str__(), product.name)

    def test_favory_creation(self):
        """Test if a favory is created, with 'Divers' as tag"""
        product = create_product()
        user = create_user()
        user.profile.favories.add(product)
        favory = Favory.objects.get(user_profile=user.profile)
        self.assertIsInstance(favory, Favory)
        self.assertEqual(favory.tag, "Non classé")
