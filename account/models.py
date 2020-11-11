# models allows use of API to access database
from django.db import models

# AbstractBaseUser allows creation of a custom user table
# BaseUserManager allows custom commands to be created for custom user table
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Sets password for user to encrypted version of password
from django.contrib.auth.hashers import make_password

# Functions which can be run to manually create users
class UserManager(BaseUserManager):
    # Create user with normal status
    def create_user(self, email, first_name, last_name, password = None, is_admin = False):
        # If no email, password, first name or last name is provided raise an error
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        # If not create a user
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        # Users password is set to encrypted version of password provided
        user.password = make_password(password)
        user.admin = is_admin
        # New user is added to database
        user.save(using = self._db)

        return user

    # Create user with administrative priviliges
    def create_superuser(self, email, first_name, last_name, password = None):
        user = self.create_user(email, first_name, last_name, password = password, is_admin = True)
        return user

# User table in database
class User(AbstractBaseUser):
    # User table has the following fields
    email = models.EmailField(unique = True, max_length = 255)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    admin = models.BooleanField(default = False)

    # The username for the user is their email
    USERNAME_FIELD = "email"

    # When a user is created, the first name and last name are required as well as the email
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    # Returns the users full name
    def getFullName(self):
        return "{} {}".format(self.first_name, self.last_name)

    # Required for django
    def has_perm(self, perm, obj = None):
        return True

    # Required for django
    def has_module_perms(self, app_label):
        return True

    # Returns the teams the user belongs to
    def getTeams(self):
        return [membership.team for membership in self.membership_set.all()]

    def getRequests(self):
        return [request.team for request in self.request_set.all()]

    # Returns the teams the user has requested to join
    def getTournaments(self):
        tournaments = []

        for team in self.getTeams():
            for enrollment in team.enrollment_set.all():
                if enrollment.tournament not in tournaments:
                    tournaments.append(enrollment.tournament)

        return tournaments

    # Returns whether the user is an admin or not as there is no separate staff
    @property
    def is_staff(self):
        return self.admin

    # Returns whether the user is an admin or not
    @property
    def is_admin(self):
        return self.admin

# Custom backend
class MyBackend:
    # Authenticate function returns the user if the usernamd and password are correct
    def authenticate(self, request, username = None, password = None):
        try:
            # Gets the user record corresponding to the user with the email provided
            user = User.objects.get(email = username)

            # Checks the password entered to log in is the user's password
            if user.check_password(password):
                return user
            else:
                return None
        except:
            return None

    # Required for django
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
