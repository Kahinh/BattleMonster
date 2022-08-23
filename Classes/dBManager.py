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
  
  async def pull_loots(self, data):
    requests = {}
    async with self.bot.db_pool.acquire() as conn:
      for slayer_id in data:
        requests[slayer_id] = []
        for row in data[slayer_id]:
          item = await conn.fetchrow('SELECT * FROM "Items" WHERE element = $1 AND rarity =$2 AND slot = ANY($3::text[]) ORDER BY random() LIMIT 1', row[0], row[1], row[2])
          requests[slayer_id].append(item)
    return requests

  async def push_loots(self, data):
    async with self.bot.db_pool.acquire() as conn:
      await conn.executemany('INSERT INTO "Slayers_Inventory_Items" (slayer_id, item_id, level, equipped) VALUES ($1, $2, $3, $4)', data)

  async def push_money(self, data):
    async with self.bot.db_pool.acquire() as conn:
      await conn.executemany('UPDATE "Slayers" SET money = money + $1 WHERE slayer_id = $2', data)

