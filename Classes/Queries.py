class qMonsters:
    SELECT_ALL = 'SELECT * FROM Monsters'
    SELECT_RANDOM_ADVANCED = 'SELECT * FROM "Monsters" WHERE rarity = $1 AND element =$2 ORDER BY random() LIMIT 1'
    SELECT_RANDOM = 'SELECT * FROM "Monsters" WHERE rarity = $1 ORDER BY random() LIMIT 1'
    INSERT = 'INSERT INTO Monsters VALUES ($1, $2, $3)'

class qGameModes:
    SELECT_ALL = 'SELECT * FROM "Gamemodes"'
    SELECT_GAMEMODE = 'SELECT * FROM "Gamemodes" WHERE name = $1'
    SELECT_RARITY_POPULATION = 'SELECT rarities FROM "Gamemodes_Spawn_Rates" WHERE gamemode_name = $1'
    SELECT_RARITY_WEIGHT = 'SELECT spawn_rate FROM "Gamemodes_Spawn_Rates" WHERE gamemode_name = $1'

class qGameModesLootSlot:
    SELECT_ALL = 'SELECT * FROM "Gamemodes_Loot_Slot"'

class qGameModesSpawnRate:
    SELECT_ALL = 'SELECT * FROM "Gamemodes_Spawn_Rates"'

class qSlayers:
    COUNT = 'SELECT COUNT(*) FROM "Slayers"'
    SELECT_SLAYER = 'SELECT * FROM "Slayers" WHERE slayer_id = $1'
    SELECT_SLAYER_ITEMS = 'SELECT * FROM "Items" LEFT JOIN "Slayers_Slots" ON "Items".id = "Slayers_Slots".item_id WHERE "Slayers_Slots".slayer_id = $1'
    SELECT_SLAYER_ROW_INVENTORY = 'SELECT "Items".*, "Slayers_Inventory_Items".level, "Slayers_Inventory_Items".equipped FROM "Items" LEFT JOIN "Slayers_Inventory_Items" ON "Items".id = "Slayers_Inventory_Items".item_id WHERE "Slayers_Inventory_Items".slayer_id = $1'
    SELECT_SLAYER_INVENTORY = 'SELECT item_id FROM "Slayers_Inventory_Items" WHERE slayer_id = $1'
    SELECT_SLAYER_SPE_INVENTORY = 'SELECT specialization_list FROM "Slayers_Inventory_Specializations" WHERE slayer_id = $1'
    SELECT_SLAYER_SLOTS = 'SELECT slot, item_id FROM "Slayers_Slots" WHERE slayer_id = $1'
    SELECT_SLAYER_SPECIFIC_SLOT = 'SELECT item_id FROM "Slayers_Slots" WHERE slayer_id = $1, slot = $2'

class qChannels:
    SELECT_ALL = 'SELECT * FROM "Channels" WHERE mode = $1'
    SELECT_CHANNEL = 'SELECT channel_id FROM "Channels" WHERE mode = $1 AND name = $2'

class qBaseBonuses:
    SELECT_ALL = 'SELECT * FROM "Base_Bonuses_Slayers"'

class qItems:
    SELECT_RANDOM = 'SELECT * FROM "Items" WHERE rarity = $1 AND element =$2 AND slot = ANY($3::text[]) ORDER BY random() LIMIT 1'
    SELECT_ITEM = 'SELECT * FROM "Items" WHERE id = $1'

class qRarities:
    SELECT_ALL = 'SELECT * FROM "Rarities"'
    SELECT_DISPLAY = 'SELECT display_text, display_color FROM "Rarities" WHERE name = $1'
    SELECT_PRICE = 'SELECT price FROM "Rarities" WHERE name = $1'

class qRaritiesLootRates:
    SELECT_ALL = 'SELECT * FROM "Rarities_Loot_Rates"'
    SELECT_RARITIES = 'SELECT rarities FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'
    SELECT_WEIGHTS = 'SELECT loot_rate FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'

class qElements:
    SELECT_ALL = 'SELECT * FROM "Elements"'
    SELECT_DISPLAY = 'SELECT display_text, display_emote FROM "Elements" WHERE name = $1'

class qLootSlot:
    pass

class qSlayersInventoryItems:
    SELECT_ALREADY = 'SELECT 1 FROM "Slayers_Inventory_Items" WHERE slayer_id = $1 AND item_id = $2'

class qSlots:
    SELECT_ALL = 'SELECT * FROM "Slots"'

class qSpe:
    SELECT_SPE = 'SELECT * FROM "Specializations" WHERE id = $1'
    SELECT_ALL = 'SELECT * FROM "Specializations"'
