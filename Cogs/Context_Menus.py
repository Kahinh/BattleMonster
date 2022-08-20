import lib

class Context_Menus(lib.commands.Cog):
    def __init__(self, bot: lib.commands.Bot) -> None:
        self.bot = bot
        self.profil_menu = lib.app_commands.ContextMenu(
            name='Profil',
            callback=self.profil,
        )
        self.bot.tree.add_command(self.profil_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.profil_menu.name, type=self.profil_menu.type)

    # @app_commads.guilds(12345)
    async def profil(self, interaction: lib.discord.Interaction, user: lib.discord.User) -> None:
        Slayer, InterfaceReady = await self.bot.ActiveList.get_Slayer(user.id, user.name, "shared_profil")
        embed = lib.Embed.create_embed_profil(Slayer, user.display_avatar)
        view = lib.SlayerView(self.bot, Slayer, interaction, user.display_avatar)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        self.bot.ActiveList.close_interface(Slayer.cSlayer.slayer_id, "shared_profil")

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Context_Menus(bot))
  print("Context_Menus : √")