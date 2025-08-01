/* This is the documentation for the asset 'Commands' */

Commands are

Available Commands:
	MEDITATE, 	//Action-Hint: Save
	REMEMBER, 	//Action-Hint: Load
	REBIRTH, 	//Action-Hint: Restart
	SUICIDE, 	//Action-Hint: Quit without save
	THINK, 		//Action-Hint: Recompile what happened so far and read hints
	AWAKE,		//Action-Hint: Level up, every level grants 7 attribute points and every 3 levels you gain 1 point for skills and traits

	CHECK,		//Action-Hint: Display multiple possible different Statistics
	STATUS,		//Action-Hint: Active Status-effects
	MIND,		//Action-Hint: Morality of your character
	ATTRIBUTES,	//Action-Hint: Attributes of your character and its current values
	INVENTORY,	//Action-Hint: Contents of your Inventory
	SKILLS,		//Action-Hint: Acquired skills
	TRAITS,		//Action-Hint: Current Traits
	FOCUS, 		//Action-Hint: Combat-only-specific special skills, applicable, but not checkable during fight
	BLOODTYPE, 	//Player-Condition: Inventory == "Blood-Drain" && Inventory == "Analyzer" 
	APPEARANCE,	//Action-Hint: Last seen appearance, for update you need a reflective surface or a mobile mirror

	OPEN,		//Action-Hint: Try to open doors and containers
	BREACH, 		//Player-Condition: 'Vigor' >= 50 / Effect: Break closed doors
	UNLOCK, 		//Player-Condition: 'Alacrity' >= 50 && Trait[] == "Silent as smoke"
	SHUT,		//Player-Condition: 
	TAKE,		//Player-Condition: 
	CRAFT, 		//Only if the player has at least 30 'Alacrity' and 20 'Awareness' and the skill "Craftsmanship"
	CONCOCT, 	//Only if the player has the skill "Alchemy"
	COOK, 		//Only possible if the play has at least 10 'Empathy' and 20 'Alacrity' and the skill "Cooking Mama"/"Cooking Daddy"
	LEECH, 		//Action-Hint: Sacrifice health, to gain Grant
	CONJURE,		//Only possible if player has at least 25 'Transcendence'
	RECHARGE,	//Action-Hint: Recharge a conjuration with the sacrifice of grant
	PILLAGE, 	//If Mind is Perverted, +25% more loot, socially immoral and replaces LOOT
	LOOT, 		//Player-Condition: 'Mind' == "Virtuous" || 'Mind' == "Conflicted" //If Mind is either Virtuous or Conflicted, socially neutral
	EQUIP, 		//Action-Hint: Equip item from inventory
	DROP,
	USE,	
	LOOKAROUND, 	//Action-Hint: Look around room or examine item/person
	EXAMINE,		//Player-Condition: 'Awareness' > 25 && Trait[] ==  "Investigative Eye" / Effect: Replace SURVEIL && More details
	MEMORIZE,	//Player-Condition:  / Effect: Backtracking, maximum of 5 charges, realized with Java-Queue 
	SYNAPSIS,	//
	READ,		//Only possible if character has Trait[] ==  "Literacy"
	WRITE, 		//Only possible if the character has the Trait[] ==  "Literacy"
	JUMP,
	HOP, 		//Disadvantage (unchangeable when 'Vigor' = 100, replaces JUMP
	CROUCH,
	HIDE,		//Player-Condition: 'Alacrity' > 15
	SNEAK, 		//Only possible if the player has at least 25 'Alacrity' and the Trait[] ==  "Silent as smoke", is disabled when the player has more than 65 'Vigor'
	WALK,		//Action-Hint: Switch to known & unknown locations
	JOG, 		//Player-Condition: 'Vigor' > 65 // Effect: Replaces SPRINT, 
	SPRINT, 		//Player-Condition: 'Alacrity' >= 25 && 'Vigor' < 65 // Effect:
	RIDE,
	STEAL, 		//Player-Condition: 'Alacrity' >= 35
	EVADE,		//Player-Condition: 'Alacrity' > 10
	SPARE,		//Player-Condition: 'Mind' => "Virtuous" / Effect: Random item-drop out of inventory && NPC remembers && +10 'Goodwill'
	STRIKE,		//Action-Hint: Attack
	CRUSH, 		//Player-Condition: 'Vigor' > 50 / Effect: Replace STRIKE, +15% Damage
	SLASH,		//Player-Condition: 'Alacrity' > 50 / Effect: Replace STRIKE, +15% Damage
	SHATTER, 	//Player-Condition: 'Vigor' > 50 && 'Alacrity' > 50 / Effect: Replace STRIKE/CRUSH/SLASH, +35% Damage
	SLAUGHTER, 	//Player-Condition: 'Mind' == "Perverted" && Trait[] ==  == "Disregard" / Effect: +15% Damage, +10% Critical Chance, +25% Critical Damage
	MUTILATE,	//Player-Condition: 'Mind' == "Perverted-Inhuman" && Trait[] ==  "Disregard" / Effect: +25% Damage, +20% Critical Chance, +35% Critical Damage
	EXECUTE,		//Player-Condition: 'Vigor' > 25 && 'Mind' == "Perverted" / Effect: Able to kill non-hostile NPCs
	ABUSE, 		//Player-Condition: 'Mind' == "Perverted-Morbid" && Trait[] ==  "Disregard" / Effect: highly immoral, -25 'Goodwill', locks out 'Innocence'
	MUTATE, 		//Player-Condition: 'Bloodtype' == "Mutated" && 'Health' <= 10%

	TALK,
	LOOK,
	PURCHASE, 	//Action-Hint: Buy items with currency
	RETAIL, 		//Action-Hint: Sell items for currency
	TRADE, 		//Action-Hint: Trade with items in exchange for other items, with percentage determining success
	INSULT,
	SCREAM,
	WHISPER,
	BARGAIN, 	//Player-Condition: 'Empathy' >= 20 / Effect: Replace TRADE, higher % based on 'Empathy' for successful trade
	INTIMIDATE, 	//Player-Condition: 'Empathy' >= 10 && 'Vigor' > 35
	DECEIT, 		//Player-Condition: 'Empathy' >= 20 && 'Mind' >= "Conflicted"
	CHARM, 		//Player-Condition: 'Empathy' >= 25 && 'Mind' == "Virtuous" || 'Empathy' >= 50 && 'Mind' == "Conflicted" || 'Empathy' >= 65 && 'Mind'  == "Perverted"
	SEDUCE, 		//Player-Condition: 'Empathy' >= 35 for opposite sex || 'Empathy' >= 50 for same sex
	MANIPULATE, 	//Player-Condition: 'Empathy' >= 35 && 'Brilliance' >= 35
	ANALYZE, 	//Player-Condition: 'Empathy' >= 30 && ''Awareness'' > 20 && 'Brilliance' > 10 && Trait[] == "Investigative Eye"

	NORTH,
	SOUTH,
	EAST,
	WEST,
	NORTHEAST,
	NORTHWEST,
	SOUTHEAST,
	SOUTHWEST,
	UP, 			//Lateral
	DOWN, 		//Lateral
	LEFT, 		//Horizontal
	RIGHT 		//Horizontal