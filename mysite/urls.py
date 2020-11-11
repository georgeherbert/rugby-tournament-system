from django.contrib import admin
from django.urls import path, include

from . import views

# Runs appropriate subroutine depending on URL path
urlpatterns = [
    path("", views.index, name = "index"),
    path("account/", include("account.urls")),
    path("tournament/", include("tournament.urls")),
    path("team/", include("team.urls")),
    path("admin/", admin.site.urls),
]
