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
      cSlayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      if len(cSlayer.inventories["items"]) > 0:
          #On init le message
          view = lib.InventoryView(self.bot, cSlayer, interaction)
          embed = view.get_embed()
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
      cSlayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      embed = lib.Embed.create_embed_profil_global(cSlayer, interaction.user.display_avatar)
      view = lib.SlayerView(self.bot, cSlayer, interaction, interaction.user.display_avatar)
      await self.bot.ActiveList.add_interface(interaction.user.id, "profil", view)
      await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="specialite")
  async def spe(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche les spécialités disponibles pour acheter ou équiper """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      cSlayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      embed = lib.Embed.create_embed_spe(cSlayer, self.bot.Specializations[1])
      view = lib.SpeView(self.bot, cSlayer, interaction)
      await self.bot.ActiveList.add_interface(interaction.user.id, "inventaire_spe", view)
      await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="regen")
  async def regen(self, interaction: lib.discord.Interaction) -> None:
    """ Permet de récupérer de la santé ou de ressuciter """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      cSlayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      if cSlayer.damage_taken > 0:
        #C'est une Rez
        if cSlayer.dead:
          waiting_time = int(self.bot.Variables["regen_waiting_time_rez"]) #7200
          #Si on a attendu suffisamment
          if datetime.datetime.timestamp(datetime.datetime.now()) - cSlayer.lastregen >= waiting_time or not cSlayer.firstregen:
            #On rez

            #Register Regen
            cSlayer.lastregen = datetime.datetime.timestamp(datetime.datetime.now())
            cSlayer.firstregen = True

            cSlayer.dead = False
            regen = cSlayer.regen()
            await self.bot.dB.push_slayer_data(cSlayer)
            await interaction.followup.send(content=f"Résurrection effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
          else:
            await interaction.followup.send(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine résurrection : **{int(cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)
        #C'est une regen
        else:
          waiting_time = int(self.bot.Variables["regen_waiting_time_regen"]) #3600
          #Si on a attendu suffisamment
          if datetime.datetime.timestamp(datetime.datetime.now()) - cSlayer.lastregen >= waiting_time or not cSlayer.firstregen:
            regen = cSlayer.regen()

            #Register Regen
            cSlayer.lastregen = datetime.datetime.timestamp(datetime.datetime.now())
            cSlayer.firstregen = True

            await self.bot.dB.push_slayer_data(cSlayer)
            await cSlayer.getDrop(pets=[192])
            #Spé Guerrisseur
            if cSlayer.faction != 0 and cSlayer.cSpe.id == 11:
              regen_mass_update = []
              content = f"> Régénération de masse effectuée.\n> Les talents de guérisseur de <@{cSlayer.id}> étendent cet effet à l'ensemble de sa faction ! Les joueurs récupèrent jusqu'à {regen} 💖\n> Joueurs concernés :\n> "
              for slayer_id, cActiveSlayer in self.bot.ActiveList.active_slayers.items():
                cOtherSlayer = cActiveSlayer.cSlayer
                if cOtherSlayer.faction == cSlayer.faction and not cOtherSlayer.dead and cOtherSlayer.damage_taken > 0 and cOtherSlayer.id != cSlayer.id:
                  content += f"<@{cOtherSlayer.id}>, "
                  cOtherSlayer.damage_taken -= min(cOtherSlayer.damage_taken, regen)
                  regen_mass_update.append((cOtherSlayer.id, cOtherSlayer.damage_taken))
              
              if regen_mass_update != []:
                channel = self.bot.get_channel(self.bot.rChannels["logs"])
                await channel.send(content=content)
                await self.bot.dB.push_MassRegenGuérisseur(regen_mass_update)


            await interaction.followup.send(content=f"Régénération effectuée : Tu as récupéré {regen} ❤️", ephemeral=True)
          else:
            await interaction.followup.send(content=f"Malheureusement, il te faut encore attendre un peu !\nProchaine régénération : **{int(cSlayer.lastregen + waiting_time - datetime.datetime.timestamp(datetime.datetime.now()))}**s", ephemeral=True)
      else:
        await interaction.followup.send(content=f"Tu n'as pas besoin de te soigner !", ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

  @lib.app_commands.command(name="loadouts")
  async def loadouts(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche votre profil, comprenant vos statistiques et votre équipement """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      cSlayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      view = lib.LoadoutView(self.bot, cSlayer, interaction, interaction.user.display_avatar)
      embed = view.select_embed()
      await self.bot.ActiveList.add_interface(interaction.user.id, "Loadout", view)
      await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Slayer(bot))
  lib.logging.warning("Commands_Slayer : OK")