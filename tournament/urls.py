# path looks at URL path, and if there is a match runs the appropriate subroutine
from django.urls import path

# Imported to allow appropriate subroutine to be run
from . import views

# Allows other apps to access urls in tournament app
app_name = "tournament"

# Runs appropriate subroutine depending on URL path
urlpatterns = [
    path("", views.tournamentList, name = "tournamentList"),
    path("create/", views.createTournament, name = "createTournament"),
    path("<int:pk>/", views.tournament, name = "tournament"),
    path("<int:pk>/edit/", views.editTournament, name = "editTournament"),
    path("<int:pk>/delete/", views.deleteTournament, name = "deleteTournament"),
    path("<int:pk>/add/", views.addTeamsToTournament, name = "addTeamsToTournament"),
    path("<int:pk>/addresults/", views.addResults, name = "addResults"),
    path("<int:tournament_pk>/invite/<int:team_pk>/", views.inviteTeam, name = "inviteTeam"),
    path("<int:tournament_pk>/remove/<int:enrollment_pk>/", views.removeTeamFromTournament, name = "removeTeamFromTournament"),
    path("<int:tournament_pk>/uninvite/<int:invite_pk>/", views.removeInvite, name = "removeInvite"),
    path("<int:pk>/choose/<int:num>/", views.chooseTournament, name = "chooseTournament"),
    path("<int:pk>/change/", views.changeLayout, name = "changeLayout"),
    path("<int:pk>/export/", views.exportAsPDF, name = "exportAsPDF")
]
