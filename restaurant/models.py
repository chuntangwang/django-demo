from django.db import models
from django.conf import settings

# Create your models here.


# class User(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()


class Restaurant(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restaurants', on_delete=models.CASCADE)


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews' , on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True)
