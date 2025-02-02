from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # drf-spactacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # allow access static files of drf-spectacular-sidecar if settings.DEBUG is False
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    # restaurant api
    path('api/', include('restaurant.urls')),
]
