from django.urls import path, include
from rest_framework.routers import SimpleRouter
import restaurant.views as views

app_name = 'restaurant'

router = SimpleRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auth-token/', views.AuthTokenView.as_view(), name='auth-token'),
    path('', include(router.urls)),
]
