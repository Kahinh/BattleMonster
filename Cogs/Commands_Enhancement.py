import lib

class Commands_Enhancement(lib.commands.GroupCog, name="amélioration"):
  def __init__(self, bot: lib.commands.Bot) -> None:
    self.bot = bot
    super().__init__()
  
  @lib.app_commands.command(name="familiers")
  async def enhancement_pets(self, interaction: lib.discord.Interaction) -> None:
    """ Ouvre l'interface des familiers. Nourrissez les pour les améliorer. """
    await interaction.response.defer(ephemeral=True)
    if self.bot.power:
      Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
      view = lib.EnhancementPetsView(self.bot, Slayer, interaction)
      await self.bot.ActiveList.add_interface(interaction.user.id, "ameliopet", view)
      await interaction.followup.send(embed=view.embed, view=view, ephemeral=True)
    else:
      await interaction.followup.send(content="Le bot est en attente de redémarrage ou en cours d'update. Veuillez patienter.")

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Commands_Enhancement(bot))
  lib.logging.warning("Commands_Enhancement : OK")