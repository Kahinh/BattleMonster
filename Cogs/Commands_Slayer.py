import lib

class Commands_Slayer(lib.commands.GroupCog, name="slayer"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="inventory")
  async def inventory(self, interaction: lib.discord.Interaction) -> None:
    """ Commande afin d'afficher l'inventaire du Slayer """
    if interaction.user.id not in self.bot.active_cSlayer:
      async with self.bot.db_pool.acquire() as conn:
        async with conn.transaction():
          rItemsSlayer = await conn.fetch(lib.qSlayers.SELECT_SLAYER_ROW_INVENTORY, interaction.user.id)
      if rItemsSlayer != None:
        #On init le Slayer
        Slayer = lib.MSlayer(self.bot, interaction)
        await Slayer.constructClass()

        #on ajoute le cSlayer dans les activeSlayer
        self.bot.active_cSlayer[Slayer.cSlayer.slayer_id] = {}
        self.bot.active_cSlayer[Slayer.cSlayer.slayer_id]["class"] = Slayer
        self.bot.active_cSlayer[Slayer.cSlayer.slayer_id]["interfaces"] = {}
        self.bot.active_cSlayer[Slayer.cSlayer.slayer_id]["interfaces"]["inventory"] = True

        #On init le message
        view = lib.InventoryView(self.bot, Slayer, interaction)
        embed = lib.Embed.create_embed_item(self.bot, Slayer.cSlayer.inventory_items[0])
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
      else:
        await interaction.response.send_message(content="Malheureusement, tu n'as pas d'objets dans ton inventaire !", ephemeral=True)
    else:
      await interaction.response.send_message(content="Une interface inventaire est déjà ouverte", ephemeral=True)

  @lib.app_commands.command(name="stats")
  async def stats(self, interaction: lib.discord.Interaction) -> None:
    """ Commande afin d'afficher les stats du Slayer """
    await interaction.response.send_message(f"En cours", ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Slayer(bot))
  print("Commands_Slayer : √")