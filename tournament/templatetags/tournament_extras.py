# Allows custom filters and tags to be used in my app
from django import template
register = template.Library()

# Procedure that takes tournament details as its input and produces tournament options as its output
from utils.organise import main as organise

# Returns HTML containing list of tournament options
@register.inclusion_tag('tournament/displayTournaments.html')
def displayTournaments(tournament, userIsOrganiser, tournament_pk):
    # Teams partaking in the tournament
    teams = [enrollment.team for enrollment in tournament.enrollment_set.all()]

    # The possible options for the tournament
    tournaments = organise(teams, tournament.pitches, tournament.halfDuration, tournament.halfTimeDuration, tournament.swapTeamsDuration, tournament.startTime.hour, tournament.startTime.minute)

    # Will hold all of possible tournament options in nested loops as opposed to objects
    tournamentList = []

    # Will hold information about each tournament option
    tournamentsInfo = []

    # For each potential tournament
    for i in range(len(tournaments)):
        # Add an empty list to the list of tournaments
        tournamentList.append([])

        # Calculate the duration of the tournament in hours and minutes
        tournamentDuration = tournaments[i].getDuration().seconds
        tournamentHours = tournamentDuration // 3600
        tournamentMinutes = int((tournamentDuration % 3600) / 60)

        # Append the tournament duration in hours and mins, as well as the number of bye games and non-bye games to tournamentInfo list
        tournamentsInfo.append([[tournamentHours, tournamentMinutes], tournaments[i].getNumOfNonByeGames(), tournaments[i].getNumOfByeGames()])

        # For each timeslot
        for j in range(tournaments[i].getNumOfTimeslots()):
            tournamentList[i].append([])

            # For each pitch
            for k in range(tournaments[i].timeslot(j).getNumOfPitches()):
                tournamentList[i][j].append([])

                # For each game
                for l in range(tournaments[i].timeslot(j).pitch(k).getNumOfGames()):
                    # Add the game start time and teams playing to the nested list
                    tournamentList[i][j][k].append([tournaments[i].timeslot(j).pitch(k).game(l).getStartTime().strftime("%H:%M"), tournaments[i].timeslot(j).pitch(k).game(l).getGame()])

    return {"tournaments": zip(tournamentList, tournamentsInfo),
            "userIsOrganiser": userIsOrganiser,
            "tournament_pk": tournament_pk
            }
