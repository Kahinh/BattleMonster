from ast import Str
from numbers import Number
import lib

@lib.app_commands.default_permissions(administrator=True)
class Commands_Admin(lib.commands.GroupCog, name="admin"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.choices(
  data=[
    lib.Choice(name='Gamemodes & Monsters Data', value="monsters"),
    lib.Choice(name='Slayers Data', value="slayers")
  ])
  @lib.app_commands.command(name="updatebot")
  async def updatebot(self, interaction: lib.discord.Interaction, data: lib.Choice[str]) -> None:
    """ Admin Only - Commande afin de lancer un update du Bot. """
    await interaction.response.defer(ephemeral=True)
    if data.value == "monsters":
      await self.bot.update_bot()
    else:
      self.bot.ActiveList.obsolete_interfaces()
      self.bot.ActiveList.reset_slayers_activelist()
      await self.bot.update_bot()
    await interaction.followup.send(f"Update {data.name} réalisée !", ephemeral=True)

  @lib.app_commands.choices(
    power=[
      lib.Choice(name='OFF', value="OFF"),
      lib.Choice(name='ON', value="ON")
    ],
    reset=[
      lib.Choice(name='RESET', value="RESET"),
      lib.Choice(name='RESUME', value="RESUME")
    ])
  @lib.app_commands.command(name="power")
  async def power(self, interaction: lib.discord.Interaction, power: lib.Choice[str], reset: lib.Choice[str]) -> None:
    """ ON/OFF """
    await interaction.response.defer(ephemeral=True)
    if power.value == "OFF":
      self.bot.power = False
      if reset.value == "RESET":
        self.bot.ActiveList.obsolete_interfaces()
        await self.bot.ActiveList.clear_all_battles()
        await self.bot.ActiveList.clear_all_recap()
    else:
      self.bot.power = True
    await interaction.followup.send(content=f"BOT : {power.value} / RESET BATTLES : {reset.value}", ephemeral=True)

  @lib.app_commands.command(name="event")
  async def event(self, interaction: lib.discord.Interaction) -> None:
    """ Admin Only - Commande afin de faire apparaître un monstre. """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      view = lib.CmdEvent(self.bot, self.bot.rGamemodes, interaction)
      await interaction.followup.send(content="Quel event faire apparaître ?", view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.describe(
      user='ID User to revive',
  )
  @lib.app_commands.command(name="heal")
  async def heal(self, interaction: lib.discord.Interaction, user: str) -> None:
    """ Retire tous les dégâts subis par un joueur et le ressuciter """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      try: 
        Slayer = self.bot.ActiveList.get_active_Slayer(int(user))
      except: 
        Slayer = None
      if Slayer is not None:
        Slayer.cSlayer.dead = False
        Slayer.cSlayer.damage_taken = 0
        await self.bot.dB.push_slayer_data(Slayer.cSlayer)
        await self.bot.ActiveList.update_interface(Slayer.cSlayer.id, "profil")
        await interaction.followup.send(content=f"{Slayer.cSlayer.name} a été réanimé !", ephemeral=True)
        channel = self.bot.get_channel(self.bot.rChannels["logs"])
        await channel.send(content=f"<@{Slayer.cSlayer.id}> a été réanimé par <@{interaction.user.id}>!")
      else:
        await interaction.followup.send(content=f"{user} n'existe pas", ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.describe(
      user='ID User',
      item_name='Item name to be given'
  )
  @lib.app_commands.command(name="give")
  async def give(self, interaction: lib.discord.Interaction, user: str, item_name: str) -> None:
    """ Offre un objet dans l'inventaire d'un joueur """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      try: 
        Slayer = self.bot.ActiveList.get_active_Slayer(int(user))
      except: 
        Slayer = None
      if Slayer is not None:
        item_row = await self.bot.dB.get_itemrow(item_name)
        if item_row is not None:
          if Slayer.isinInventory(item_row["id"]):
            await interaction.followup.send(content=f"{user} possède déjà {item_name}", ephemeral=True)
          else:
            cItem = lib.Item(item_row, self.bot)
            Slayer.addtoInventory(cItem)
            await self.bot.dB.add_item(Slayer.cSlayer, cItem)
            await self.bot.ActiveList.update_interface(Slayer.cSlayer.id, "inventaire")
            await interaction.followup.send(content=f"{item_name} a été donné à {user}", ephemeral=True)
            channel = self.bot.get_channel(self.bot.rChannels["logs"])
            await channel.send(content=f"<@{Slayer.cSlayer.id}> a obtenu {item_name} de la part de <@{interaction.user.id}>!")
        else:
          await interaction.followup.send(content=f"{item_name} n'existe pas", ephemeral=True)
      else:
        await interaction.followup.send(content=f"{user} n'existe pas", ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")
      
async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Admin(bot))
  lib.logging.warning("Commands_Admin : OK")