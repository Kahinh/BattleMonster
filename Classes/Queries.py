class qMonsters:
    SELECT_ALL = 'SELECT * FROM Monsters'
    SELECT_RANDOM = 'SELECT * FROM "Monsters" WHERE rarity = $1 ORDER BY random() LIMIT 1'
    INSERT = 'INSERT INTO Monsters VALUES ($1, $2, $3)'

class qGameModes:
    SELECT_ALL = 'SELECT * FROM "Gamemodes" WHERE autospawn = True'
    SELECT_GAMEMODE = 'SELECT * FROM "Gamemodes" WHERE name = $1'
    SELECT_RARITY_POPULATION = 'SELECT rarities FROM "Gamemodes_Spawn_Rates" WHERE gamemode_name = $1'
    SELECT_RARITY_WEIGHT = 'SELECT spawn_rate FROM "Gamemodes_Spawn_Rates" WHERE gamemode_name = $1'

class qSlayers:
    COUNT = 'SELECT COUNT(*) FROM "Slayers"'
    SELECT_SLAYER = 'SELECT * FROM "Slayers" WHERE slayer_id = $1'
    SELECT_SLAYER_ITEMS = 'SELECT * FROM "Items" LEFT JOIN "Slayers_Slots" ON "Items".id = "Slayers_Slots".item_id WHERE "Slayers_Slots".slayer_id = $1'
    SELECT_SLAYER_INVENTORY = 'SELECT item_id FROM "Slayers_Inventory_Items" WHERE slayer_id = $1'
    SELECT_SLAYER_SPE_INVENTORY = 'SELECT specialization_id FROM "Slayers_Inventory_Specializations" WHERE slayer_id = $1'
    SELECT_SLAYER_SLOTS = 'SELECT slot, item_id FROM "Slayers_Slots" WHERE slayer_id = $1'

class qChannels:
    SELECT_CHANNEL = 'SELECT channel_id FROM "Channels" WHERE mode = $1 AND name = $2'

class qBaseBonuses:
    SELECT_BASE_BONUSES = 'SELECT * FROM "Base_Bonuses_Slayers"'

class qRaritiesLootRates:
    SELECT_RARITIES = 'SELECT rarities FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'
    SELECT_WEIGHTS = 'SELECT loot_rate FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'

class qItems:
    SELECT_RANDOM = 'SELECT * FROM "Items" WHERE rarity = $1 AND element =$2 ORDER BY random() LIMIT 1'

class qRarities:
    SELECT_DISPLAY = 'SELECT display_text, display_color FROM "Rarities" WHERE name = $1'
    SELECT_PRICE = 'SELECT price FROM "Rarities" WHERE name = $1'

class qElements:
    SELECT_DISPLAY = 'SELECT display_text, display_emote FROM "Elements" WHERE name = $1'

class qLootSlot:
    pass
