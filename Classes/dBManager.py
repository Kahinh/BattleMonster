class dB:
  def __init__(
    self,
    bot
    ):
    self.bot = bot

  async def sell_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'DELETE FROM "slayers_inventory_items" WHERE slayer_id = {cSlayer.id} AND id = {cItem.id}')
            await conn.execute(f'UPDATE "slayers" SET money = money + {self.bot.rRarities[cItem.rarity]["price"]} WHERE item_id = {cSlayer.id}')

  async def equip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = True WHERE slayer_id = {cSlayer.id} AND item_id = {cItem.id}')
            await conn.execute(f'UPDATE "slayers" SET damage_taken = {cSlayer.damage_taken} WHERE id = {cSlayer.id}')

  async def unequip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = False WHERE slayer_id = {cSlayer.id} AND item_id = {cItem.id}')
            await conn.execute(f'UPDATE "slayers" SET damage_taken = {cSlayer.damage_taken} WHERE id = {cSlayer.id}')

  async def switch_item(self, cSlayer, cItem1, cItem2):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = True WHERE slayer_id = {cSlayer.id} AND item_id = {cItem1.id}')
            await conn.execute(f'UPDATE "slayers_inventory_items" SET equipped = False WHERE slayer_id = {cSlayer.id} AND item_id = {cItem2.id}')
            await conn.execute(f'UPDATE "slayers" SET damage_taken = {cSlayer.damage_taken} WHERE id = {cSlayer.id}')
  
  async def pull_loottable(self, monster, lootslot):
    async with self.bot.db_pool.acquire() as conn:
      loottable = await conn.fetch('SELECT * FROM "items" WHERE monster = $1 AND slot = ANY($2::text[])', monster, lootslot)
    return loottable
  
  async def push_behemoths_killed_achievement(self, data_behemoths_killed_achievement):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        if data_behemoths_killed_achievement != []:    
          await conn.executemany('UPDATE "slayers_achievements" SET monsters_killed = monsters_killed + $1 WHERE id = $2', data_behemoths_killed_achievement)

  async def push_biggest_hit_achievement(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():   
        await conn.execute('UPDATE "slayers_achievements" SET biggest_hit = + $1 WHERE id = $2', cSlayer.achievements["biggest_hit"], cSlayer.id)

  async def push_loots_money(self, data_loots, data_money):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        if data_loots != []:
          await conn.executemany('INSERT INTO "slayers_inventory_items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', data_loots)
        if data_money != []:
          await conn.executemany('UPDATE "slayers" SET money = money + $1 WHERE id = $2', data_money)
  
  async def push_slayer_data(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers" (id, xp, money, damage_taken, special_stacks, faction, specialization, creation_date, name, dead, gearscore)' \
            f" VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 0)" \
            ' ON CONFLICT (id) DO ' \
            f"UPDATE SET xp=$2, money=$3, damage_taken=$4, special_stacks=$5, faction=$6, specialization=$7, dead=$10, gearscore=$11", cSlayer.id, cSlayer.xp, cSlayer.money, cSlayer.damage_taken, cSlayer.special_stacks, cSlayer.faction, cSlayer.specialization, cSlayer.creation_date, cSlayer.name, cSlayer.dead, cSlayer.gearscore)

  async def push_achievement_data(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers_achievements" (id) VALUES ($1)', cSlayer.id)

  async def get_itemrow(self, item_name):
    async with self.bot.db_pool.acquire() as conn:
      item_row = await conn.fetchrow('SELECT * FROM "items" WHERE name = $1', item_name)
    return item_row
  
  async def add_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers_inventory_items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', cSlayer.id, cItem.id, 1, False)
  
  async def push_spe_list(self, cSlayer):
    async with self.bot.db_pool.acquire() as conn:
      await conn.execute('INSERT INTO "slayers_inventory_specializations" (slayer_id, specialization_list)' \
            f" VALUES ($1, $2)" \
            ' ON CONFLICT (slayer_id) DO ' \
            f"UPDATE SET specialization_list=$2", cSlayer.id, str(cSlayer.inventory_specializations))
  
  async def get_rPet(self, pet_id):
    async with self.bot.db_pool.acquire() as conn:
      rPet = await conn.fetchrow('SELECT * FROM "items" WHERE id = $1', pet_id)
    return rPet
