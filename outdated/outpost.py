import random
import json_help

class Outpost(object):
    
    def __init__(self, owner, typ, loc):
        """ An outpost which a player controls and reaps benefits from.

        Attributes:
            owner   = <Player> Player who controls outpost
            typ     = <str> Name of resource produced
            loc     = <int> Rim outpost is in
        
            level   = <int> Indicates level of outpost
            bounty  = <int> Output of outpost
            bonus   = <int> Any extra bounty owner gives bounty
            troops  = <int> Number of troops stationed in outpost

            pop     = <int> Population of outpost (scales with level)

        Methods:
        """

        self.typ = typ
        self.loc = loc
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
        Changes level of outpost and updates stats,
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

    def __init__(self, name):
        """ Stores information about the player.

        Attributes:
            name        = <str> Storing the player's name
            resources   = <dict> Stores player's current resources
            bonus       = <dict> Stores bonuses for each resource when reaping
            allocation  = <dict> Stores allocated points
            outposts    = <array> Stores outposts owned by player

            points      = <int> Total count of points allocated
        """

        self.name = name
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
