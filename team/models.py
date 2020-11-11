# models allows use of API to access database
from django.db import models

# reverse returns a URL path depending on its parameters
from django.urls import reverse

# Gets the user table being used by my project as defined in settings.py
# Enables me to easily change the user table being used by my project without having to change lots of my code
from django.contrib.auth import get_user_model
User = get_user_model()

# Team table in database
class Team(models.Model):
    # Has a field to store the team name
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

    # Returns the URL for the team record the function is being run for
    def get_absolute_url(self):
        return reverse("team:team", kwargs = {
            "pk": self.id
        })

# Membership table in database
class Membership(models.Model):
    # Has a user field and a team field as its foreign keys, enabling a user to be a member of multiple teams
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    # States whether the user is a team administrator or not
    administrator = models.BooleanField(default = False)

    def __str__(self):
        return "{} is a member of {}".format(self.user.getFullName(), self.team.name)

# Request table in database
class Request(models.Model):
    # Has a user field and a team field as its foreign keys, enabling a user to request to join multiple teams
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)

    def __str__(self):
        return "{} is requesting to join {}".format(self.user.getFullName(), self.team.name)
