import lib

@lib.app_commands.default_permissions(administrator=True)
class Commands_Admin(lib.commands.GroupCog, name="admin"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="updatebot")
  async def updatebot(self, interaction: lib.discord.Interaction) -> None:
    """ Admin Only - Commande afin de lancer un update du Bot. """
    await self.bot.update_bot()
    await interaction.response.send_message(f"Update réalisée !", ephemeral=True)

  @lib.app_commands.choices(
    gamemode=[
      lib.Choice(name='Chasse', value="hunts"),
      lib.Choice(name='Event Gold', value="gold_event")
    ])
  @lib.app_commands.command(name="spawnmonster")
  async def spawnmonster(self, interaction: lib.discord.Interaction, gamemode: lib.Choice[str]) -> None:
    """ Admin Only - Commande afin de faire apparaître un monstre. """

    rGamemode = await self.bot.db_pool.fetchrow(lib.qGameModes.SELECT_GAMEMODE, gamemode.value)
    #On crée la class et on construit
    Battle = lib.Battle(self.bot, rGamemode, interaction)
    await Battle.constructGamemode()

  @lib.app_commands.command(name="test")
  async def updatebot(self, interaction: lib.discord.Interaction) -> None:
    """ Test. """
    data = ([("commun", "blaze", ["weapon"]),("legendary", "blaze", ["weapon"])])
    query = await self.bot.dB.pull_loots(data)
    print(query)
    await interaction.response.send_message(f"C'est fait !", ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Admin(bot))
  print("Commands_Admin : √")