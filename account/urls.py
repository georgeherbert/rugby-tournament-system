# path looks at URL path, and if there is a match runs the appropriate subroutine
from django.urls import path

# Imported to allow appropriate subroutine to be run
from . import views

# Allows other apps to access urls in account app
app_name = "account"

# Runs appropriate subroutine depending on URL path
urlpatterns = [
    path("", views.account, name = "account"),
    path("login/", views.logIn, name = "logIn"),
    path("logout/", views.logOut, name = "logOut"),
    path("signup/", views.signUp, name = "signUp"),
    path("changePassword", views.changePassword, name = "changePassword")
]
