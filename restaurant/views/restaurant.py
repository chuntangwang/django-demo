from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Avg
from restaurant.models import Restaurant, Review
from restaurant import serializers
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiExample,
)


@extend_schema(tags=['Restaurant'])
@extend_schema_view(
    list=extend_schema(
        description='List all restaurants with descending order of average score.'
    ),
    retrieve=extend_schema(description='Retrieve a restaurant.'),
    create=extend_schema(description='Create a restaurant.'),
    update=extend_schema(description='Update a restaurant.'),
    partial_update=extend_schema(description='Partial update a restaurant.'),
    destroy=extend_schema(description='Delete a restaurant.'),
)
class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    # TODO: using task queue or stored procedure to update resturant__avg_score in db.
    def get_queryset(self):
        return Restaurant.objects.annotate(
            avg_score=Avg('review__score', default=0)
        ).order_by('-avg_score')


@extend_schema(tags=['Review'])
@extend_schema_view(
    list=extend_schema(
        description='List all reviews.',
        parameters=[
            OpenApiParameter(
                name='restaurant',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by restaurant id.',
            ),
            OpenApiParameter(
                name='user',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by user id.',
            ),
            OpenApiParameter(
                name='user__username',
                type=OpenApiTypes.STR,
                description='Filter by user.username.',
            ),
        ],
    ),
    retrieve=extend_schema(description='Retrieve a review.'),
    create=extend_schema(
        description='Create a review, same user can only create a review in same restaurant.',
        examples=[
            OpenApiExample(
                'Request Example',
                description='`restaurant_id`: should greater than or equal to 1, `score`: Integers of [1, 2, 3, 4, 5]',
                value={
                    'restaurant_id': 1,
                    'score': 5,
                    'comment': '5 stars',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Response Example',
                value={
                    'restaurant': {
                        'id': 1,
                        'creator': 'user',
                        'avg_score': 5,
                        'name': 'Costco',
                        'description': 'A shopping mall',
                    },
                    'user': {
                        'username': 'user',
                        'email': 'user@example.com',
                    },
                    'score': 1,
                    'comment': '5 stars',
                    'date_created': '2025-02-02T17:37:03.560Z',
                },
                response_only=True,
            ),
        ],
    ),
    update=extend_schema(description='Update a review.'),
    partial_update=extend_schema(description='Partial update a review.'),
    destroy=extend_schema(description='Delete a review.'),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'restaurant': ['exact'],
        'user': ['exact'],
        'user__username': ['exact'],
    }
