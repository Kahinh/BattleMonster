from ssl import Options
from discord import Role
import lib

@lib.app_commands.default_permissions(administrator=True)
class Commands_Admin(lib.commands.GroupCog, name="admin"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="savebdd")
  async def savebdd(self, interaction: lib.discord.Interaction) -> None:
    """ Admin Only - Commande afin de lancer une save de la BDD avant un reboot du Bot Discord. """
    logs = self.bot.slayers_list
    await interaction.response.send_message(f"{logs}", ephemeral=True)

  @lib.app_commands.describe(rarity='Rareté du Monstre à apparaître')
  @lib.app_commands.describe(gamemode='Config du Gamemode')
  @lib.app_commands.choices(
    rarity=[
      lib.Choice(name='Commun', value="common"),
      lib.Choice(name='Rare', value="rare"),
      lib.Choice(name='Épique', value="epic"),
      lib.Choice(name='Légendaire', value="legendary")
    ],
    gamemode=[
      lib.Choice(name='Chasse', value="hunts"),
      lib.Choice(name='Event Gold', value="gold_event")
    ])
  @lib.app_commands.command(name="spawnmonster")
  async def spawnmonster(self, interaction: lib.discord.Interaction, rarity: lib.Choice[str], gamemode: lib.Choice[str]) -> None:
    """ Admin Only - Commande afin de faire apparaître un monstre. """

    rGamemode = await self.bot.db_pool.fetchrow(lib.qGameModes.SELECT_GAMEMODE, gamemode.value)
    embed, view, rChannels = await lib.Battle_Functions.create_battle(self, rGamemode, rarity.value)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)


async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Admin(bot))
  print("Commands_Admin : √")