from django.contrib import admin
from .models import User, Tenant

admin.site.register(User)
admin.site.register(Tenant)