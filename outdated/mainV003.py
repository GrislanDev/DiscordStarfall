import random
import json_help

"""
Features:
    - Load data from and save to json file
    - Skill point allocation
    - Resource collection and population counts
    - Outpost creation
    - Player creation
    - Troop purchases

Goals:
    - Costs for upgrading outposts
    - Fixed level stats for outposts
    - Troop-Troop combat
    - Relationship statuses (ally, enemy)
    - Trading 
"""

class Outpost(object):
    
    def __init__(self, name, world, saved=False):
        """ An outpost which a player controls and reaps benefits from.

        Attributes:
            name    = <str> Name of outpost
            owner   = <str> Name of player who owns
            
            typ     = <str> Name of resource produced
            loc     = <int> Rim outpost is in
            world   = <World> object storing info on world
        
            level   = <int> Indicates level of outpost
            bounty  = <int> Output of outpost
            bonus   = <int> Any extra bounty owner gives bounty
            troops  = <int> Number of troops stationed in outpost

            pop       = <int> Population of outpost (scales with level)
            ownerInfo = <dict> Stores info about owner
        """        

        self.name = name
        self.world = world

        if saved:
            self.load()

    def __str__(self):
        result = "================ OUTPOST INFO ================\n"
        result += "Name: {}\n".format(self.name)
        result += "Owner: {}\n".format(self.owner)
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
        Saves data into world.save for json.
        """
        self.world.save["outposts"][self.name] = {
            "name" : self.name,
            "owner" : self.owner,
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
        Loads data from world.save from json format.
        """
        s = self.world.save["outposts"][self.name]
        
        self.typ = s["typ"]
        self.owner = s["owner"]
        self.level = s["level"]
        self.loc = s["location"]
        self.bounty = s["bounty"]
        self.bonus = s["bonus"]
        self.troops = s["troops"]
        self.pop = s["pop"]

        self.ownerInfo = self.world.save["players"][self.owner]

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
            self.pop += self.ownerInfo["bonus"]["Pop"] + self.level * 15
            
        self.save()
        self.world.info["players"][self.owner].popUpdate()
        

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
            self.ownerInfo["resources"][self.typ] += random.randint(self.bonus / 3, self.bounty + self.bonus)
        elif not(self.typ == "Pop"):
            self.ownerInfo["resources"][self.typ] += self.bounty + self.bonus

    def changeOwnership(self, newOwner):
        # Move outpost from outpost lists
        self.world.info["players"][self.owner].outposts.remove(self.name)
        self.world.info["players"][newOwner].outposts.append(self.name)
        #self.world.save["players"][newOwner]["outposts"].append(self.name)

        # Change owner and update population of old owner
        self.world.info["players"][self.owner].popUpdate()
        self.owner = None       
        self.owner = newOwner

        # Update stats of new owner, and apply differences in bonus
        self.ownerInfo = self.world.save["players"][newOwner]
        self.bonus = self.ownerInfo["bonus"][self.typ] 
        self.updateStats()

    def train(self, troops):
        """ Adds <int> troops to outpost if affordable.

        Currently, we'll set the cost at 7 Gems per Troop.
        This also won't go through if the outpost's population will be less
        than the amount of troops at it.
        """

        if troops < 1:
            return (False, "Troops must be positive integer.")

        if self.troops + troops < self.pop + 1:
            cost = troops * 7
            if self.ownerInfo["resources"]["Gems"] - cost > -1:
                self.ownerInfo["resources"]["Gems"] -= cost

                self.save()
                self.world.info["players"][self.owner].save()
                return (True, "Training successful.")
            return (False, "Can't afford.")
        return (False, "Population insufficient.")

class newOutpost(Outpost):
    
    def __init__(self, name, world, owner, typ, loc):
        """
        Creates a completely new Outpost object.
        """
        
        super(newOutpost, self).__init__(name, world)
        
        self.typ = typ
        self.loc = loc

        self.level = 1
        self.troops = 0
        self.bounty = 0
        self.pop = 0
        self.owner = owner
        self.ownerInfo = self.world.save["players"][self.owner]
        self.bonus = self.ownerInfo["bonus"][self.typ]

        self.world.info["outposts"][self.name] = self
        self.save()

        self.world.info["players"][self.owner].outposts.append(self.name)
        self.world.info["players"][self.owner].save()
        self.updateStats()

class Player(object):

    def __init__(self, name, world, saved=False):
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

        self.world.info["players"][self.name] = self

        if saved:
            self.load()

    def __str__(self):
        result = "================ PLAYER INFO ================\n"
        result += "Name: {}\n".format(self.name)
        result += "Resources: {}\n".format(self.resources)
        result += "Bonuses: {}\n".format(self.bonus)
        result += "Allocation: {}\n".format(self.allocation)
        result += "Outposts: {}\n".format(
            [self.world.info["outposts"][o].describe() for o in self.outposts]
            )
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
            "outposts" : self.outposts
            }

    def load(self):
        """
        Loads data from world.info.
        """
        s = self.world.save["players"][self.name]
        
        self.points = s["points"]
        self.resources = s["resources"]
        self.bonus = s["bonus"]
        self.allocation = s["allocation"]
        self.outposts = s["outposts"]

    def reapBounty(self):
        """
        Reap bounties from all outposts owned and count population.
        """

        self.popUpdate()
        for o in self.outposts:
            self.world.info["outposts"][o].reapBounty()

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
            self.world.info["outposts"][o].updateStates()
        self.popUpdate()
        
        return True, "Got it!"

    def popUpdate(self):
        """ Update population and troop count. """
        self.resources["Pop"] = sum(
            [self.world.info["outposts"][o].pop for o in self.outposts]
            )
        self.resources["Troops"] = sum(
            [self.world.info["outposts"][o].troops for o in self.outposts]
            )

        self.save()

class newPlayer(Player):
    
    def __init__(self, name, world):
        """
        Creates a completely new Outpost object.
        """
        
        super(newPlayer, self).__init__(name, world)
        
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

        self.popUpdate()
        
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
        self.create()

    def __str__(self):
        result = ""
        for classification in self.info.keys():
            for item in self.info[classification].keys():
                result += str(self.info[classification][item])
        return result

    def create(self):
        """
        Initializes all objects from save.
        """

        self.info = {
            "accounts" : self.save["accounts"],
            "players" : {},
            "outposts" : {}
            }
        
        for p in self.save["players"].keys():
            self.info["players"][p] = Player(p,self,True)
        
        for o in self.save["outposts"].keys():
            self.info["outposts"][o] = Outpost(o,self,True)

    def save_all(self):
        """
        Save all data to json file.
        """

        for key in self.info.keys():
            if not key == "accounts":
                for obj in self.info[key].keys():
                    self.info[key][obj].save()

        self.write_save()


        
