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
        Slayer = await self.bot.ActiveList.get_Slayer(user.id, user.name)
        embed = lib.Embed.create_embed_profil(Slayer, user.display_avatar)
        view = lib.SlayerView(self.bot, Slayer, interaction, user.display_avatar, "shared_profil")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: lib.commands.Bot) -> None:
  await bot.add_cog(Context_Menus(bot))
  print("Context_Menus : √")