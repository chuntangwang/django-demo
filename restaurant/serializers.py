from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Restaurant, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class RestaurantSerializer(serializers.ModelSerializer):
    # get restaurant, show username, not PK
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    avg_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    # create restaurant by session user
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['creator'] = request.user
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    score = serializers.ChoiceField([1, 2, 3, 4, 5])

    class Meta:
        model = Review
        fields = [
            'restaurant_id',
            'restaurant',
            'user',
            'score',
            'comment',
            'date_created',
        ]
        # drf-spectacular does not support depth
        # depth = 1

    # create review by session user and restaurant_id
    def create(self, validated_data):
        request = self.context.get('request')
        restaurant_id = validated_data.pop('restaurant_id')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        validated_data['restaurant'] = restaurant
        validated_data['user'] = request.user
        return super().create(validated_data)
