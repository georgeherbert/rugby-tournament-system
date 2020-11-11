# render used to return HTML responses
# get_object_or_404 raises a 404 error if a record cannot be found
from django.shortcuts import render, get_object_or_404

# HttpResponseRedirect redirects the user to a specific URL
# HttpResponse generates an HTTP response
from django.http import HttpResponseRedirect, HttpResponse

# reverse returns a URL path depending on its parameters
from django.shortcuts import reverse

# datetime allows dates to be stored in python
# timedelta enables dates to be updated by a certain number of days etc.
from datetime import datetime, timedelta

# Procedure that takes tournament details as its input and produces tournament options as its output
from utils.organise import main as organise

# High to low quicksort algorithm which takes values to be sorted and attribute to be sorted by in tuples as parameters
from utils.quickSort import quickSort

# Turns HTML into a PDF for a tournament
from utils.renderToPDF import renderToPDF

# Imports forms and database tables
from account import models as accountModels
from team import models as teamModels
from . import models
from . import forms

# Provides the user with information about a specific tournament
def tournament(request, pk):
    # The tournament the user is trying to get information on
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # numOfOrganisers is intiailly set to 0
    numOfOrganisers = 0

    # Empty list is created for organising teams to be added to
    organiserTeams = []

    # numOfOrganisers is calculated by looking at each enrollment for the tournament
    for enrollment in tournamentSelected.enrollment_set.all():
        if enrollment.organiser == True:
            numOfOrganisers += 1

    # The user making the request
    user = models.User.objects.get(id = request.user.id)

    # Stores whether the user is a tournament organiser
    userIsOrganiser = isOrganiser(user, tournamentSelected)

    # games holds the list of games taking place in the tournament
    games = models.Game.objects.none()
    for timeslot in tournamentSelected.timeslot_set.all():
        for pitch in timeslot.pitchinstance_set.all():
            games = games | pitch.game_set.all()

    # hasScores is initially assumed to be false
    hasScores = False

    # If a tournament layout has been chosen
    if len(games) > 0:
        # If there is a score for the first game there will be scores for all games
        if games[0].team1Score != None:
            # Therefore hasScores must be true
            hasScores = True

    # Returns the HTML page with tournament information
    return render(request, "tournament/tournament.html", {
        "tournament": tournamentSelected,
        "numOfOrganisers": numOfOrganisers,
        "userIsOrganiser": userIsOrganiser,
        "hasScores": hasScores
    })

# Provides the user with a list of tournaments their teams are competing in
def tournamentList(request):
    # The user making the request
    user = models.User.objects.get(id = request.user.id)
    # The tournaments the user is partaking in
    tournaments = user.getTournaments()

    # Empty lists for upcoming and past tournaments to be added to to separate them
    upcoming = []
    past = []

    # If the user has competed/is going to compete in tournaments
    if len(tournaments) != 0:
        # Each tournament is put in a sublist with its start time
        tournamentsWithTimestamps = [[(datetime.combine(tournament.startDate, datetime.min.time()).timestamp(), tournament)] for tournament in tournaments]

        # Sorts the tournaments most recent first
        mostRecentFirst = quickSort(tournamentsWithTimestamps)
        # Takes each tournament out of the tuple it is in with its start time
        tournamentsOrganised = [tournament[0][1] for tournament in mostRecentFirst]

        # The current date at midnight
        currentDate = datetime.now()
        currentDateMidnight = datetime(currentDate.year, currentDate.month, currentDate.day, 0, 0)

        for tournament in tournamentsOrganised:
            # If tournament is after start of current day add to upcoming
            if datetime.combine(tournament.startDate, datetime.min.time()) >= currentDateMidnight:
                upcoming.append(tournament)
            # Otherwise add to past
            else:
                past.append(tournament)

    # Returns the HTML page with list of tournaments
    return render(request, "tournament/tournamentList.html", {
        "tournamentsUpcoming": upcoming,
        "tournamentsPast": past
    })

# Search for teams to add to a tournament
def addTeamsToTournament(request, pk):
    # Searched is initially assumed to be false so web page doesn't attempt to load search results
    searched = False
    # Matches will be added to this list
    allMatches = []

    # The user searching
    user = models.User.objects.get(id = request.user.id)
    # The tournament the user is attempting to add teams to
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user is a tournament organiser and the layout hasn't already been decided
    if isOrganiser(user, tournamentSelected) == True and tournamentSelected.timeslot_set.count() == 0:

            # The search form
            inviteSearchForm = forms.InviteSearchForm()

            # If the request is an HTML POST request
            if request.method == "POST":
                # The search form with the search query
                form = forms.InviteSearchForm(request.POST)

                # If the form is valid
                if form.is_valid():

                    # Search query is split into its individual words and common terms such as RFC are removed
                    team = form.cleaned_data.get("team")
                    teamSplit = team.split(" ")
                    teamSplitFiltered = [i for i in teamSplit if i != "RFC" and i != "Rugby" and i != "Club" and i != "Team"]

                    # For each word in the query
                    for keyWord in teamSplitFiltered:
                        # Teams in the db which contain this word are retrieved
                        matches = models.Team.objects.filter(name__icontains = keyWord)
                        for match in matches:
                            # If the team is not already a match and not already invited/competing in the tournament it is added as a match
                            if match not in allMatches and match not in tournamentSelected.getTeamsInvited() and match not in tournamentSelected.getTeamsJoined():
                                allMatches.append(match)

                    # Searched is now set to true so search results will appear on the web page
                    searched = True

            # Returns the HTML page with the search field and search resutls
            return render(request, "tournament/addTeamsToTournament.html", {
                "tournament": tournamentSelected,
                "form": inviteSearchForm,
                "searched": searched,
                "matches": allMatches,
            })

# Adds an invitation to the database when a team is invited to join a tournament
def inviteTeam(request, tournament_pk, team_pk):
    # The user inviting the team
    user = models.User.objects.get(id = request.user.id)
    # The tournament the team is being inivted to
    tournamentSelected = get_object_or_404(models.Tournament, pk = tournament_pk)
    # The team being invited
    teamSelected = get_object_or_404(models.Team, pk = team_pk)

    # If the user inviting is a tournament organiser, and the team being invited is not already invited and not already competing
    if isOrganiser(user, tournamentSelected) == True and teamSelected not in tournamentSelected.getTeamsInvited() and teamSelected not in tournamentSelected.getTeamsJoined():
        # The invite is added to the database
        addInvite = models.Invite.objects.create(team = teamSelected, tournament = tournamentSelected)

        # Returns the HTML page with the search field and search results so more teams can be added
        return HttpResponseRedirect(reverse("tournament:addTeamsToTournament", args = [tournamentSelected.pk]))

# Removes an enrollment from the database so a team is no longer competing in a tournament
def removeTeamFromTournament(request, tournament_pk, enrollment_pk):
    # The user removing the team from the tournament
    user = models.User.objects.get(id = request.user.id)
    # The enrollment which is to be deleted
    enrollmentSelected = get_object_or_404(models.Enrollment, pk = enrollment_pk)

    # If the user is a tournament organiser and the layout hasn't already been decided
    if isOrganiser(user, enrollmentSelected.tournament) == True and enrollmentSelected.tournament.timeslot_set.count() == 0:
        # The enrollment is deleted from the database, removing the team from the tournament
        enrollmentSelected.delete()
        # Returns HTML page with tournament info
        return HttpResponseRedirect(enrollmentSelected.tournament.get_absolute_url())

# Removes an invitation from the database so a team is no longer invited to a tournament
def removeInvite(request, tournament_pk, invite_pk):
    # The user removing the invite
    user = models.User.objects.get(id = request.user.id)
    # The invite which is to be deleted
    inviteSelected = get_object_or_404(models.Invite, pk = invite_pk)

    # If the user is a tournament organiser
    if isOrganiser(user, inviteSelected.tournament) == True:
        # The invite is deleted from the database, uninviting the team
        inviteSelected.delete()

        # User is redirected to the invite teams search page to invite more teams if needed
        return HttpResponseRedirect(reverse("tournament:addTeamsToTournament", args = [inviteSelected.tournament.pk]))

# Provides a form used to create a tournament
def createTournament(request):
    # The user creating the tournament
    user = models.User.objects.get(id = request.user.id)
    # If the user is a member of at least one team
    if user.membership_set.count() != 0:
        # The form to create a tournament
        form = forms.TournamentForm(request.POST or None)

        # If the request is an HTML post request
        if request.method == "POST":

            # If the form is valid
            if form.is_valid():
                # The tournament is added to the database
                tournament = form.save()

                # Each team the user is a member of is automatically enrolled in the tournament
                memberships = teamModels.Membership.objects.filter(user = user)
                for membership in memberships:
                    if membership.administrator == True:
                        addOrganiser = models.Enrollment.objects.create(team = membership.team, tournament = tournament, organiser = True)

                # User is redirected to the tournament they just created
                return HttpResponseRedirect(tournament.get_absolute_url())

        # Returns the HTML page with the form used to create a tournament
        return render(request, "tournament/createTournament.html", {
            "form": form
        })

# Provides a form used to edit a tournament
def editTournament(request, pk):
    # The user editing the tournament
    user = models.User.objects.get(id = request.user.id)
    # The tournament being edited
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user attempting to edit the tournament is a tournament organiser and the layout hasn't yet been decided
    if isOrganiser(user, tournamentSelected) == True and tournamentSelected.timeslot_set.count() == 0:
        # The form with the tournament info already filled in
        form = forms.TournamentForm(request.POST or None, instance = tournamentSelected)

        # If the request is an HTML post request
        if request.method == "POST":

            # If the form is valid
            if form.is_valid():
                # Update the tournament info in the database
                tournament = form.save()

                # User is redirected to the tournament they just edited
                return HttpResponseRedirect(tournamentSelected.get_absolute_url())

        # Returns the HTML page with the form used to edit a tournament
        return render(request, "tournament/editTournament.html", {
            "form": form,
            "tournament": tournamentSelected
        })

# Removes a tournament from the database
def deleteTournament(request, pk):
    # The user attempting to delete the tournament
    user = models.User.objects.get(id = request.user.id)
    # The tournament the user is attempting to delete
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user is a tournament organiser the tournament is deleted from the database
    if isOrganiser(user, tournamentSelected) == True:
        tournamentSelected.delete()

        # User is redirected to the tournaments list
        return HttpResponseRedirect(reverse("tournament:tournamentList"))

# Adds the games for the appropriate tournament layout to the database
def chooseTournament(request, pk, num):
    # The user attempting to choose a layout
    user = models.User.objects.get(id = request.user.id)
    # The tournament a user is attempting to choose a layout for
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user is a tournament organiser
    if isOrganiser(user, tournamentSelected) == True:
        # The teams partaking in the tournament
        teams = [enrollment.team for enrollment in tournamentSelected.enrollment_set.all()]
        # All invites are deleted as teams cannot join tournament once layout is decided
        invites  = tournamentSelected.invite_set.all().delete()

        # Holds the list of potential tournament layouts
        tournaments = organise(teams, tournamentSelected.pitches, tournamentSelected.halfDuration, tournamentSelected.halfTimeDuration, tournamentSelected.swapTeamsDuration, tournamentSelected.startTime.hour, tournamentSelected.startTime.minute)

        # The layout the user selected
        tournament = tournaments[num - 1]

        # For each timeslot in the tournament
        for i in range(tournament.getNumOfTimeslots()):
            # The timeslot is added to the database
            timeslot = models.Timeslot(number = i + 1, tournament = tournamentSelected)
            timeslot.save()

            # For each pitch in the timeslot
            for j in range(tournament.timeslot(i).getNumOfPitches()):
                # The pitch is added to the database
                pitch = models.PitchInstance(name = j + 1, timeslot = timeslot)
                pitch.save()

                # For each game on the pitch
                for k in range(tournament.timeslot(i).pitch(j).getNumOfGames()):
                    # The teams in the game
                    (team1, team2) = tournament.timeslot(i).pitch(j).game(k).getGame()

                    # If either team is a bye team it is assigned the BYE team record in the team database
                    if team1 == "BYE":
                        team1 = teamModels.Team.objects.get(id = 1)
                    elif team2 == "BYE":
                        team2 = teamModels.Team.objects.get(id = 1)

                    # Tne game is added to the database
                    game = models.Game(team1 = team1, team2 = team2, startTime = tournament.timeslot(i).pitch(j).game(k).getStartTime(), pitch = pitch)
                    game.save()

        # Returns the URL of the HTML page with tournament info
        return HttpResponseRedirect(tournamentSelected.get_absolute_url())

# Enables user to select a new tournament layout
def changeLayout(request, pk):
    # The user attempting to change the layout
    user = models.User.objects.get(id = request.user.id)
    # The tournament the user is attempting to change the layout of
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user is an organiser
    if isOrganiser(user, tournamentSelected) == True:
        # Delete each timeslot in the tournament - will also delete every pitch and game
        for timeslot in tournamentSelected.timeslot_set.all():
            timeslot.delete()

        # Returns the URL of the HTML page with tournament info
        return HttpResponseRedirect(tournamentSelected.get_absolute_url())

# Enables the user to view the tournament layout as a PDF to print
def exportAsPDF(request, pk):
    # The tournament the user is attempting to view as a PDF
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the tournament layout has been chosen
    if tournamentSelected.timeslot_set.count() != 0:
        # Makes the tournament layout a PDF format
        pdf = renderToPDF(tournamentSelected)
        # Returns a pdf file to view in web browser
        return HttpResponse(pdf, content_type='application/pdf')

# Provides the user with a form to add results and adds these results to the database
def addResults(request, pk):
    # The user attempting to add the results
    user = models.User.objects.get(id = request.user.id)
    # The tournament the user is attempting to add the results to
    tournamentSelected = get_object_or_404(models.Tournament, pk = pk)

    # If the user is a tournament organiser
    if isOrganiser(user, tournamentSelected) == True:
        # games holds each game taking place in the tournament
        games = models.Game.objects.none()
        for timeslot in tournamentSelected.timeslot_set.all():
            for pitch in timeslot.pitchinstance_set.all():
                games = games | pitch.game_set.all()

        # Holds teams partaking in the tourname in order they appear in games
        teamsInGamesOrder = []
        for game in games:
            teamsInGamesOrder.append([game.team1, game.team2])

        # The form that scores will be inputted to
        gameFormSet = forms.GameFormSet(queryset = games)

        # If the request is an HTML POST request
        if request.method == "POST":
            # Form with fields filled in with new inputs
            form = forms.GameFormSet(request.POST)

            # If the form is valid
            if form.is_valid():
                # Save the updated scores to the database
                form.save()

                # Return the URL of the HTML page with tournament info
                return HttpResponseRedirect(tournamentSelected.get_absolute_url())

        # Returns the HTML page with the form to input scores
        return render(request, "tournament/addResults.html", {
            "tournament": tournamentSelected,
            "gamesWithFormset": zip(list(teamsInGamesOrder), gameFormSet),
            "formset": gameFormSet
        })

# Determines whether a user is a tournament organiser and therefore has permission to perform certain tasks
def isOrganiser(user, tournamentSelected):
    # Will hold the teams the user is an organiser of
    organiserTeams = []

    # For each enrollment the user has in the database
    for enrollment in tournamentSelected.enrollment_set.all():
        # If the user is set as an organiser of that enrollment add the team to the organiserTeams list
        if enrollment.organiser == True:
            organiserTeams.append(enrollment.team.pk)

    # userIsOrganiser is initially assumed to be false
    userIsOrganiser = False

    # For each team the user is a member of, if that team is an organiser team and the user is a team administator of that team, then they are an organiser
    for membership in user.membership_set.all():
        if membership.administrator == True:
            if membership.team.pk in organiserTeams:
                userIsOrganiser = True

    return userIsOrganiser
