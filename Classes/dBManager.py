class dB:
  def __init__(
    self,
    bot
    ):
    self.bot = bot

  async def sell_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'DELETE FROM "Slayers_Inventory_Items" WHERE slayer_id = {cSlayer.slayer_id} AND item_id = {cItem.item_id}')
            await conn.execute(f'UPDATE "Slayers" SET money = money + {self.bot.rRarities[cItem.rarity]["price"]} WHERE slayer_id = {cSlayer.slayer_id}')
  async def equip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "Slayers_Inventory_Items" SET equipped = True WHERE slayer_id = {cSlayer.slayer_id} AND item_id = {cItem.item_id}')
            await conn.execute(f'UPDATE "Slayers" SET damage_taken = {cSlayer.damage_taken} WHERE slayer_id = {cSlayer.slayer_id}')

  async def unequip_item(self, cSlayer, cItem):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "Slayers_Inventory_Items" SET equipped = False WHERE slayer_id = {cSlayer.slayer_id} AND item_id = {cItem.item_id}')
            await conn.execute(f'UPDATE "Slayers" SET damage_taken = {cSlayer.damage_taken} WHERE slayer_id = {cSlayer.slayer_id}')

  async def switch_item(self, cSlayer, cItem1, cItem2):
    async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(f'UPDATE "Slayers_Inventory_Items" SET equipped = True WHERE slayer_id = {cSlayer.slayer_id} AND item_id = {cItem1.item_id}')
            await conn.execute(f'UPDATE "Slayers_Inventory_Items" SET equipped = False WHERE slayer_id = {cSlayer.slayer_id} AND item_id = {cItem2.item_id}')
            await conn.execute(f'UPDATE "Slayers" SET damage_taken = {cSlayer.damage_taken} WHERE slayer_id = {cSlayer.slayer_id}')
  
  async def pull_loottable(self, element, rarity, lootslot):
    async with self.bot.db_pool.acquire() as conn:
      loottable = await conn.fetch('SELECT * FROM "Items" WHERE element = $1 AND rarity =$2 AND slot = ANY($3::text[])', element, rarity, lootslot)
    return loottable

  async def push_loots_money(self, data_loots, data_money):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        if data_loots != []:
          await conn.executemany('INSERT INTO "Slayers_Inventory_Items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', data_loots)
        if data_money != []:
          await conn.executemany('UPDATE "Slayers" SET money = money + $1 WHERE slayer_id = $2', data_money)

