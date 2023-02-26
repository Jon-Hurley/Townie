from django.db import models

# This is the Friendship class – this will hold the friend's ID, 
# friendship status, and games played together
class Friendship(models.Model):
    #friends = models.ManyToManyField(User)

    #User ID for friend
    friendID = models.PositiveIntegerField()

    #0 for accepted, 1 for pending
    status = models.PositiveIntegerField()
    gamesPlayedTogether = models.PositiveIntegerField()

    # Creates a new instance of Friendship
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # Initializes a new instance of Friendship
    def __init__(self, id):
        self.friendID = id
        self.status = 1
        self.gamesPlayedTogether = 0

    # Returns the current object
    def get(self):
        return self
    
    # Accepts the friendship, changing the status to accepted
    def accepted(self):
        self.status = 1
        return
    
    # Increments games played together
    def incrementGPT(self):
        self.gamesPlayedTogether += 1





#This class contains a Purchase - it holds an ID, name, and cost
class Purchase(models.Model):
    purchaseID = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    cost = models.PositiveIntegerField()

    # Creates a new instance of Purchase
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # Initializes a new instance of Purchase
    def __init__(self, id, n, c):
        self.purchaseID = id
        self.name = n
        self.cost = c

    # Returns current purchase object
    def get(self):
        return self
    
    def set(self, id=purchaseID, n=name, c=cost):
        self.purchaseID = id
        self.name = n
        self.cost = c





# This is the User class – this will hold the user's ID, contact information, rank, etc.
class User(models.Model):
    userID = models.PositiveIntegerField()
    #accessToken = 
    username = models.CharField(max_length=20)
    passwordHash = models.CharField(max_length=100)
    phoneNumber = models.PositiveIntegerField()
    totalPoints = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()
    #purchases = models.ManyToManyField(Purchase)
    friends = models.ManyToManyField(Friendship)

    # Creates a new instance of Friendship
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # Initializes a new instance of Friendship
    def __init__(self, id, user, p, phone):
        self.userID = id
        self.username = user
        self.passwordHash = p
        self.phoneNumber = phone
        self.totalPoints = 0
        self.rank = 0
        #purchases = 
        #friends = 


    # Set certain User fields to new parameters, non-specified fields are kept at
    # current values 
    #def set(self, user=username, p=passwordHash, phone=phoneNumber, tp=totalPoints, r=rank, pur=purchases, f=friends):
        #self.username = user
        #self.passwordHash = p
        #self.phoneNumber = phone
        #self.totalPoints = tp
        #self.rank = r
        #purchases = 
        #friends = 

    # Returns current user object
    def get(self):
        return self
    
    # Adds a friend given another user object
    def addFriend(self, user : "User"):
        friendship = Friendship(User(user.userID))
        friendship.save()
        self.friends.add(friendship)

        friendship2 = Friendship(User(self.userID))
        friendship2.save()
        user.friends.add(friendship2)

    # Removes a friend given another user
    def removeFriend(self, user : "User") -> bool:
        success = False
        for ship in self.friends.all():
            if (Friendship(ship).friendID == user.userID):
                self.friends.remove(ship)

        for ship in user.friends.all():
            if (Friendship(ship).friendID == self.userID):
                user.friends.remove(ship)
                success = True
        
        return success
    
    # Makes a purchase with a given ID, name, and cost
    def makePurchase(self, pid, n, c):
        purchase = Purchase(pid, n, c)
        purchase.save()
        self.purchases.add(purchase)
        

    
    

