"""
Stores preset strings and dictionaries for DiscordStarfall.
"""

command_info = {
    "help" : ["'$help [commandName]'", "Shows syntax and purpose of a command."],
    "lore" : ["'$lore'", "Describes the lore of the Discord Starfall Galaxy."],
    "start" : ["'$start [faction]'", "Starts a new faction. Name can only contain letters and numbers."],
    "tut" : ["$tut [topic]'", "Shows tutorial explaining topic. Leave topic empty to see existing topics."],
    
    "flist" : ["'$flist'", "Lists all the existing factions."],
    "olist" : ["'$olist'", "Lists all the existing outposts."],
    "infoo" : ["'$infoo [outpost]'", "Shows information on an outpost. Addtional information is shown for controlled outposts."],
    "infof" : ["'$infoo [faction]'", "Shows information on a faction. Addtional information is shown for your faction."],
    "infou" : ["'$infou [userTag]'", "Shows information on a Discord user's Starfall account. Addtional information is shown for yourself."],
     
    "upgrade" : ["'$upgrade [outpost]'", "Upgrades an outpost under your control. See !infoo to determine upgrade cost and other outpost information."],
    "build" : ["'$build [outpost] [type] [location]'", "Creates an outpost. Outpost types can be Forge, Harvester, and Ark. The location of the outpost will be an integer from 0 to 4."],

    "train" : ["'$train [troops] [outpost]'", "Trains troops at an outpost under your control at the cost of 3 Gems per troop."],
    "reinforce" : ["'$reinforce [troops] [source] [destination]'", "Moves troops from a controlled source outpost to a controlled destination outpost. Costs 1 Energy + 1 Energy for each Rim in between the outposts."],
    "strike" : ["'$strike [troops] [source] [target]'", "Attacks a target outpost with troops from a controlled source outpost. Costs 1 Energy + 1 Energy for each Rim in between the outposts."],
    }

tut_info = {
    "resources" :
"""Resources are collected from your outposts and drive your faction's development.

Steel is produced by Forges and is used to upgrade and build outposts.
Gems are produced by Harvesters and are used to train troops.

Related topics: outposts
""",
    "outposts" :
"""Starfall revolves around controlling outposts located aross the 5 Rims (Core, Inner, Middle, Outer, Deep). Each outpost can be built for 250 Steel and provides different advantages which can be improved through upgrades. An outpost's population determines how many troops it can have.

Forges produce Steel. Harvesters produce Gems. Arks have massive populations.

Related topics: resources
""",
    "battle" :
"""
Outposts can be captured through strikes, by sending troops from a controlled outpost to a target outpost. Troops can be moved between controlled outposts to increase the size of an attack force. The distance between two outposts determines the Energy cost of moving troops between them for reinforcement and strikes. If a strike eliminates all the defending troops the target outpost comes under your control. Your forces will retreat if their numbers drop too low - troops who retreat will not return to the source outpost.

Related topics: energy
""",
    "energy" :
"""
Energy allows you to move troops and strike outposts. The Energy cost of moving troops and striking outposts increases if the outposts are located far from each other. 1 Energy is regenerated every 15 minutes and you have a maximum of 15 Energy.

Related topics: battle
"""
    }

lore = {
    "main" :
"""In the Revelation we discovered and decrypted the Nexon, an ancient technology holding the secrets to galatical exploration.
In the Expansion we left our ravished Solar System and colonized the far reaches of another galaxy.

Those were days of peace and cooperation, when stability was maintained by the Council and protected by the Warlocks.

In the Stagnation our resources ran thin as our populations rocketed. Unrest grew as the Council turned corrupt and locked away the Nexon for themselves.
In the Fall our Warlocks turned us against each other, and our galaxy plummeted into chaos.

Those were days of despair and betrayal, a pathetic repetition of our destruction of the Milky Way.

Those days are over.

We have entered the Resurrection. The Citadel of Epsilus stole the Nexon and destroyed it.
The Warlocks have been exiled to the Deep Rim, now replaced by Factions who once knelt beneath them.
Lead yours wisely, {}. Many threats await your coming.

The Warlocks now plot for a return to the Fall, and will strike against any sign of unity.
The Factions all vie for the control of the galaxy, and will do whatever it takes to get there.

Welcome to Starfall.
"""
    }
