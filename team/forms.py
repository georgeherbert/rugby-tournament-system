# forms allows forms to be created
from django import forms

# Allows database to be accessed and updated by forms
from . import models

# Form used to add teams to database
class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        exclude = []

# Form used to search for teams to request to join
class RequestSearchForm(forms.Form):
    # Team name field
    team = forms.CharField(label = "Team Name", max_length = 255)
