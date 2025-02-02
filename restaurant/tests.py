import pytest
from django.contrib.auth.models import User
from django.conf import settings


@pytest.mark.django_db
def test_db_location():
    # Prints the test DB path
    print(settings.DATABASES['default']['NAME'])


@pytest.mark.django_db
def test_my_user():
    User.objects.create_superuser(
        username='admin', password='adminpass', email='admin@example.com'
    )
    admin = User.objects.get(username='admin')
    assert admin.is_superuser
