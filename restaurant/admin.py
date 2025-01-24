from django.contrib import admin
from .models import User

class UserAdminSite(admin.AdminSite):
    site_header = 'Restaurant users administration'

user_admin = UserAdminSite(name='user_admin')
user_admin.register(User)
