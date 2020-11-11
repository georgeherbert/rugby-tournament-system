from django.contrib import admin

# Register your models here.

from . import models
admin.site.register(models.User)
from django.contrib.auth.models import Group
admin.site.unregister(Group)
