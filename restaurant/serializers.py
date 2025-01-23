from restaurant.models import Restaurant, Review
from rest_framework import serializers
from django.contrib.auth.models import User


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['name', 'email']


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    # restaurant = serializers.SlugRelatedField(queryset=Restaurant.objects, slug_field='name')
    user = serializers.SerializerMethodField()
    score = serializers.ChoiceField([1, 2, 3, 4, 5])

    def get_user(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return request.user.username
        return None

    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'score', 'comment']
