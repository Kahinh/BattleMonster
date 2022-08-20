import lib

class Commands_Slayer(lib.commands.GroupCog, name="slayer"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="inventaire")
  async def inventory(self, interaction: lib.discord.Interaction) -> None:
    """ Ouvre l'inventaire. Utilisez les menus déroulants pour accéder à un objet spécifique """
    Slayer, InterfaceReady = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name, "inventory")
    if InterfaceReady:
      if len(Slayer.cSlayer.inventory_items) > 0:
          #On init le message
          view = lib.InventoryView(self.bot, Slayer, interaction)
          embed = lib.Embed.create_embed_item(self.bot, Slayer.cSlayer.inventory_items[list(Slayer.cSlayer.inventory_items.keys())[0]])
          await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
      else:
        await interaction.response.send_message(content="Malheureusement, tu n'as pas d'objets dans ton inventaire !", ephemeral=True)
    else:
      await interaction.response.send_message(content="Une interface est déjà ouverte", ephemeral=True)

  @lib.app_commands.command(name="profil")
  async def stats(self, interaction: lib.discord.Interaction) -> None:
    """ Affiche votre profil, comprenant vos statistiques et votre équipement """
    Slayer, InterfaceReady = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name, "profil")
    if InterfaceReady:
      embed = lib.Embed.create_embed_profil(Slayer, interaction.user.display_avatar)
      view = lib.SlayerView(self.bot, Slayer, interaction, interaction.user.display_avatar)
      await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
      await interaction.response.send_message(content="Une interface est déjà ouverte", ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Slayer(bot))
  print("Commands_Slayer : √")