from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """A Profile is attached at each User to store additionnal informations.
    fields:
    -user: The User at wich the Profile is attached
    -favories: All the products that the user has saved"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favories = models.ManyToManyField(
        'substitut_search.Product', through='substitut_search.Favory')

    def __str__(self):
        return self.user.username
