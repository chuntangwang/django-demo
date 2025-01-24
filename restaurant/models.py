from django.db import models
from django.conf import settings
from django.contrib.auth .models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRE_FIELDS = ['username']

class Restaurant(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='restaurants',
        on_delete=models.CASCADE
    )


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.IntegerField()
    comment = models.TextField(blank=True)
