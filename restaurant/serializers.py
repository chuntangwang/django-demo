from restaurant.models import Restaurant, Review
from rest_framework import serializers


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['name', 'email']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'score', 'comment']
