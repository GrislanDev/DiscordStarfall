Welcome to DiscordStarfall, a bot project written with Python 3.4.2 and the discord.py API.

The player rules a faction in a sci-fi fantasy universe, where they must maintain control over their outposts
to gather resources. Additionally, players can expand their territory by creating new outposts and invading
other players. 

Updates:
"2017-07-10 mainV002"
- Player class
- Outpost class
- World class
- All data can be saved to and retrieved from .json file

- Outpost.reapBounty() to gather resources
- Outpost.train() to purchase and deploy troops
- Outpost.changeOwnership() to change owner of outpost
- Outpost.changeLevel() to update stats with new level
- Outpost.updateStats() to make all stats consistent

- Player.reapBounty() to gather all resources from outposts
- Player.allocatePoints() to allocate skill points
- Player.popUpdate() to keep population consistent with outposts

- World.create() to initialize all objects from save to World.info
- World.save_all() to call self.save() for all objects in World.info
	- Then saves data to .json file

- newOutpost and newPlayer classes for outpost/player creation in-game

"2017-07-10 mainV003"
- Added accounts key to .json to link Discord accounts to player names
	- Will be used to identfy players sending messages
	
"2017-07-11 botV001"
- Bot is now functional on Discord, compatible with mainV003
- Command prefix is "!"
- Added commands:
	- start <factionName>
		- Checks if factionName is availible
		- Checks if user already has a faction
		- Checks if factionName is alphanumeric
		- If successful, creates a new player and saves to file
	- lore
		- Tells user of an epic journey explaining humanity's downfall and the user's role in-game
		
"2017-07-12 mainV004"
- Outpost.train() method removed, now is Player.train(troops, outpost)
	- Troop cost is now 3 Gems/Troop
		- AIM: Add multiplier to cost as Strength allocation increases
	- Error checking is done within method, returns result as a string to send to bot
- World.update() method added
	- Adds 1 energy to all Players, with a max of 15
	- Calls Player.reapBounty() for all Players
	- Saves world to json file
- Player now has energy attribute
	- Consumed when moving troops, max of 15
	- Regen through World.update()
	- Puts gameplay limitations on how much a player can do in one go
- Player.reinforce(troops,source,destination) method added
	- Consumes energy (the distance between outposts + 1)
		- Puts a limit of rapid mobilization of troops
		- Moving between the same Rim costs 1 energy
		- Moving from the Inner to the Deep Rim costs 5 energy
	- Error traps:
		- troops is a positive integer
		- Player owns both outposts	
			- AIM: Allow for allied outpostst be destination
		- Source must have required troops
		- Destination must have required population
		
"2017-07-21 mainV005"
- Outpost.upgrade() method added, increases level by 1 for cost of Steel
	- Cost loaded from World.stats["oc"]
	- Rejects if Outpost is Level 12 already
- World.stats and World.resourcePath attributes added	
	- World.resourcePath defaults to a json file path
		- Stores levelling stats for outposts (upgrade costs, bounty, population)
		- Levelling stats hand-crafted (needs play-testing)
		- Has a default value (this will stay constant across worlds)
	- World.stats is the dict version of json data in World.resourcePath file
		- Created in World.__init__()
		
"2017-07-26 mainV006"
- Outpost.upgrade() method fixes made and tested
	- Not yet implemented in bot, though moved botV001.py to outdated folder
	- botV002.py currently has upgrade method, but is untested
	
"2017-08-02 mainV007"
- Player.strike() method added
	- Fully tested in mainV007
	- Will be implemented as part of botV002
		- Bot will call world.save_all() after the command is issued
	- Player relationships have not been implemented yet
		- Striking isn't an act of war
- Minor changes to Player.reinforce() and Player.train() return strings
	- Made more informative
	- I still want to change the return strings for Player.strike()
		- They work but don't sound cool enough
- World.save_specific() method added
	- Updates a specific object, then saves data to json
	- Might implement in bot later to save time
- World.save_all() docstring changed

"2017-08-05 botV002"
- Added tested build command
- Added untested train command
- Changed syntax messages, arguments now surrounded by [] in syntax reminders

"2017-08-02 mainV008"
- World.time attribute added
	- <json_help.File> object storing current time in minutes (0 --> 1439)
- World.update() no longer calls World.save_all()
- tickTime attribute added
	- Minutes between ticks
- World.update_time() method added
	- Updates World.time and calculates the number of upgrade ticks that have passed
	- Updates the world accordingly, then saves data
	
"2017-08-02/09 botV003"
- Made to work with mainV008
- Calls world.update_time() whenever it recieves a message
	- This worked in mainV008, need to check for effect over Discord
- Uses command_info dictionary from ThinkeroniPizzaBot
	- Stores syntax and description of each command
		- Makes !help command easy to implement
		- Easy to see which commands have been implemented in the bot
- Added !help command
	- If used alone, shows names and descriptions of all commands
	- If used with a command name, shows description and syntax of command
		- When commands are typed with the wrong syntax, !help is suggested
- Added !infoo command
	- Shows information of an outpost, using Outpost.information()
	- Added information() method to Outpost
- Added !infof command
	- Shows information of a faction, using Player.information()
	- Added information() method to Player
- Added !infou command
	- Shows info for an account linked to a Discord user
- Fixed bugs in !train command

"2017-08-11 botV004"
- MAJOR NOTE:
	- None of the bot commands have been tested for a player without a Starfall account
	- For players with accounts they all work
	- For commands that react differently if the player has ownership, only the ownership portion is tested
	- World.update_time() works fine within one day, but can't deal with time wrapping around midnight
		- Needs to store and interpret the entire timestamp in time.json, currently only uses minutes of the day
- Uhhh broke botV003...
	- Fixed issue, text.py module is now in root folder for importing
- text.py module stores dictionaries of strings
	- Command information, lore
	- Will add more to the lore library and tutorial information
		- Comes with functionality of !tuts and an update to !lore
- Minor changes to mainV008
	- Added outpost owner to Outpost.information() result
	- Added basic text formatting
	- Minor bug fixes to !reinforce and !strike
		- Now assumes that troops will be given as a string then converts to int if ok
- Added !reinforce command, stable but with the concerns listed in MAJOR NOTE
	- Added information to help, and return strings
	
Short-Term Goals (Due August 19): ---> Completed August 17
- Organize !help information, the dictionary has no apparent order when printed due to hashing. 
- Fix the time system to include full timestamps
- Implement !tut command to explain basic mechanics
	- You'll need this to help out your confused players
- Implement !strike command in the bot
	- This will be the first playable version of Starfall, show to friends for testing
	
"2017-08-16/17 General Patch 1"
- Tested all information commands for fullInfo and limited info cases
- Fixed battle system bugs
- Fixed infou and infoo bugs
- Improved infof and upgrade return messages
- Fixed time system
	- time.json now stores more info
	- [Current:[days,seconds], [Next:[days,seconds]]]
	- These are days and seconds since datetime.datetime(1,1,1)
	- Conversions done in update_time()
- Added !flist command (lists all factions alphabetically)
- Added !olist command (lists all outposts alphabetically)
- !help commands sorted alphabetically
- Added !tut command

"2017-08-17 botV004 Live Alpha"
- Put ZortanTheSeer online, tested with starfy and yi
	- Good response, maybe cut down on the text a bit
- Changed prefix from ! to $
	- Interfered with another bot :(
	- Changed all command texts showing !
- Removed $strike debug text showing damage and troop counts
- Removed update_time() debug text showing time stats with every message
	- Perhaps I should use the logging module to store events?
	- Will need to dump command info to some sort of log
- Dereck offered to host with Rasp Pi
	- I'll need to put Starfall on Github

"2017-08-25 mainV010"
- reapBounty() and update() now take an extra argument "ticks"
	- Shows how many ticks that need to be simulated
	- update_time() now passes ticks to update() rather than calling update ticks times
	- reapBounty() multiplied the bounty given by ticks so it only needs to be called once
- Player has new attribute, int offline
	- Shows number of offline ticks the player can still collect resources during
	- Player stops collecting resources after 1/2 day offline
		- This is still a ridiculous amount of resources btw
	- Behaviour implemented in reapBounty(), which limits ticks and updates Player.offline
- Added "minSteel" and "minGems" to stats.json
	- If the player has no outposts they're given this minimum income per tick
	- Basic rubber banding to help players get back on their feet
- mainV009 moved to outdated folder
- Removed players sHaDyMen, Arken, and Gondor (and related outposts and accounts)
- botV004 now uses V001ZortanLiveTest.json

1.1 Ascension Update
	- news, allocate, infof^, tuts^, help^
	- Adds news command to show events that have occured since the player last used news
		- Different items in the log have levels of importance, determining how long they stay in the log
		- Log will have max # of items for each level of importance? Need to keep memory low
	- Adds levelling to each faction
		- Factions gain EXP through combat (high stakes, high EXP)
		- Factions gain EXP through upgrading outposts (not building them)
		- When a faction levels up they get a Nexon Shard
		- Level determines the max amount of resources you can store	
			- This doesn't limit troops
	- Adds allocate command
		- A faction can allocate a Nexon Shard into Alpha, Gamma, Delta, Sigma, Epsilon techs
		- Allocation gives certain buffs. Nexon Shards gained through levelling
		- Player can allocate 7 Shards into a tech, maximum of 21 Shards overall
		- Allocation is irreversible
		
        Epsilon - Decreases retreat threshold in battle
        Alpha - Increases attack multiplier, Increases Troop cost
        Gamma - Increases defensive multiplier
        Delta - Increases Steel output, Decreases upgrade cost
        Sigma - Increases Gems output, Increases Population bonus from Arks
		
1.2 Allegiance Update
	- okally, askally, noally, okpeace, askpeace, nopeace, infoo^, infof^, reinforce^, strike^, tuts^, help^
	- Adds alliance and peace requests
		- Allies can see full info on you using infoo and infof
		- infof will show information about alliances for fullInfo
	- Adds the "act of war" mechanics
		- Allies can send troops to allied outposts with reinforce
		- Striking is an act of war, immediately rejects peace
			- Can't strike allies without backing out of alliance
	- tuts update for player relationships, may need multiple topics
	- help update for new commands
	
1.3 Enterprise Update
	- donate, asktrade, oktrade, notrade, news^, lore^, tuts^, help^
	- Allies can directly donate Gems and Steel to each other
	- Allies can request/accept trades of Gems and Steel
	- lore update with topic for the Warlock's Market
	- tuts update explaining the market
	- help update for new commands
	- news will show trade information
	
1.4 Treason Update
	- bounty, sabotage, asktrade^, news^, lore^, tuts^, help^
	- Bounties allow players to gain Shards - new resource
		- Bounties are missions adjusted to the player's estimated level of skill
	- Sabotage allows the player to hire Warlock forces to anonymously attack
		- Sabotage costs Shards
		- You can sabotage anyone, even allies
	- Players must pay a fee of Shards for requesting trades
		- The fee will not apply to donations
		
1.5 Citadel Update (needs awe-inspiring, forceful name. Genocide? Stay away from holocaust.)
	- transport, assemble, launch, shield, build^, news^, lore^, tuts^, help^, infoo^
	- Introduces the Citadel
		- A mobile outpost, can be moved at high energy cost with !transport 
		- Can assemble X # of missiles (scales up with levelling?) using !assemble
		- Makes a huge impact on warfare
	- Introduces Missiles
		- Built and fired from Citadels, they do massive damage to outposts' defenses
			- Built from Steel using !assemble
			- Fired with !launch, this is an act of war
		- They take time to reach their target and cost energy to launch depending on distance
	- Introduces Shields
		- Protects an outpost from Missiles for X ticks
		- They cost Energy to build with !shield, and their durability goes down if hit by Missiles
			- Will not affect !strike (troop-troop combat)
	
Long-Term Goals:
- Relationship statuses between players (Ally, At War, Neutral)
	- Must update !strike to be an act of war
- Alliance request/accept system between players
- Player-Player donations between Allies
- Trade request/accept system between players
