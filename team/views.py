# render used to return HTML responses
# get_object_or_404 raises a 404 error if a record cannot be found
from django.shortcuts import render, get_object_or_404

# HttpResponseRedirect redirects the user to a specific URL
from django.http import HttpResponseRedirect

# reverse returns a URL path depending on its parameters
from django.urls import reverse

# Imports forms and database tables
from . import models, forms

# Imports database tables defined in tournament app
from tournament import models as tournamentModels

# Provides the user with information about a specific team
def team(request, pk):
    # Gets the appropriate team record from the database
    teamSelected = get_object_or_404(models.Team, pk = pk)
    # The user making the request
    user = models.User.objects.get(id = request.user.id)

    # If the user is trying to view a team they are a member of
    if teamSelected in user.getTeams():

        # Gets the membership record corresponding to the user being a member of the team
        membership = models.Membership.objects.get(user = user, team = teamSelected)
        # Holds whether the user is a team administrator
        isTeamAdministrator = membership.administrator

        # Every game the team has partaken in
        allGames = tournamentModels.Game.objects.none()
        allGames = allGames | tournamentModels.Game.objects.filter(team1 = teamSelected)
        allGames = allGames | tournamentModels.Game.objects.filter(team2 = teamSelected)

        # Won, drawn and lost is initially set to 0
        won = 0
        drawn = 0
        lost = 0

        # For each game the team has played
        for game in allGames:
            # If game was a draw
            if game.team1Score == game.team2Score:
                drawn += 1
            # If team is team1
            elif game.team1 == teamSelected:
                # If team1 won
                if game.team1Score > game.team2Score:
                    won += 1
                #If team1 lost
                else:
                    lost += 1
            # Must be team 2
            else:
                # If team2 won
                if game.team2Score > game.team1Score:
                    won += 1
                # If team2 lost
                else:
                    lost += 1

        # Returns the HTML page with team information
        return render(request, "team/team.html", {
            "team": teamSelected,
            "isTeamAdministrator": isTeamAdministrator,
            "games": allGames,
            "won": won,
            "drawn": drawn,
            "lost": lost
        })

# Provides the user with the list of teams they are a member of
def teamList(request):
    return render(request, "team/teamList.html")

# Provides the user with a form to create a team, then adds the new team to the database
def createTeam(request):
    # The form for creating a new team
    teamForm = forms.TeamForm()

    # If the user is making an HTML POST request
    if request.method == "POST":
        # Fill each field in the form with the response data so new team can be saved to database
        form = forms.TeamForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Save the new team to the database
            team = form.save()
            # The user that submitted the form
            user = models.User.objects.get(id = request.user.id)

            # Create a new membership record, making the user who created the new team a member of the team
            membership = models.Membership()
            membership.user = user
            membership.team = team
            membership.administrator = True
            membership.save()

            # Redirect the user to the URL of the new team they have created
            return HttpResponseRedirect(membership.team.get_absolute_url())

    # Returns the HTML page with the form to create a team
    return render(request, "team/createTeam.html", {
        "form": teamForm
    })

# Provides the user with a search form to request to join a team
def requestTeam(request):
    # The form for searching for teams
    form = forms.RequestSearchForm(request.POST or None)

    # Searched is initially assumed to be false so when webpage loads it doesn't attempt to display results
    searched = False
    # Empty list of matches to be added to
    allMatches = []

    # If the user is making an HTML POST request
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            # The user making the search
            user = models.User.objects.get(id = request.user.id)

            # The team being searched for is split into individual words
            team = form.cleaned_data.get("team")
            teamSplit = team.split(" ")

            # The words "Rugby", "RFC", "Club" and "Team" are removed as too many teams will match this
            teamSplitFiltered = [i for i in teamSplit if i != "RFC" and i != "Rugby" and i != "Club" and i != "Team"]

            # For each word that makes up the search
            for keyWord in teamSplitFiltered:
                # All matches that contain this word
                matches = models.Team.objects.filter(name__icontains = keyWord)
                # Each match is added to the search results providing the user it not already a member of the team and is not already requesting to join that team
                for match in matches:
                    if match not in allMatches and match not in user.getTeams() and match not in user.getRequests():
                        allMatches.append(match)

            # The webpage will now display these search results
            searched = True

    # Returns the HTML page with the search form and search results
    return render(request, "team/requestTeam.html", {
        "form": form,
        "searched": searched,
        "matches": allMatches
    })

# Adds the request to join a team to the database and redirects the user to the list of teams
def sendRequest(request, pk):
    # The team the user wishes to join
    teamSelected = get_object_or_404(models.Team, pk = pk)
    # The user making the request to join the team
    user = models.User.objects.get(id = request.user.id)

    # Record added to Request table with user and team as foreign keys
    models.Request.objects.create(team = teamSelected, user = user)

    # Redirects the user to the URL of the list of teams
    return HttpResponseRedirect(reverse("team:teamList"))

# A team administrator has accepted the request, so the user is made a member of the team
def requestTeamAccept(request, team_pk, request_pk):
    # The user trying to accept the request
    requester = models.User.objects.get(id = request.user.id)
    # The request record is retrieved from the database
    requestSelected = get_object_or_404(models.Request, pk = request_pk)

    # If the user is an administrator of the team that another user is trying to join
    if isRequesterAdministrator(requester, requestSelected.team) == True:
        team = requestSelected.team
        user = requestSelected.user

        # A record is created in the membership table, effectively adding the user to the team
        membership = models.Membership()
        membership.user = user
        membership.team = team
        # The user doesn't have team administrator status
        membership.administrator = False
        membership.save()

        # Now the user has been added, the request is deleted
        requestSelected.delete()

        # Redirects the team administrator back to the team info page
        return HttpResponseRedirect(requestSelected.team.get_absolute_url())

# A team administrator has rejected the request, so the request is deleted
def requestTeamReject(request, team_pk, request_pk):
    # The user trying to reject the request
    requester = models.User.objects.get(id = request.user.id)
    # The request record is retrieved from the database
    requestSelected = get_object_or_404(models.Request, pk = request_pk)

    # If the user is an administrator of the team that another user is trying to join
    if isRequesterAdministrator(requester, requestSelected.team) == True:
        team = requestSelected.team
        # The record is deleted from the database, effectively rejecting the request
        requestSelected.delete()

        # Redirects the team administator back to the team info page
        return HttpResponseRedirect(team.get_absolute_url())

# Removes the user from the team if a team administrator requests to remove them
def removeFromTeam(request, team_pk, membership_pk):
    # The user making the request
    requester = models.User.objects.get(id = request.user.id)
    # The membership record of the user the team administrator is requesting to remove
    membershipSelected = get_object_or_404(models.Membership, pk = membership_pk)

    # If the user making the request is a team administrator
    if isRequesterAdministrator(requester, membershipSelected.team) == True:
        # The membership record is deleted, effectively removing the user from the team
        membershipSelected.delete()

        # The team the team administrator is a member of
        teamSelected = get_object_or_404(models.Team, pk = team_pk)

        # Redirects the team administrator back to the team info page
        return HttpResponseRedirect(teamSelected.get_absolute_url())

# Promotes a user to team administraor status
def promoteToTeamAdmin(request, team_pk, membership_pk):
    # The user making the request
    requester = models.User.objects.get(id = request.user.id)
    # The membership record of the user that is being promoted to team administrator
    membershipSelected = get_object_or_404(models.Membership, pk = membership_pk)

    # If the user making the request is a team administrator of the correct team
    if isRequesterAdministrator(requester, membershipSelected.team) == True:
        # The administrator field in the membership record is set to true thus making the user a team administrator
        membershipSelected.administrator = True
        membershipSelected.save()

        # Redirects the team administrator back to the team info page
        return HttpResponseRedirect(membershipSelected.team.get_absolute_url())

# Demotes a user from team administrator status
def demoteFromTeamAdmin(request, team_pk, membership_pk):
    # The user making the request
    requester = models.User.objects.get(id = request.user.id)
    # The membership record of the user that is being demoted
    membershipSelected = get_object_or_404(models.Membership, pk = membership_pk)

    # If the user making the request is a team administator of the correct team
    if isRequesterAdministrator(requester, membershipSelected.team) == True:
        # The administrator field in the membership record is set to false thus removing the users team admin status
        membershipSelected.administrator = False
        membershipSelected.save()

        # Redirects the team administrator back to the team info page
        return HttpResponseRedirect(membershipSelected.team.get_absolute_url())

# Deletes the team
def deleteTeam(request, pk):
    # The user making the request
    requester = models.User.objects.get(id = request.user.id)
    # The team that is being deleted
    teamSelected = get_object_or_404(models.Team, pk = pk)

    # If the user making the request is a team administrator of the team being deleted
    if isRequesterAdministrator(requester, teamSelected) == True:
        # The team is deleted
        teamSelected.delete()

        # The user is redirected back to the list of teams they are a member of
        return HttpResponseRedirect(reverse("team:teamList"))

# Lets a user leave a team
def leaveTeam(request, pk):
    # The user attempting to leave the team
    user = models.User.objects.get(id = request.user.id)
    # The team the user is attempting to leave
    teamSelected = get_object_or_404(models.Team, pk = pk)

    # Deletes membership record which records the user as being a member of the team
    membershipSelected = models.Membership.objects.get(user = user, team = teamSelected)
    membershipSelected.delete()

    # Redirects te user back to the list of teams they are a member of
    return HttpResponseRedirect(reverse("team:teamList"))

# Accepts an invite to partake in a tournament
def acceptInvite(request, team_pk, invite_pk):
    # The user attempting to accept the invitation
    requester = models.User.objects.get(id = request.user.id)
    # The invite the user is attempting to accept
    invite = tournamentModels.Invite.objects.get(id = invite_pk)

    # If the user attempting to accept the invitation is a team administrator
    if isRequesterAdministrator(requester, invite.team) == True:

        # Enroll the team in the tournament
        enrollment = tournamentModels.Enrollment()
        enrollment.tournament = invite.tournament
        enrollment.team = invite.team
        enrollment.save()

        # Delete the invite
        invite.delete()

        # Redirect the user to the tournament they just accepted an invite to
        tournament = enrollment.tournament
        return HttpResponseRedirect(tournament.get_absolute_url())

# Rejects an invite to partake in a tournament
def rejectInvite(request, team_pk, invite_pk):
    # The user attempting to reject the invite
    requester = models.User.objects.get(id = request.user.id)
    # The invite record in the database the user is attempting to reject
    invite = tournamentModels.Invite.objects.get(id = invite_pk)

    # If the user attempting to reject the invite is a team administrator
    if isRequesterAdministrator(requester, invite.team) == True:
        team = invite.team
        # Delete the invite record from the database
        invite.delete()

        # Redirect the user to the team they rejected the invite on behalf of
        return HttpResponseRedirect(team.get_absolute_url())

# Determines whether a user is a team administator of a given team
def isRequesterAdministrator(user, teamSelected):
    # If the user is a member of the team
    if teamSelected in user.getTeams():
        # Membership record which links the user to the team
        userRelationship = models.Membership.objects.get(user = user, team = teamSelected)

        # If the user is an administrator return true
        if userRelationship.administrator == True:
            return True
        else:
            return False
    else:
        return False
