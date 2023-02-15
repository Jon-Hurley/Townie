from django.db import models

# Create your models here.
class Location(models.Model):
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)

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

class Group(models.Model):
    groupName = models.CharField(max_length = 20)
    #members = models.ManytoManyField(GroupUser)

    def getGroupName(self):
        return self.groupName
    
    def getMembers(self):
        return self.members
    
    def addUser(self, otherUser):
        groupMembers = self.members
        list(groupMembers).append(otherUser)
    
    def removeUser(self, otherUser):
        groupMembers = self.members
        list(groupMembers).remove(otherUser)

class GameSettings(models.Model):
    busAllowed = models.BooleanField()
    carAllowed = models.BooleanField()
    subwayAllowed = models.BooleanField()
    boatAllowed = models.BooleanField()
    radius = models.PositiveIntegerField()
    intendedCompletionTime = models.PositiveIntegerField()
    theme = models.CharField(max_length = 50)

    def getTransportation(self):
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