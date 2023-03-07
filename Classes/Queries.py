class qMonsters:
    SELECT_ALL = 'SELECT * FROM Monsters'
    SELECT_RANDOM_ADVANCED = 'SELECT * FROM "monsters" WHERE rarity = $1 AND element =$2 ORDER BY random() LIMIT 1'
    SELECT_RANDOM = 'SELECT * FROM "monsters" WHERE rarity = $1 ORDER BY random() LIMIT 1'
    INSERT = 'INSERT INTO Monsters VALUES ($1, $2, $3)'

class qGameModes:
    SELECT_ALL = 'SELECT * FROM "gamemodes"'
    SELECT_GAMEMODE = 'SELECT * FROM "gamemodes" WHERE name = $1'
    SELECT_RARITY_POPULATION = 'SELECT rarities FROM "gamemodes_spawn_rates WHERE gamemode_name = $1'
    SELECT_RARITY_WEIGHT = 'SELECT spawn_rate FROM "gamemodes_spawn_rates WHERE gamemode_name = $1'

class qGameModesLootSlot:
    SELECT_ALL = 'SELECT * FROM "gamemodes_loot_slot"'

class qGameModesSpawnRate:
    SELECT_ALL = 'SELECT * FROM "gamemodes_spawn_rates"'

class qSlayers:
    COUNT = 'SELECT COUNT(*) FROM "slayers"'
    SELECT_SLAYER = 'SELECT * FROM "slayers" LEFT JOIN "slayers_achievements" ON "slayers_achievements".id = "slayers".id WHERE "slayers".id = $1'
    SELECT_SLAYER_ITEMS = 'SELECT * FROM "items" LEFT JOIN "Slayers_Slots" ON "items".id = "Slayers_Slots".id WHERE "Slayers_Slots".id = $1'
    SELECT_SLAYER_ROW_INVENTORY = 'SELECT "items".*, "slayers_inventory_items".level, "slayers_inventory_items".equipped FROM "items" LEFT JOIN "slayers_inventory_items" ON "items".id = "slayers_inventory_items".item_id WHERE "slayers_inventory_items".slayer_id = $1'
    SELECT_SLAYER_INVENTORY = 'SELECT id FROM "slayers_inventory_items" WHERE id = $1'
    SELECT_SLAYER_SPE_INVENTORY = 'SELECT specialization_list FROM "slayers_inventory_specializations" WHERE slayer_id = $1'
    SELECT_SLAYER_SLOTS = 'SELECT slot, id FROM "Slayers_Slots" WHERE id = $1'
    SELECT_SLAYER_SPECIFIC_SLOT = 'SELECT id FROM "Slayers_Slots" WHERE id = $1, slot = $2'

class qChannels:
    SELECT_ALL = 'SELECT * FROM "channels" WHERE mode = $1'
    SELECT_CHANNEL = 'SELECT channel_id FROM "channels" WHERE mode = $1 AND name = $2'

class qBaseBonuses:
    SELECT_ALL = 'SELECT * FROM "base_bonuses_slayers"'

class qItems:
    SELECT_RANDOM = 'SELECT * FROM "items" WHERE rarity = $1 AND element =$2 AND slot = ANY($3::text[]) ORDER BY random() LIMIT 1'
    SELECT_ITEM = 'SELECT * FROM "items" WHERE id = $1'

class qRarities:
    SELECT_ALL = 'SELECT * FROM "rarities"'
    SELECT_DISPLAY = 'SELECT display_text, display_color FROM "rarities" WHERE name = $1'
    SELECT_PRICE = 'SELECT price FROM "rarities" WHERE name = $1'

class qRaritiesLootRates:
    SELECT_ALL = 'SELECT * FROM "Rarities_Loot_Rates"'
    SELECT_RARITIES = 'SELECT rarities FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'
    SELECT_WEIGHTS = 'SELECT loot_rate FROM "Rarities_Loot_Rates" WHERE rarities_name = $1'

class qElements:
    SELECT_ALL = 'SELECT * FROM "elements"'
    SELECT_DISPLAY = 'SELECT display_text, display_emote FROM "elements" WHERE name = $1'

class qLootSlot:
    pass

class qSlayersInventoryItems:
    SELECT_ALREADY = 'SELECT 1 FROM "slayers_inventory_items" WHERE id = $1 AND id = $2'

class qSlots:
    SELECT_ALL = 'SELECT * FROM "slots"'

class qSpe:
    SELECT_SPE = 'SELECT * FROM "specializations" WHERE id = $1'
    SELECT_ALL = 'SELECT * FROM "specializations"'

class qGatherables:
    SELECT_ALL = 'SELECT * FROM "gatherables"'

class qGatherables_Spawn:
    SELECT_ALL = 'SELECT * FROM "gatherables_spawn"'
