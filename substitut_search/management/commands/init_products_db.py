from django.core.management.base import BaseCommand, CommandError

from substitut_search.utils.fill_db import FillDB
from substitut_search.models import Product

class Command(BaseCommand):
    """Add the command to init the database by dowloading
    the products on OpenFoodFacts.org"""
    help = 'Init the database by dowloading the products on OpenFoodFacts.org'

    def add_arguments(self, parser):
        """Add a positional argument
        n_products: the number of products to download"""
        parser.add_argument('n_products', type=int, default=1000)

    def handle(self, *args, **options):
        """-Delete all the products from the database.
        -Diplay the number of products deleted.
        -Download and insert the products in the database.
        -Display the number of products inserted."""
        old_count = Product.objects.count()
        Product.objects.all().delete()
        count = Product.objects.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted {old_count} products in the database'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'{count} products still in the database'))
        fill_db = FillDB(nb_products=options['n_products'])
        fill_db.insert_products()
        count = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully insered {count} products in the database'))