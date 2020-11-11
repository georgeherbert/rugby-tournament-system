from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Tournament)
admin.site.register(models.Enrollment)
admin.site.register(models.Timeslot)
admin.site.register(models.PitchInstance)
admin.site.register(models.Game)
admin.site.register(models.Invite)
