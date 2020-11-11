# path looks at URL path, and if there is a match runs the appropriate subroutine
from django.urls import path

# Imported to allow appropriate subroutine to be run
from . import views

# Allows other apps to access urls in account app
app_name = "team"

# Runs appropriate subroutine depending on URL path
urlpatterns = [
    path("", views.teamList, name = "teamList"),
    path("<int:pk>/", views.team, name = "team"),
    path("<int:team_pk>/request/<int:request_pk>/accept/", views.requestTeamAccept, name = "requestTeamAccept"),
    path("<int:team_pk>/request/<int:request_pk>/reject/", views.requestTeamReject, name = "requestTeamReject"),
    path("<int:team_pk>/member/<int:membership_pk>/remove/", views.removeFromTeam, name = "removeFromTeam"),
    path("<int:team_pk>/member/<int:membership_pk>/promote/", views.promoteToTeamAdmin, name = "promoteToTeamAdmin"),
    path("<int:team_pk>/member/<int:membership_pk>/demote/", views.demoteFromTeamAdmin, name = "demoteFromTeamAdmin"),
    path("<int:team_pk>/invite/<int:invite_pk>/accept/", views.acceptInvite, name = "acceptInvite"),
    path("<int:team_pk>/invite/<int:invite_pk>/reject/", views.rejectInvite, name = "rejectInvite"),
    path("<int:pk>/leave", views.leaveTeam, name = "leaveTeam"),
    path("<int:pk>/delete/", views.deleteTeam, name = "deleteTeam"),
    path("create/", views.createTeam, name = "createTeam"),
    path("request/", views.requestTeam, name = "requestTeam"),
    path("request/<int:pk>", views.sendRequest, name = "sendRequest")
]
