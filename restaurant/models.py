from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=250, db_index=True, unique=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='restaurants', on_delete=models.CASCADE
    )


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'user'],
                name='unique_review_per_user_per_restaurant',
            )
        ]
