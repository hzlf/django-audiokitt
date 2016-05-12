from authtools.admin import StrippedUserAdmin
from django.contrib import admin

from .models import User

admin.site.register(User, StrippedUserAdmin)
