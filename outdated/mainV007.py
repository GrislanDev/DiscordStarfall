import random
import datetime

import json_help

"""
Features:
    - Load data from and save to json file
    - Skill point allocation
    - Resource collection and population counts
    - Outpost creation
    - Player creation
    - Troop purchases
    - Troop movement between owned outposts
    - Energy/Time system automated in World.update()
    - Load outpost stats per level from json file
        - Ensures game balance, already designed levelling curves
    - Outpost.upgrade() method
    - Troop-Troop combat

Goals:
    - Relationship statuses (ally, enemy)
    - Trading 
"""

outpostTypes = {
    "Steel" : "Forge",
    "Gems" : "Harvester",
    "Pop" : "Ark",
    }
resourceTypes = {
    "Forge" : "Steel",
    "Harvester" : "Gems",
    "Ark" : "Pop",
    }

def alphanumeric(s):
    """ Returns if <str> s only contains letters and numbers. """
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for ch in s:
        if not(ch in allowed):
            return False
    return True

def okint(n):
    """ Returns if <str> n can be converted to an int. """
    allowed = "0123456789"
    for ch in n:
        if not(ch in allowed):
            return False
    return True    

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
        result += "Type: {}\n".format(outpostTypes[self.typ])
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
        """ Shortened description showing loc, typ, and level for Player.__str__() """
        return "{0} Rim L{2}: {3} {1}".format(
            ["Core","Inner","Middle","Outer","Deep"][self.loc],
            outpostTypes[self.typ], self.level, self.name
            )

    def info(self):
        """ Description of outpost for player information. """
        return "===== {0} {1} =====\nLocation: {2} Rim\n"

    def updateStats(self):
        """
        Changes bounty and pop of outpost dependent on level.
        Later, rather than a formula the stats will be stored in a leveling chart.

        Right now the maximum level is 12
        """

        self.bounty = self.world.stats["ob"][self.level-1]
        self.pop = self.world.stats["op"][self.level-1]

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

    def upgrade(self):
        """
        Upgrades stats at cost of Steel. Will not progress beyond level 12.
        """
        if self.level < 12:
            if self.ownerInfo["resources"]["Steel"] >= self.world.stats["oc"][self.level-1]:
                self.ownerInfo["resources"]["Steel"] -= self.world.stats["oc"][self.level-1]
                self.level += 1
                self.updateStats()
                return "Upgrade successful."
            return "Upgrade failed. You can't afford the cost of {} Steel.".format(self.world.stats["oc"][self.level-1])
        return "Upgrade failed. Outpost is at maximum level."
    
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
            energy      = <int> Energy of player, consumed when moving troops
        """

        self.name = name
        self.world = world

        self.world.info["players"][self.name] = self

        if saved:
            self.load()

    def __str__(self):
        result = "================ PLAYER INFO ================\n"
        result += "Name: {}\n".format(self.name)
        result += "Energy: {}\n".format(self.energy)
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
            "energy" : self.energy,
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
        self.energy = s["energy"]
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

    def strike(self, troops, source, target):
        """ Attacks the target outpost with troops from owned source outpost. """

        if not(source in self.outposts):
            return "Strike denied. Source outpost {} is not owned by you.".format(source)

        if target in self.outposts:
            return "Strike denied. Target outpost {} is owned by you.".format(target)

        if not(target in self.world.info["outposts"]):
            return "Strike denied. Target outpost {} does not exist.".format(target)

        if not((type(troops)== int)) or troops < 1:
            return "Strike denied. The number of troops must be a positive integer."

        if troops > self.world.info["outposts"][source].troops:
            return "Strike denied. Source outpost {0} only has {1} troop(s).".format(
                source,self.world.info["outposts"][source].troops)

        d = self.world.info["outposts"][target]
        s = self.world.info["outposts"][source]
        cost = abs(d.loc - s.loc) + 1

        if cost > self.energy:
            return "Strike denied. You need {0} more Energy to carry out the strike.".format(
                cost - self.energy
                )

        self.energy -= cost

        # Number of troops on each side
        attackers = int(troops)
        defenders = int(self.world.info["outposts"][target].troops)

        # Original number of troops
        oatk = int(attackers)
        odef = int(defenders)

        # The enemy player
        enemy = self.world.info["players"][self.world.info["outposts"][target].owner]

        # Damage multipliers for each side
        atkMultiplier = 1.05 + (self.allocation["Alpha"] * 0.05)
        defMultiplier = 1.25 + (enemy.allocation["Gamma"] * 0.045)

        # Retreat thresholds for the attackers - defenders fight to the death
        retreat = oatk * (0.49 - self.allocation["Epsilon"] * 0.07)

        while True:
            damageAtk = round(attackers * atkMultiplier * (random.randint(10, 45) / 100))
            damageDef = round(defenders * defMultiplier * (random.randint(10, 45) / 100))

            attackers -= damageDef
            defenders -= damageAtk

            print ("DAMAGE: {0}, {1}".format(damageAtk, damageDef))
            print ("TROOPS: {0}, {1}".format(attackers, defenders))
            
            if attackers < retreat:
                if defenders < 0:
                    defenders = 0
                self.world.info["outposts"][target].troops = defenders
                self.world.info["outposts"][source].troops = self.world.info["outposts"][source].troops - oatk + min(0,attackers)

                self.save()
                
                return "Strike failed. Your troops suffered {0} casualities and retreated. Target outpost has {1} troops left. You have {2} Energy left.".format(
                    oatk - attackers, self.world.info["outposts"][target].troops, self.energy
                    )
            
            elif defenders <= 0:
                if attackers < 0:
                    attackers = 0
                self.world.info["outposts"][target].troops = attackers
                self.world.info["outposts"][source].troops = self.world.info["outposts"][source].troops - oatk

                self.world.info["outposts"][target].changeOwnership(self.name)

                self.save()
                
                return "Strike successful. You have taken control of target outpost {0} with {1} troops left. You have {2} Energy left.".format(
                    target, self.world.info["outposts"][target].troops, self.energy
                    )

    def train(self, troops, outpost):
        """ Adds <int> troops to <str> outpost if affordable.

        Currently, we'll set the cost at 3 Gems per Troop.
        This also won't go through if the outpost's population will be less
        than the amount of troops at it.
        """

        if not(outpost in self.outposts):
            return "Training failed. {} is not owned by you.".format(outpost)

        if not((type(troops)== int)) or troops < 1:
            # Troops must be int
            return "Training failed. The number of troops must be a positive integer."

        if self.world.info["outposts"][outpost].troops + troops < self.world.info["outposts"][outpost].pop + 1:
            # Outpost population must be able to support troops
            cost = troops * 3
            if self.resources["Gems"] - cost > -1:
                # Player must be able to afford troops
                self.resources["Gems"] -= cost
                self.world.info["outposts"][outpost].troops += troops
                self.resources["Troops"] += troops

                self.world.info["outposts"][outpost].save()
                self.save()
                return "Training successful. {0} now has {1} troops. You have {2} Gems remaining.".format(
                    outpost, self.world.info["outposts"][outpost].troops, self.resources["Gems"]
                    )
            return "Training failed. You need {0} more Gems to train {1} troops.".format(
                cost - self.resources["Gems"], troops
                )
        return "Training failed. The population of {0} is insufficient for the deployment of {1} troops.".format(
            outpost, troops
            )

    def reinforce(self, troops, source, destination):
        """ Moves <int> troops from <str> source outpost to <str> destination outpost. """
        
        if troops < 1 or not((type(troops)== int)):
            # Troops must be int
            return "Reinforcement failed. The number of troops must be a positive integer."

        if not(source in self.outposts and destination in self.outposts):
            return "Reinforcement failed. Both the source and the destination must be owned by you."

        d = self.world.info["outposts"][destination]
        s = self.world.info["outposts"][source]
        cost = abs(d.loc - s.loc) + 1

        if cost <= self.energy:
            # Player must have enough energy to move troops
            if d.troops + troops < d.pop + 1:
                # Destination outpost population must be able to support troops
                if s.troops + 1 > troops:
                    # Source outpost must have enough troops to give
                    s.troops -= troops
                    d.troops += troops
                    self.energy -= cost
                    s.save()
                    d.save()
                    self.save()

                    return "Reinforcement successful. {0} now has {1} troops. {2} now has {3} troop(s). You have {4} energy left.".format(
                        source, s.troops, destination, d.troops, self.energy
                        )
                else:
                    return "Reinforcement failed. The troop count of {0} ({2}) is insufficient for the deployment of {1} troop(s).".format(
                        source, troops, s.troops
                        )
            else:
                return "Reinforcement failed. The population of {0} ({2}) is insufficient for the deployment of {1} troop(s).".format(
                    destination, troops, d.pop
                    )
        else:
            return "Reinforcement failed. Your energy level of {0} is insufficient for the cost of moving the troop(s) ({1}).".format(
                self.energy, cost
                )

    def buildOutpost(self, name, typ, loc):
        if okint(loc) and 0 <= int(loc) <= 4:
            # Location must be legal
            if typ in resourceTypes.keys():
                # Outpost type must be legal
                if alphanumeric(name) and name not in self.world.save["outposts"].keys():
                    # Outpost name can't be taken already and must be alphanumeric
                    if self.resources["Steel"] >= 250:
                        # Player must have at least 250 Steel
                        self.resources["Steel"] -= 250
                        newOutpost(name, self.world, self.name, resourceTypes[typ], int(loc))
                        self.popUpdate()
                        return "The {0} {1} has been built. You now have {2} Steel.".format(
                            name, typ, self.resources["Steel"]
                            )
                    return "Construction failed. You need {} more Steel to build an outpost.".format(
                        250 - self.resources["Steel"]
                        )
                return "Construction failed. Your outpost name can't be taken already and must only contain letters and numbers."
            return "Construction failed. The types of outposts are {}. See '!tuts outposts' for more info.".format(
                "('Forge', 'Ark', 'Harvester')"
                )
        return "Construction failed. Your outpost location must an integer between 0 and 4."
            
    def allocatePoints(self, tag, amount=1):
        """
        Allocates points for the player. Will fail if player has maximum number
        of points already, or if specified area already is maxed out.

        These allocations change stats about the player. Can't be undone.

        Epsilon - Decreases retreat threshold in battle
        Alpha - Increases attack multiplier
        Gamma - Increases defensive multiplier
        Delta - Increases Steel output, decreases upgrade cost
        Sigma - Increases chance of recieving gems and population bonus from farms
        """

        # Check if allocation is possible and doesn't exceed limits
        if self.points + amount > 21:
            return False, "Exceeds allocation limit of 21."
        elif self.allocation[tag] + amount > 7:
            return False, "Exceeds allocation limit of 7 per attribute."
        
        self.allocation[tag] += amount
        self.points += amount

        # Apply special bonuses
        if tag == "Delta":
            self.bonus["Steel"] += 25 * amount
        elif tag == "Sigma":
            self.bonus["Pop"] += 10 * amount
            self.bonus["Gems"] += 10 * amount

        # Update all stats of outposts
        for o in self.outposts:
            self.world.info["outposts"][o].updateStats()
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
        
        self.resources = {"Gems":50,"Steel":450,"Pop":0,"Troops":0}
        self.bonus = {"Gems":0,"Steel":0,"Pop":0,"Troops":0}
        
        self.allocation = {
            "Epsilon":0,
            "Alpha":0,
            "Gamma":0,
            "Delta":0,
            "Sigma":0
            }

        self.outposts = []
        self.points = 0
        self.energy = 10

        self.popUpdate()
        
class World(json_help.File):

    def __init__(self, path, resourcePath="resources\\stats.json"):
        """
        Stores info on the world, deals with saving to json files and
        loading data.

        Attributes: 
            path    = <str> File path of json file where data is stored.
            save    = <dict> Stores all info of world for Python to use.
            info    = <dict> Links every object to its name in a dict.

            statsPath = <str> File path of json file where fixed stats are stored.
            stats     = <dict> Storing all fixed stats from statsPath
        """

        super(World, self).__init__(path)

        self.stats = json_help.File(resourcePath).save
        
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
            "outposts" : {},
            }
        
        for p in self.save["players"].keys():
            self.info["players"][p] = Player(p,self,True)
        
        for o in self.save["outposts"].keys():
            self.info["outposts"][o] = Outpost(o,self,True)

    def update(self):
        """ Updates all outposts and players, gather resources and handle all time systems.

        Called every: 15 min
        
        Affects:
            - Reaps bounty for players
            - Replenishes energy
            - Checks if requests (trade, alliance, peace) have expired
            - Depletes shields
        """

        for player in self.info["players"].keys():
            p = self.info["players"][player]
            if p.energy < 15:
                # Player can have a max of 15 energy
                p.energy += 1
            p.reapBounty()

        self.save_all()

    def save_all(self):
        """ Updates all of self.save and writes to json file. """

        for key in self.info.keys():
            if not key == "accounts":
                for obj in self.info[key].keys():
                    self.info[key][obj].save()

        self.write_save()

    def save_specific(self, key, obj):
        """ Updates portion of self.save and writes to json. """
        
        self.info[key][obj].save()
        self.write_save()
        


        
