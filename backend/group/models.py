from django.db import models
# Create your models here.
class Location(models.Model):
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)


# This is the Destination class -- this will hold the name, location, address
# and point value associated with the destination for the game.

class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    
    def getLocation(self):
        return self.location
    
    def getAddress(self):
        return self.address
    
    def getPoints(self):
        return self.points

# This is the Group class -- this holds the name of the group and a list of
# users that are currently in the group.

class Group(models.Model):
    groupName = models.CharField(max_length = 20)
    #members = models.ManytoManyField(GroupUser)

    def getGroupName(self):
        return self.groupName
    
    def getMembers(self):
        return self.members

    # This function adds a user to the list of players, which will be invoked
    # when a user tries to join the group.
    
    def addUser(self, otherUser):

        # To add a user, we simply cast the list of members to a list, and use
        # the append function to add the member to the list.

        groupMembers = self.members
        list(groupMembers).append(otherUser)

    # This function removes a user from the list of players, which is invoked
    # when a user attempts to leave the game.
    
    def removeUser(self, otherUser):

        # To remove the user, we simply cast the list of members to a list, and
        # then use the remove function to remove the user from the list.

        groupMembers = self.members
        list(groupMembers).remove(otherUser)

# This is the GameSettings class which holds the information for a game. An
# object of type GameSettings holds four boolean values that represent which
# modes of transportation, a radius, a time for intended completion, and a
# string representing the theme of the game (food, museums, etc.)

class GameSettings(models.Model):
    busAllowed = models.BooleanField()
    carAllowed = models.BooleanField()
    subwayAllowed = models.BooleanField()
    boatAllowed = models.BooleanField()
    radius = models.PositiveIntegerField()
    intendedCompletionTime = models.PositiveIntegerField()
    theme = models.CharField(max_length = 50)

    # This is the function that gets the transportation modes for the game.

    def getTransportation(self):

        # To handle getting the transportation modes without using four
        # different functions to get each mode, we return an list of four
        # transportation modes.

        transportation = []
        transportation.append(self.busAllowed)
        transportation.append(self.carAllowed)
        transportation.append(self.subwayAllowed)
        transportation.append(self.boatAllowed)

        return transportation
    
    def getRadius(self):
        return self.radius
    
    def getIntendedCompletionTime(self):
        return self.intendedCompletionTime
    
    def getTheme(self):
        return self.theme

# This is the Game class, which holds the data for the central element of the
# project, the game. It holds the game ID which is used for joining, the start
# time, the maximum time allowed to play, the number of players who are
# finished with the game, a Group object to show the members, the list of
# destinations, and an object that holds all of the settings.

class Game(models.Model):
    gameID = models.IntegerField()
    startTime = models.DateTimeField(auto_now_add=True)
    maxTime = models.IntegerField()
    numFinished = models.IntegerField()
    members = models.OneToOneField(Group, on_delete=models.DO_NOTHING)
    destinations = models.ManyToManyField(Destination)
    settings = models.OneToOneField(GameSettings, on_delete=models.CASCADE)

    def getGameID(self):
        return self.gameID
    
    def getStartTime(self):
        return self.startTime

    def getMaxTime(self):
        return self.maxTime
    
    def getNumFinished(self):
        return self.numFinished
    
    def getMembers(self):
        return self.members
    
    def getDestinations(self):
        return self.destinations
    
    def getGameSettings(self):
        return self.settings
    
    def setNumFinished(self, newNumFinished):
        self.numFinished = newNumFinished
    
    def setDestinations(self, newDestinations):
        self.numFinished = newDestinations
    
    def generateDestList():
        # TODO: Implement web-scraping and come back to this.
        return
    
    def endGame():
        # TODO: Implement ending the game and return to this.
        return
    
    def startGame():
        # TODO: Implement starting the game and returning to this.
        return