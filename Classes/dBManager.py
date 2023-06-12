import logging
logging.basicConfig(filename='logs.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s') 

class dB:
  def __init__(self, bot):
    self.bot = bot

  async def pull_slayer_data(self, Slayer_id):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
          Slayer_Data = await conn.fetchrow('SELECT * FROM "slayers" WHERE "slayers".id = $1', Slayer_id)
          Slayer_Inventory = await conn.fetch('SELECT "items".*, "slayers_inventory_items".level, "slayers_inventory_items".equipped FROM "items" LEFT JOIN "slayers_inventory_items" ON "items".id = "slayers_inventory_items".item_id WHERE "slayers_inventory_items".slayer_id = $1', Slayer_id)
          Slayer_Gatherables = await conn.fetch('SELECT * FROM "slayers_inventory_gatherables" WHERE slayer_id = $1', Slayer_id)
          Slayer_Spe_Inventory = await conn.fetchrow('SELECT specialization_list FROM "slayers_inventory_specializations" WHERE slayer_id = $1', Slayer_id)
          Slayer_Achievements = await conn.fetch('SELECT * FROM slayers_achievements WHERE slayer_id = $1', Slayer_id)
          Slayer_Loadouts = await conn.fetch('SELECT * FROM slayers_loadouts WHERE slayer_id = $1', Slayer_id)
    logging.info(f"PULL SLAYER_DATA : {Slayer_id}")
    return Slayer_Data, Slayer_Inventory, Slayer_Spe_Inventory, Slayer_Gatherables, Slayer_Achievements, Slayer_Loadouts

  async def equip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = True WHERE slayer_id = {cSlayer.id} AND item_id = {cItem.id}')

  async def unequip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = False WHERE slayer_id = {cSlayer.id} AND item_id = {cItem.id}')
  
  async def equip_unequip_mass_update(self, mass_update_data):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
          await conn.executemany(f'UPDATE "slayers_inventory_items" SET equipped = $3 WHERE slayer_id = $1 AND item_id = $2', mass_update_data)

  async def pull_OpponentLootTable(self, monster, lootslot):
    async with self.bot.db_pool.acquire() as conn:
      loottable = await conn.fetch('SELECT * FROM "items" WHERE monster = $1 AND slot = ANY($2::text[])', monster, lootslot)
    return loottable

  async def push_loots_executemany(self, data_loots):
    if data_loots != []:
      async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany('INSERT INTO "slayers_inventory_items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', data_loots) 

    logging.info(f"PUSH LOOTS : {data_loots}")

  async def push_money_executemany(self, data_money):
    if data_money != []:
      async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany('UPDATE "slayers" SET money = money + $1 WHERE id = $2', data_money)
      
      print(f"PUSH MONEY : {data_money}")

  async def push_money(self, slayer_id, amount): 
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
          await conn.execute('UPDATE "slayers" SET money = money + $1 WHERE id = $2', amount, slayer_id)

  async def push_spe(self, slayer_id, spe_id): 
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
          await conn.execute('UPDATE "slayers" SET specialization = $1 WHERE id = $2', spe_id, slayer_id)

  async def push_special_stacks(self, slayer_id, special_stacks):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
          await conn.execute('UPDATE "slayers" SET special_stacks = $1 WHERE id = $2', special_stacks, slayer_id)

  async def push_slayer_data(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers" (id, xp, money, damage_taken, special_stacks, faction, creation_date, name, dead, gearscore)' \
            f" VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 0)" \
            ' ON CONFLICT (id) DO ' \
            f"UPDATE SET xp=$2, money=$3, damage_taken=$4, special_stacks=$5, faction=$6, dead=$9, gearscore=$10", cSlayer.id, cSlayer.xp, cSlayer.money, cSlayer.damage_taken, cSlayer.special_stacks, int(cSlayer.faction), cSlayer.creation_date, cSlayer.name, cSlayer.dead, cSlayer.gearscore)

    logging.info(f"PUSH SLAYER_DATA : {cSlayer}")

  async def push_damage_taken(self, slayer_id, damage_taken):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('UPDATE "slayers" SET damage_taken = $1 where id = $2', damage_taken, slayer_id)

  async def get_itemrow_by_name(self, item_name):
    async with self.bot.db_pool.acquire() as conn:
      item_row = await conn.fetchrow('SELECT * FROM "items" WHERE name = $1', item_name)
    return item_row
  
  async def add_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers_inventory_items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', cSlayer.id, cItem.id, 1, False)

    logging.info(f"PUSH ADD_ITEM : {cSlayer.id} {cItem.id}")
  
  async def push_spe_list(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers_inventory_specializations" (slayer_id, specialization_list)' \
            f" VALUES ($1, $2)" \
            ' ON CONFLICT (slayer_id) DO ' \
            f"UPDATE SET specialization_list=$2", cSlayer.id, str(cSlayer.inventories["specializations"]))
    
    logging.info(f"PUSH SPE_LIST : {cSlayer.id} {str(cSlayer.inventory_specializations)}")
  
  async def get_rPet(self, pet_id):
    async with self.bot.db_pool.acquire() as conn:
      rPet = await conn.fetchrow('SELECT * FROM "items" WHERE id = $1', pet_id)

    logging.info(f"PULL - GET_PET : {pet_id}")
    return rPet
  
  async def push_Gather(self, slayer_id, gatherable_id, amount):
    async with self.bot.db_pool.acquire() as conn :
      await conn.execute('INSERT INTO "slayers_inventory_gatherables" (slayer_id, gatherable_id, amount)' \
        ' VALUES ($1, $2, $3)' \
        ' ON CONFLICT ON CONSTRAINT slayer_and_gatherable_unique' \
        ' DO UPDATE' \
        ' SET amount = $3', slayer_id, gatherable_id, amount)
      
    logging.info(f"PUSH - SLAYERS_INVENTORY_GATHERABLES : {slayer_id} {gatherable_id} {amount}")

  async def push_update_item_level(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('UPDATE slayers_inventory_items' \
        ' SET level = $1' \
        ' WHERE slayers_inventory_items.slayer_id = $2 AND slayers_inventory_items.item_id = $3', cItem.level, cSlayer.id, cItem.id)
      
    logging.info(f"PUSH - SLAYERS_INVENTORY_ITEMS LEVEL : {cSlayer.id} {cItem.id} {cItem.level}")

  async def push_MythicStones(self, data_mythic_stones):
    if data_mythic_stones != []:  
      async with self.bot.db_pool.acquire() as conn :
        await conn.executemany('INSERT INTO "slayers_inventory_gatherables" (slayer_id, gatherable_id, amount)' \
          ' VALUES ($1, $2, $3)' \
          ' ON CONFLICT ON CONSTRAINT slayer_and_gatherable_unique' \
          ' DO UPDATE' \
          ' SET amount = $3 + slayers_inventory_gatherables.amount', data_mythic_stones)
  
      print(f"PUSH - MYTHIC STONES : {data_mythic_stones}")

  async def pull_OpponentData(self, rarity, element, type):
    async with self.bot.db_pool.acquire() as conn:
      OpponentData = await conn.fetchrow('SELECT * FROM "monsters" WHERE rarity = $1 AND element =$2 AND type =$3 ORDER BY random() LIMIT 1', rarity, element, type) 
    return OpponentData
  
  async def pull_GamemodeLootSlot(self, gamemode_name):
    async with self.bot.db_pool.acquire() as conn:
      GamemodeLootSlot = await conn.fetch('SELECT * FROM "gamemodes_loot_slot" WHERE gamemode = $1', gamemode_name)
    return GamemodeLootSlot
  
  async def pullGamemodeSpawnRate(self, gamemode_name):
    async with self.bot.db_pool.acquire() as conn:
      GamemodeSpawnRate = await conn.fetch('SELECT * FROM "gamemodes_spawn_rates" WHERE gamemode = $1', gamemode_name)
    return GamemodeSpawnRate

  async def push_Achievement(self, slayer_id, achievement, value):
    async with self.bot.db_pool.acquire() as conn :
      await conn.execute('INSERT INTO slayers_achievements (slayer_id, achievement, value)' \
        ' VALUES ($1, $2, $3)' \
        ' ON CONFLICT ON CONSTRAINT slayer_and_achievement_unique' \
        ' DO UPDATE' \
        ' SET value = $3', slayer_id, achievement, value)

  async def push_Achievement_Executemany(self, achievement_data):
    async with self.bot.db_pool.acquire() as conn :
      await conn.executemany('INSERT INTO slayers_achievements (slayer_id, achievement, value)' \
        ' VALUES ($1, $2, $3)' \
        ' ON CONFLICT ON CONSTRAINT slayer_and_achievement_unique' \
        ' DO UPDATE' \
        ' SET value = $3', (achievement_data))
    print(f"PUSH - ACHIEVEMENTS : {achievement_data}")
  
  async def pull_spe_data(self, spe_id):
    async with self.bot.db_pool.acquire() as conn :
      spe_data = await conn.fetchrow("SELECT * FROM specializations WHERE id = $1", spe_id)
    return spe_data

  async def push_behemoths_killed_achievement(self, data_behemoths_killed_achievement):
    if data_behemoths_killed_achievement != []: 
      async with self.bot.db_pool.acquire() as conn:   
          await conn.executemany('INSERT INTO slayers_achievements (slayer_id, achievement, value)' \
            ' VALUES ($1, $2, $3)' \
            ' ON CONFLICT ON CONSTRAINT slayer_and_achievement_unique' \
            ' DO UPDATE' \
            ' SET value = $3',data_behemoths_killed_achievement)

      print(f"PUSH - ACHIEVEMENTS : {data_behemoths_killed_achievement}")
          
  async def push_creation_loadouts(self, slayer_id, name, loadout_list):
    async with self.bot.db_pool.acquire() as conn:   
        id = await conn.fetchval('INSERT INTO slayers_loadouts (slayer_id, name, loadout)' \
          ' VALUES ($1, $2, $3) RETURNING id', slayer_id, name, str(loadout_list), column=0)
    return id

  async def push_update_loadouts(self, loadout_id, slayer_id, name, loadout_list):
    async with self.bot.db_pool.acquire() as conn:   
        await conn.execute('UPDATE slayers_loadouts SET slayer_id = $1, name = $2, loadout = $3' \
          ' WHERE id = $4', slayer_id, name, str(loadout_list), loadout_id)
    return id