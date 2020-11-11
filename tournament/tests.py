from django.test import TestCase

from . import models
from team import models as teamModels

class InviteTestCase(TestCase):
    def setUp(self):
        self.tournament = models.Tournament.objects.create(
            name = "Test Tournament",
            location = "Test Location",
            pitches = 1,
            halfDuration = 40,
            halfTimeDuration = 10,
            swapTeamsDuration = 10,
            startDate = "2021-01-01",
            startTime = "00:00",
        )
        self.team = teamModels.Team.objects.create(name = "Test Team")
        self.invite = models.Invite.objects.create(tournament = self.tournament, team = self.team)

    def test_tournament_assignment(self):
        self.assertEqual(self.invite.tournament, self.tournament)

    def test_team_assignment(self):
        self.assertEqual(self.invite.team, self.team)

    def test_string_representation(self):
        self.assertEqual(str(self.invite), "Test Team is invited to Test Tournament")
