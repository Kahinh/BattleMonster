import lib
import datetime

class Commands_Slayer(lib.commands.GroupCog, name="slayer"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="inventaire")
  async def inventory(self, interaction: lib.discord.Interaction) -> None:
    """ Ouvre l'inventaire. Utilisez les menus déroulants pour accéder à un objet spécifique """
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    if len(Slayer.cSlayer.inventory_items) > 0:
        #On init le message
        view = lib.InventoryView(self.bot, Slayer, interaction)
        embed = lib.Embed.create_embed_item(self.bot, Slayer.cSlayer.inventory_items[list(Slayer.cSlayer.inventory_items.keys())[0]], Slayer)
        await self.bot.ActiveList.add_interface(interaction.user.id, "inventaire", view)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.response.send_message(content="Malheureusement, tu n'as pas d'objets dans ton inventaire !", ephemeral=True)

  @lib.app_commands.command(name="profil")
  async def stats(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche votre profil, comprenant vos statistiques et votre équipement """
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    embed = lib.Embed.create_embed_profil(Slayer, interaction.user.display_avatar)
    view = lib.SlayerView(self.bot, Slayer, interaction, interaction.user.display_avatar)
    await self.bot.ActiveList.add_interface(interaction.user.id, "profil", view)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

  @lib.app_commands.command(name="specialite")
  async def spe(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche les spécialités disponibles pour acheter ou équiper """
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    embed = lib.Embed.create_embed_spe(Slayer, self.bot.rSpe[0])
    view = lib.SpeView(self.bot, Slayer, interaction)
    await self.bot.ActiveList.add_interface(interaction.user.id, "inventaire_spe", view)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

  @lib.app_commands.command(name="regen")
  async def regen(self, interaction: lib.discord.Interaction) -> None:
    """ Permet de récupérer de la santé ou de ressuciter """
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    #C'est une Rez
    if Slayer.cSlayer.dead:
      waiting_time = 20 #7200
      #Si on a attendu suffisamment
      if datetime.datetime.timestamp(datetime.datetime.now()) - Slayer.cSlayer.lastregen >= waiting_time:
        #On rez
        Slayer.cSlayer.dead = False
        regen = Slayer.cSlayer.regen()
        await self.bot.dB.push_slayer_data(Slayer.cSlayer)
        await interaction.response.send_message(content=f"Résurrection effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
      else:
        await interaction.response.send_message(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine résurrection : **{int(Slayer.cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)
    #C'est une regen
    else:
      waiting_time = 10 #3600
      #Si on a attendu suffisamment
      if datetime.datetime.timestamp(datetime.datetime.now()) - Slayer.cSlayer.lastregen >= waiting_time:
        regen = Slayer.cSlayer.regen()
        await self.bot.dB.push_slayer_data(Slayer.cSlayer)
        await interaction.response.send_message(content=f"Régénération effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
      else:
        await interaction.response.send_message(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine régénération : **{int(Slayer.cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Slayer(bot))
  print("Commands_Slayer : √")