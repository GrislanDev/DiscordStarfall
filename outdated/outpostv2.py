import random
import json_help

"""
Replicates behaviour of outpost.py, with file IO

Goals:
    - Create a player object and load it into a json file
    - Load player data from a json file
    - Update player data in a json file

    - Above behaviours for outposts
"""

class Outpost(object):
    
    def __init__(self, world):
        """ An outpost which a player controls and reaps benefits from.

        Attributes:
            name    = <str> Name of outpost
            owner   = <Player> Player who controls outpost
            typ     = <str> Name of resource produced
            loc     = <int> Rim outpost is in
            world   = <World> object storing info on world
        
            level   = <int> Indicates level of outpost
            bounty  = <int> Output of outpost
            bonus   = <int> Any extra bounty owner gives bounty
            troops  = <int> Number of troops stationed in outpost

            pop     = <int> Population of outpost (scales with level)

        Methods:
        """

        self.name = name
        self.typ = typ
        self.loc = loc
        self.world = world
        
        self.level = 1
        self.troops = 0
        
        self.bonus = owner.bonus[self.typ]
        self.owner = owner
        owner.outposts.append(self)

        self.updateStats()

    def __str__(self):
        result = "======== OUTPOST INFO ========\n"
        result += "Owner: {}\n".format(self.owner.name)
        result += "Type: {}\n".format(self.typ)
        result += "Level: {}\n".format(self.level)
        result += "Location: {} Rim\n".format(
            ["Core","Inner","Middle","Outer","Deep"][self.loc]
            )
        result += "Troops: {}\n".format(self.troops)
        result += "Population: {}\n".format(self.pop)
        return result

    def save(self):
        """
        Saves data into world as json.
        """
        self.world.save["outposts"][self.name] = {
            "name" : self.name,
            "owner" : self.owner.name,
            "typ" : self.typ,
            "level": self.level,
            "location" : self.loc,
            "bounty" : self.bounty,
            "bonus" : self.bonus,
            "troops" : self.troops,
            "pop" : self.pop
            }

    def load(self):
        """
        Loads data from world.
        """
        s = self.world.save["outposts"][self.name]
        
        self.typ = s["typ"]
        self.level = s["level"]
        self.loc = s["location"]
        self.bounty = s["bounty"]
        self.bonus = s["bonus"]
        self.troops = s["troops"]
        self.pop = s["pop"]

    def describe(self):
        """
        Shortened description showing loc, typ, and level for Player.__str__()
        """
        return "{0} Rim: {1} {2}".format(
            ["Core","Inner","Middle","Outer","Deep"][self.loc],
            self.typ, self.level
            )

    def updateStats(self):
        """
        Changes bounty and pop of outpost dependent on level.
        Later, rather than a formula the stats will be stored in a leveling chart.

        Right now the maximum level is 29, after that the bounty begins to decrease.
        """

        self.bounty = (self.level * 50) - ((self.level ** 2))
        self.pop = self.level * 25

        # Food outposts (farms) provide more population
        if self.typ == "Pop":
            self.pop += self.owner.bonus["Pop"] + self.level * 15

        self.owner.popUpdate()

    def changeLevel(self, newLevel):
        """
        Changes level of outpost and updates stats
        """

        self.level = newLevel
        self.updateStats()

    def reapBounty(self):
        """
        Gives the owner the bounty and the added bonus of the owner.
        """
        if self.typ == "Gems":
            self.owner.resources[self.typ] += random.randint(self.bonus / 3, self.bounty + self.bonus)
        elif not(self.typ == "Pop"):
            self.owner.resources[self.typ] += self.bounty + self.bonus

    def changeOwnership(self, newOwner):
        # Move outpost from outpost lists
        self.owner.outposts.remove(self)    
        newOwner.outposts.append(self)

        # Change owner and update population of old owner
        self.owner.popUpdate()
        self.owner = None       
        self.owner = newOwner

        # Update stats of new owner, and apply differences in bonus
        self.bonus = self.owner.bonus[self.typ] 
        self.updateStats()

class Player(object):

    def __init__(self, name, world):
        """ Stores information about the player.

        Attributes:
            name        = <str> Storing the player's name
            world       = <World> object storing info on world
            resources   = <dict> Stores player's current resources
            bonus       = <dict> Stores bonuses for each resource when reaping
            allocation  = <dict> Stores allocated points
            outposts    = <array> Stores outposts owned by player

            points      = <int> Total count of points allocated
        """

        self.name = name
        self.world = world
        self.resources = {"Gems":0,"Steel":0,"Pop":0,"Troops":0}
        self.bonus = {"Gems":0,"Steel":0,"Pop":0,"Troops":0}
        
        self.allocation = {
            "Faith":0,
            "Intelligence":0,
            "Strength":0,
            "Fortitude":0,
            "Harmony":0
            }

        self.outposts = []
        self.points = 0

    def __str__(self):
        result = "======== PLAYER INFO ========\n"
        result += "Name: {}\n".format(self.name)
        result += "Resources: {}\n".format(self.resources)
        result += "Bonuses: {}\n".format(self.bonus)
        result += "Allocation: {}\n".format(self.allocation)
        result += "Outposts: {}\n".format([o.describe() for o in self.outposts])
        result += "Troops: {0}/{1}\n".format(
            self.resources["Troops"],self.resources["Pop"]
            )
        return result

    def save(self):
        """
        Saves data into world as json.
        """
        self.world.save["players"][self.name] = {
            "name" : self.name,
            "points" : self.points,
            "resources" : self.resources,
            "bonus" : self.bonus,
            "allocation" : self.allocation,
            "outposts" : [o.name for o in self.outposts]
            }

    def load(self):
        """
        Loads data from world.
        """
        s = self.world.save["players"][self.name]
        
        self.points = s["points"]
        self.resources = s["resources"]
        self.bonus = s["bonus"]
        self.allocation = s["allocation"]
        self.outposts = [self.world.info[o] for o in s["outposts"]]

    def reapBounty(self):
        """
        Reap bounties from all outposts owned and count population.
        """

        self.popUpdate()
        for o in self.outposts:
            o.reapBounty()

    def allocatePoints(self, tag, amount=1):
        """
        Allocates points for the player. Will fail if player has maximum number
        of points already, or if specified area already is maxed out.

        These allocations change stats about the player. Can't be undone.

        Faith - Decreases chance of rout in battle, plague from Gods
        Strength - Increases attack power
        Fortitude - Increases defensive power
        Intelligence - Increases Steel output, decreases upgrade cost
        Harmony - Increases chance of recieving gems and population bonus from farms
        """

        # Check if allocation is possible and doesn't exceed limits
        if self.points + amount > 21:
            return False, "Exceeds allocation limit of 21."
        elif self.allocation[tag] + amount > 7:
            return False, "Exceeds allocation limit of 7 per attribute."
        
        self.allocation[tag] += amount
        self.points += amount

        # Apply special bonuses
        if tag == "Intelligence":
            self.bonus["Steel"] += 25 * amount
        elif tag == "Harmony":
            self.bonus["Pop"] += 10 * amount
            self.bonus["Gems"] += 10 * amount

        # Update all stats of outposts
        for o in self.outposts:
            o.updateStats()
        self.popUpdate()
        
        return True, "Got it!"

    def popUpdate(self):
        """ Update population and troop count. """
        self.resources["Pop"] = sum([o.pop for o in self.outposts])
        self.resources["Troops"] = sum([o.troops for o in self.outposts])

class World(json_help.File):

    def __init__(self, path):
        """
        Stores info on the world, deals with saving to json files and
        loading data.

        Attributes:
            path    = <str> File path of json file where data is stored.
            save    = <dict> Stores all info of world for Python to use.
            info    = <dict> Links every object to its name in a dict
        """

        super(World, self).__init__(path)
        #self.create()

##    def create(self):
##        """
##        Initializes all objects from save.
##        """
##
##        self.info = {}
##        for o in self.save["outposts"].keys():
##            self.info["outposts"][o] = Outpost(
        
