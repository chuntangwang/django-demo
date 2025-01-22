from django.db import models

# Create your models here.

class User(models.Model):
    pass

class Restaurant(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pass

class Review(models.Model):
    pass
