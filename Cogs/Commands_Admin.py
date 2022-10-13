from ast import Str
from numbers import Number
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

  @lib.app_commands.describe(
      user='ID User to revive',
  )
  @lib.app_commands.command(name="heal")
  async def heal(self, interaction: lib.discord.Interaction, user: str) -> None:
    """ Retire tous les dégâts subis par un joueur et le ressuciter """
    try: 
      Slayer = self.bot.ActiveList.get_active_Slayer(int(user))
    except: 
      Slayer = None
    if Slayer is not None:
      Slayer.cSlayer.dead = False
      Slayer.cSlayer.damage_taken = 0
      await self.bot.dB.push_slayer_data(Slayer.cSlayer)
      await interaction.response.send_message(content=f"{Slayer.cSlayer.name} a été réanimé !", ephemeral=True)
      channel = self.bot.get_channel(self.bot.rChannels["logs"])
      await channel.send(content=f"<@{Slayer.cSlayer.slayer_id}> a été réanimé par <@{interaction.user.id}>!")
    else:
      await interaction.response.send_message(content=f"{user} n'existe pas", ephemeral=True)

  @lib.app_commands.describe(
      user='ID User to revive',
      item_name='Item name to be given'
  )
  @lib.app_commands.command(name="give")
  async def give(self, interaction: lib.discord.Interaction, user: str, item_name: str) -> None:
    """ Offre un objet dans l'inventaire d'un joueur """
    Slayer = self.bot.ActiveList.get_active_Slayer(int(user))
    try: 
      Slayer = self.bot.ActiveList.get_active_Slayer(int(user))
    except: 
      Slayer = None
    if Slayer is not None:
      item_row = await self.bot.dB.get_itemrow(item_name)
      if item_row is not None:
        if Slayer.isinInventory(item_row["id"]):
          await interaction.response.send_message(content=f"{user} possède déjà {item_name}", ephemeral=True)
        else:
          cItem = lib.Item(item_row)
          Slayer.addtoInventory(cItem)
          await self.bot.dB.add_item(Slayer.cSlayer, cItem)
          await interaction.response.send_message(content=f"{item_name} a été donné à {user}", ephemeral=True)
          channel = self.bot.get_channel(self.bot.rChannels["logs"])
          await channel.send(content=f"<@{Slayer.cSlayer.slayer_id}> a obtenu {item_name} de la part de <@{interaction.user.id}>!")
      else:
        await interaction.response.send_message(content=f"{item_name} n'existe pas", ephemeral=True)
    else:
      await interaction.response.send_message(content=f"{user} n'existe pas", ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Admin(bot))
  print("Commands_Admin : √")