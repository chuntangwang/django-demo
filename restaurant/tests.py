from django.conf import settings
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
def test_db_location():
    # Prints the test DB path
    print(settings.DATABASES['default']['NAME'])


@pytest.mark.django_db
def test_admin_user():
    """
    Test if admin user is created successfully.
    """
    User.objects.create_superuser(
        username='admin', password='admin123456', email='admin@example.com'
    )
    user = User.objects.get(username='admin')
    assert user.is_superuser
