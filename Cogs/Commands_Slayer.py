import lib
import datetime

class Commands_Slayer(lib.commands.GroupCog, name="slayer"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="inventaire")
  async def inventory(self, interaction: lib.discord.Interaction) -> None:
    """ Ouvre l'inventaire. Utilisez les menus déroulants pour accéder à un objet spécifique """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      if len(Slayer.cSlayer.inventory_items) > 0:
          #On init le message
          itemsequipped_list = Slayer.getListEquippedOnSlot(Slayer.cSlayer.inventory_items[list(Slayer.cSlayer.inventory_items.keys())[0]].slot)
          itemID_compare = Slayer.cSlayer.inventory_items[list(Slayer.cSlayer.inventory_items.keys())[0]].item_id
          view = lib.InventoryView(self.bot, Slayer, interaction, itemsequipped_list, itemID_compare)
          embed = lib.Embed.create_embed_item(self.bot, Slayer.cSlayer.inventory_items[list(Slayer.cSlayer.inventory_items.keys())[0]], Slayer, itemsequipped_list[0] if itemsequipped_list != [] else None)
          await self.bot.ActiveList.add_interface(interaction.user.id, "inventaire", view)
          await interaction.followup.send(embed=embed, view=view, ephemeral=True)
      else:
        await interaction.followup.send(content="Malheureusement, tu n'as pas d'objets dans ton inventaire !", ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="profil")
  async def stats(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche votre profil, comprenant vos statistiques et votre équipement """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      embed = lib.Embed.create_embed_profil(Slayer, interaction.user.display_avatar)
      view = lib.SlayerView(self.bot, Slayer, interaction, interaction.user.display_avatar)
      await self.bot.ActiveList.add_interface(interaction.user.id, "profil", view)
      await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="specialite")
  async def spe(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche les spécialités disponibles pour acheter ou équiper """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      embed = lib.Embed.create_embed_spe(Slayer, lib.Toolbox.get_spe_row_by_id(self.bot.rSpe, 1))
      view = lib.SpeView(self.bot, Slayer, interaction)
      await self.bot.ActiveList.add_interface(interaction.user.id, "inventaire_spe", view)
      await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="regen")
  async def regen(self, interaction: lib.discord.Interaction) -> None:
    """ Permet de récupérer de la santé ou de ressuciter """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      if Slayer.cSlayer.damage_taken > 0:
        #C'est une Rez
        if Slayer.cSlayer.dead:
          waiting_time = 1200 #7200
          #Si on a attendu suffisamment
          if datetime.datetime.timestamp(datetime.datetime.now()) - Slayer.cSlayer.lastregen >= waiting_time:
            #On rez
            Slayer.cSlayer.lastregen = datetime.datetime.timestamp(datetime.datetime.now())
            Slayer.cSlayer.dead = False
            regen = Slayer.cSlayer.regen()
            await self.bot.dB.push_slayer_data(Slayer.cSlayer)
            await interaction.followup.send(content=f"Résurrection effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
          else:
            await interaction.followup.send(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine résurrection : **{int(Slayer.cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)
        #C'est une regen
        else:
          waiting_time = 600 #3600
          #Si on a attendu suffisamment
          if datetime.datetime.timestamp(datetime.datetime.now()) - Slayer.cSlayer.lastregen >= waiting_time:
            regen = Slayer.cSlayer.regen()
            Slayer.cSlayer.lastregen = datetime.datetime.timestamp(datetime.datetime.now())
            await self.bot.dB.push_slayer_data(Slayer.cSlayer)
            await interaction.followup.send(content=f"Régénération effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
          else:
            await interaction.followup.send(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine régénération : **{int(Slayer.cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)
      else:
        await interaction.followup.send(content=f"Tu n'as pas besoin de te soigner !", ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Slayer(bot))
  print("Commands_Slayer : √")