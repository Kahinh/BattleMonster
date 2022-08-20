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
