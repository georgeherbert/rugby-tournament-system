# forms allows forms to be created
from django import forms

# Allows database to be accessed and updated by forms
from . import models

# Form used to add tournaments to the database
class TournamentForm(forms.ModelForm):
    class Meta:
        # Form fields are every field in Tournament table
        model = models.Tournament
        # The labels for each field
        labels = {
            "name": "Tournament Name",
            "location": "Location",
            "pitches": "Number of Pitches",
            "halfDuration": "Duration of a Half",
            "halfTimeDuration": "Duration of Half-Time",
            "swapTeamsDuration": "Duration Between Games",
            "startDate": "Date",
            "startTime": "Start Time"
        }
        exclude = []

        widgets = {
            # Start date uses a date selection dropdown
            "startDate": forms.SelectDateWidget(),
            }

    # Determines whether the form is valid
    def clean(self):
        data = self.cleaned_data

        errors = {}

        # If the user has stated that there is less than one pitch raise an error
        if data.get("pitches") < 1:
            errors.update({"pitches": "You cannot have less than 1 pitch."})

        # If the user has stated that a half has negative time raise an error
        if data.get("halfDuration") < 0:
            errors.update({"halfDuration": "You cannot have a negative half duration."})

        # If the user has stated that half time has negative time raise an error
        if data.get("halfTimeDuration") < 0:
            errors.update({"halfTimeDuration": "You cannot have a negative half-time duration."})

        # If the user has stated that it takes negative time to swap teams raise an error
        if data.get("swapTeamsDuration") < 0:
            errors.update({"swapTeamsDuration": "You cannot have a negative duration between games."})

        # If there are errors
        if errors != {}:
            raise forms.ValidationError(errors)

        return data

# Form used to search for teams to invite
class InviteSearchForm(forms.Form):
    team = forms.CharField(label = "Team Name", max_length = 255)

# Form used to add game results to the database
class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        labels = {
            "team1Score": "",
            "team2Score": ""
        }
        # Only fields in the form are team1Score and team2Score
        exclude = ["team1", "team2", "startTime", "pitch"]

    # Determines whether the form is valid
    def clean(self):
        data = self.cleaned_data

        # If the user has actually entered scores
        if data.get("team1Score") is None or data.get("team2Score") is None:
            raise forms.ValidationError("")

        return data

# Enables the scores for multiple games to be entered at once
GameFormSet = forms.modelformset_factory(
    models.Game,
    form = GameForm,
    extra = 0,
)
