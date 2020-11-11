# models allows use of API to access database
from django.db import models

# reverse returns a URL path depending on its parameters
from django.urls import reverse

# Enables records from tables in team app to be used as foreign keys
from team.models import Team, Membership

# Gets the user table being used by my project as defined in settings.py
# Enables me to easily change the user table being used by my project without having to change lots of my code
from django.contrib.auth import get_user_model
User = get_user_model()

# Tournament table in database
class Tournament(models.Model):
    # Fields for the table
    name = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    pitches = models.IntegerField()
    halfDuration = models.IntegerField()
    halfTimeDuration = models.IntegerField()
    swapTeamsDuration = models.IntegerField()
    startDate = models.DateField()
    startTime = models.TimeField()

    def __str__(self):
        return self.name

    # Returns the URL of the tournament
    def get_absolute_url(self):
        return reverse("tournament:tournament", kwargs = {
            "pk": self.id
        })

    # Returns the teams invited to the tournament
    def getTeamsInvited(self):
        return [invite.team for invite in self.invite_set.all()]

    # Returns the teams currently enrolled in the tournament
    def getTeamsJoined(self):
        return [enrollment.team for enrollment in self.enrollment_set.all()]

# Enrollment table in database
class Enrollment(models.Model):
    # Fields for the table
    tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    organiser = models.BooleanField(default = False)

    def __str__(self):
        return "{} is enrolled in {}".format(self.team.name, self.tournament.name)

# Invite table in database
class Invite(models.Model):
    # Fields for the table
    tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)

    def __str__(self):
        return "{} is invited to {}".format(self.team.name, self.tournament.name)

# Invite table in database
class Timeslot(models.Model):
    # Fields in the table
    number = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)

    def __str__(self):
        return "Timeslot {}".format(self.number)

class PitchInstance(models.Model):
    name = models.CharField(max_length = 255)
    timeslot = models.ForeignKey(Timeslot, on_delete = models.CASCADE)

    def __str__(self):
        return "Pitch {}".format(self.name)

class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name = "team1", on_delete = models.CASCADE)
    team2 = models.ForeignKey(Team, related_name = "team2", on_delete = models.CASCADE)
    team1Score = models.IntegerField(null = True)
    team2Score = models.IntegerField(null = True)
    startTime = models.TimeField()
    pitch = models.ForeignKey(PitchInstance, on_delete = models.CASCADE)

    def __str__(self):
        return "{}: {} vs {} ({})".format(self.startTime, self.team1, self.team2, self.pitch)
