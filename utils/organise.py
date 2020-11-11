# datetime allows dates to be stored in python
# timedelta enables dates to be updated by a certain number of days etc.
from datetime import datetime, timedelta

class Queue():
    def __init__(self, aList):
        self.queue = aList

    def deQueue(self):
        return self.queue.pop(0)

class Tournament:
    def __init__(self):
        self.timeslots = []
        self.duration = 0

    # Returns specified timeslot object
    def timeslot(self, timeslot):
        return self.timeslots[timeslot]

    # Adds a timeslot to a tournament with a specific number of pitches
    def addTimeslot(self, numOfPitches):
        self.timeslots.append(Timeslot(numOfPitches))

    # Returns the number of timeslots
    def getNumOfTimeslots(self):
        return len(self.timeslots)

    # Calculates the duration of the tournament once all games have been added
    def calculateDuration(self, gameDuration):
        tournamentStart = self.timeslot(0).pitch(0).game(0).getStartTime()
        tournamentEnd = self.timeslot(self.getNumOfTimeslots() - 1).pitch(0).game(self.timeslot(self.getNumOfTimeslots() - 1).pitch(0).getNumOfGames() - 1).getStartTime()

        # The duration of the tournament is the difference between the start of the first game and the start of the last game, plus the duration of the last game
        self.duration = tournamentEnd - tournamentStart + gameDuration

    # Returns the duration of the tournament
    def getDuration(self):
        return self.duration

    # Returns the number of bye games in the tournament
    def getNumOfByeGames(self):
        total = 0

        # The number of bye games in the tournament is the total number of bye games in each timeslot
        for timeslot in self.timeslots:
            total += timeslot.getNumOfByeGames()

        return total

    # Returns the number of non bye games in the tournament
    def getNumOfNonByeGames(self):
        total = 0

        # The number of non-bye games in the tournament is the total number of non-bye games in each timeslot
        for timeslot in self.timeslots:
            total += timeslot.getNumOfNonByeGames()

        return total

class Timeslot:
    def __init__(self, numOfPitches):
        self.pitches = [Pitch() for i in range(numOfPitches)]

    # Returns specified pitch object
    def pitch(self, pitch):
        return self.pitches[pitch]

    # Adds a pitch to a timeslot
    def addPitch(self):
        self.pitches.append(Pitch())

    # Returns the number of pitches used within the timeslot
    def getNumOfPitches(self):
        return len(self.pitches)

    # Returns the  number of bye games within the timeslot
    def getNumOfByeGames(self):
        total = 0

        # The number of bye games in the timeslot is the total number of bye games on each pitch
        for pitch in self.pitches:
            total += pitch.getNumOfByeGames()

        return total

    # Returns the number of non bye games within the timeslot
    def getNumOfNonByeGames(self):
        total = 0

        # The number of non-bye games in the timeslot is the total number of non-bye games on each pitcn
        for pitch in self.pitches:
            total += pitch.getNumOfNonByeGames()

        return total

class Pitch:
    def __init__(self):
        self.teams = []
        self.games = []
        self.hasBye = False

    # Returns specified pitch object
    def team(self, team):
        return self.teams[team]

    # Adds a team to the pitch
    def addTeam(self, name):
        self.teams.append(Team(name, False))

    # Adds a bye team to the pitch
    def addByeTeam(self):
        self.teams.append(Team("BYE", True))

    # Returns the number of teams playing on the pitch
    def getNumOfTeams(self):
        return len(self.teams)

    # Returns specified game object
    def game(self, game):
        return self.games[game]

    # Adds a game to the pitch
    def addGame(self, team1, team2, startTime):
        self.games.append(Game(team1, team2, startTime))

    # Returns the number of games on the pitch
    def getNumOfGames(self):
        return len(self.games)

    # Specifies that the pitch needs a bye team
    def needsBye(self):
        self.hasBye = True

    # Returns whether the pitch needs a bye team
    def doesPitchNeedBye(self):
        return self.hasBye

    # Returns the number of bye games
    def getNumOfByeGames(self):

        # Bye team must play every other team, so there will be one less bye game than there are teams
        if self.hasBye == True:
            return self.getNumOfTeams() - 1
        # If there are no bye teams, there are no bye games
        else:
            return 0

    # Returns the number of non-bye games
    def getNumOfNonByeGames(self):
        # The number of non bye games is the total number of games minus the number of bye games
        return self.getNumOfGames() - self.getNumOfByeGames()

class Team:
    def __init__(self, name, isBye):
        self.name = name
        self.isBye = isBye

    # Returns the name of the team
    def getTeam(self):
        return self.name

    # Returns whether the team is a bye team
    def getIsBye(self):
        return self.isBye

class Game:
    def __init__(self, team1, team2, startTime):
        self.team1 = team1
        self.team2 = team2
        self.startTime = startTime

    # Returns the two teams playing in the game
    def getGame(self):
        return [self.team1, self.team2]

    # Returns the start time of the game
    def getStartTime(self):
        return self.startTime

class TournamentPolygon:
    def __init__(self, pitch):
        self.pitch = pitch

        # If the pitch needs a bye team then a bye team is added to the pitch
        if pitch.doesPitchNeedBye() == True:
            self.pitch.addByeTeam()

        # The teams playing on the pitch
        self.teams = [pitch.team(i) for i in range(pitch.getNumOfTeams())]

        # If the number of teams is even, then a team must go in the centre of the polygon
        if len(self.teams) % 2 == 0:
            self.hasCentre = True
            self.centre = self.teams.pop(-1)
        else:
            self.hasCentre = False

    # Each time moves one vertex along on the polygon, other than the centre team which remains where it is
    def rotate(self):
        self.teams = [self.teams[-1]] + self.teams[:-1]

    # Returns the games for this specific orientation of the polygon
    def getGamesForOrientation(self):
        gamesForOrientation = []

        # Each team plays the team horizontally opposite from it
        for i in range(len(self.teams) // 2):
            gamesForOrientation.append([self.teams[-2 - i], self.teams[i]])

        # The centre team plays the team at the top of the polygon
        if self.hasCentre == True:
            gamesForOrientation.append([self.teams[-1], self.centre])

        return gamesForOrientation

    # Calculates the games for each orientation
    def getGames(self):
        games = []

        # Games need to be calculated for each rotation until polygon is back to its initial orientation
        for i in range(len(self.teams)):
            games.append(self.getGamesForOrientation())
            self.rotate()

        return games

    # Adds games to the pitch
    def calculateGames(self, startTime, gameDuration):
        gameTime = startTime
        # For each orientation essentially
        for round in self.getGames():
            # For each game in the orientation
            for game in round:
                # If the game is a bye game then the game start time is the same as the previous game
                if game[0].getIsBye() == True or game[1].getIsBye() == True:
                    self.pitch.addGame(game[0].getTeam(), game[1].getTeam(), gameTime - gameDuration)
                # If the game is not a bye game then the start time is incremented
                else:
                    self.pitch.addGame(game[0].getTeam(), game[1].getTeam(), gameTime)
                    gameTime += gameDuration

# Rounds the game duration up to nearest five minutes
def calculateGameDuration(halfDuration, halfTimeDuration, swapTeamsDuration):
    # gameDuration is the sum of the two halves, the half-time, and the time taken to get teams off pitch at end of game
    gameDuration = 2 * halfDuration + halfTimeDuration + swapTeamsDuration

    # Rounds game duration up to nearest five minutes
    for i in range(gameDuration, gameDuration + 5):
        if i % 5 == 0:
            gameDuration = i
            break

    return gameDuration

# Returns the minimum number of timeslots needed for a tournament depending on the number of teams and number of pitches
def calcNumOfTimeslots(numOfTeams, numOfPitches):
    maxTeamsPerPitch = numOfTeams // numOfPitches
    teamsRemaining = numOfTeams - (maxTeamsPerPitch * numOfPitches)

    if teamsRemaining != 0:
        maxTeamsPerPitch += 1

    numOfTimeslots = 0

    # 5 teams can fit on a pitch in a timeslot
    # A new timeslot is needed if the no. of teams on a pitch exceeds a new multiple of 5
    # Therefore the for loop below counts up from the max number of teams per pitch until it reaches a number in the sequence 5n + 1
    # It then works out how many times it fits into the sequence, and this is the number of timeslots needed
    for i in range(maxTeamsPerPitch + 1, maxTeamsPerPitch + 6):
        if ((i - 1) / 5) % 1 == 0:
            numOfTimeslots += int((i - 1) / 5)
            break

    return numOfTimeslots

# Returns the layout for each group for a given number of teams and groups
def calcNumOfTeamsOnPitches(numOfTeams, numOfPitches):
    # Initially spreads the number of teams evenly across the groups
    minTeamsPerPitch = numOfTeams // numOfPitches
    teamsRemaining = numOfTeams - (minTeamsPerPitch * numOfPitches)
    numOfTeamsOnPitches = [minTeamsPerPitch] * numOfPitches

    # Assigns the remaining teams to the groups, starting at the first group
    i = 0
    while teamsRemaining != 0:
        numOfTeamsOnPitches[i] += 1
        teamsRemaining -= 1
        i += 1

    return numOfTeamsOnPitches

# Calculates the possible tournament layouts for a given number of teams, pitches and timeslots
def calcTeamsOnPitchesCombos(numOfTeams, numOfPitches, numOfTimeslots):
    # Possible layouts will be added to this list
    combos = []

    # Each pitch within a timeslot is known as a group
    numOfGroups = numOfPitches * numOfTimeslots

    # Finds all possible layouts for the given number of timeslots
    for i in range(numOfTimeslots, numOfTimeslots + numOfPitches):
        # Finds the combo for the number of teams and number of groups
        combo = calcNumOfTeamsOnPitches(numOfTeams, numOfGroups)

        # Assumes the combo to be valid
        validCombo = True

        # For each group in the combo
        for i in combo:
            # If there is more than 5 teams in the group the combo isn't valid
            if i > 5:
                validCombo = False
        # If there is 2 or 1 or 0 teams in a group the combo isn't valid
        if 2 in combo or 1 in combo or 0 in combo:
            validCombo = False

        # If the combo is valid add it
        if validCombo == True:
            combos.append(combo)

        # Reduce the number of groups by 1 to find other potential combos
        numOfGroups -= 1

    return combos

# Creates the tournament objects for each combo provided
def createPossibleTournaments(teams, combos, numOfTimeslots):
    # Creates a queue of teams repeated for the number of combos needed to be implemented
    # This is as each team will need to be dequeued in order to be assigned to a tournament
    teams = Queue(teams.copy() * len(combos))

    # To hold each possible tournament for specific number of timeslots
    tournaments = []

    combosDuplicate = []
    for combo in combos:
        combosDuplicate.append(combo.copy())

    # For each tournament combo
    for i in range(len(combos)):

        # The maximum number of teams on a pitch for a combo is the number of teams on the first pitch
        maxNumOfTeamsOnPitchInATimeslot = combosDuplicate[i][0]

        # The maximum number on a pitch in a timeslot is the number of times the given number of timeslots fits into the number of groups in the combo
        maxNumOfPitchesPerTimeslot = len(combos[0]) // numOfTimeslots
        # Needs to be incremented by one if the number of timeslots does not perfectly fit into the number of groups in the first combo
        if len(combos[0]) % numOfTimeslots != 0:
            maxNumOfPitchesPerTimeslot += 1

        tournaments.append(Tournament())

        numOfPitchesInLastTimeslot = len(combos[i]) - (numOfTimeslots - 1) * maxNumOfPitchesPerTimeslot

        # Add a timeslot for each timeslot
        for j in range(numOfTimeslots):

            # If last timeslot to be added
            if j == numOfTimeslots - 1:
                tournaments[i].addTimeslot(numOfPitchesInLastTimeslot)
            # If not the last timeslot to be added
            else:
                tournaments[i].addTimeslot(maxNumOfPitchesPerTimeslot)

        # For each timeslot in the tournament just created
        for j in range(tournaments[i].getNumOfTimeslots()):

            # For each pitch in the timeslot
            for k in range(tournaments[i].timeslot(j).getNumOfPitches()):
                numOfTeamsToBeAddedToPitch = combosDuplicate[i].pop(0)

                # For the number of teams which will play on the pitch
                for l in range(numOfTeamsToBeAddedToPitch):
                    tournaments[i].timeslot(j).pitch(k).addTeam(teams.deQueue())

                if numOfTeamsToBeAddedToPitch < maxNumOfTeamsOnPitchInATimeslot:
                    tournaments[i].timeslot(j).pitch(k).needsBye()

    return tournaments

# Function called when progran is run. Takes tournament info as its input and returns list of possible combos.
def main(teams, numOfPitches, halfDuration, halfTimeDuration, swapTeamsDuration, startHour, startMinute):
    startTime = datetime(1970, 1, 1, startHour, startMinute)
    gameDuration = timedelta(minutes = calculateGameDuration(halfDuration, halfTimeDuration, swapTeamsDuration))

    numOfTeams = len(teams)
    # Calculate the number of timeslots by inputting the number of teams and number of pitches
    numOfTimeslots = calcNumOfTimeslots(numOfTeams, numOfPitches)

    # Will hold each tournament combo
    tournaments = []

    # Will loop until valid combos can no longer be produced
    while True:
        # Holds the valid tournament layouts for the number of timeslots the loop is being repeated for
        combos = calcTeamsOnPitchesCombos(numOfTeams, numOfPitches, numOfTimeslots)

        # If no valid combos were made then no more valid combos can be made so break the loop
        if combos == []:
            break
        # If valid combos were produced
        else:
            # Implement the combos using tournament object
            tournaments.append(createPossibleTournaments(teams, combos, numOfTimeslots))
            # Incrememnt the number of timeslots by one so the while loop repeats for a greater number of timeslots to find more combos
            numOfTimeslots += 1

    # Puts each combo in each sublist into one big list of combos
    tournaments = [j for i in tournaments for j in i]

    # For each tournament layout
    for tournament in tournaments:
        timeslotStartTime = startTime
        # For each timeslot in the tournament
        for i in range(tournament.getNumOfTimeslots()):
            # For each pitch in the timeslot
            for j in range(tournament.timeslot(i).getNumOfPitches()):
                # The games are calculated for the pitch using the tournament polygon object
                TournamentPolygon(tournament.timeslot(i).pitch(j)).calculateGames(timeslotStartTime, gameDuration)
            # Increase the timeslot start time so start time is correct for games in the next timeslot
            timeslotStartTime += timedelta(seconds = gameDuration.seconds * tournament.timeslot(i).pitch(0).getNumOfGames())

        # The duration of the tournament is now calculated now that all games have been added
        tournament.calculateDuration(gameDuration)

    # The valid tournament layouts are returned
    return tournaments
