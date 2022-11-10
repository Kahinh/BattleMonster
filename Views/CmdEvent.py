import lib

class Gamemode_Dropdown(lib.discord.ui.Select):
    def __init__(self, rGamemodes):
        options = []
        for row in rGamemodes:
            if row["cmdevent"]:
                options.append(lib.discord.SelectOption(label=row["name"], value=row["id"]))

        super().__init__(placeholder='Choisissez l\' à faire apparaître...', min_values=1, max_values=1, options=options)
    async def callback(self, interaction: lib.discord.Interaction):
        for row in self.view.gamemodes:
            if int(row["id"]) == int(self.values[0]):
                gamemode = row
        await interaction.response.send_message(content="L'event va apparaître !", ephemeral=True)
        Battle = lib.Battle(self.view.bot, gamemode, interaction)
        await Battle.constructGamemode()
        await self.view.close_view()

class CmdEvent(lib.discord.ui.View):
    def __init__(self, bot, gamemodes, interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.gamemodes = gamemodes
        self.interaction = interaction

        self.add_item(Gamemode_Dropdown(self.gamemodes))

    async def close_view(self):
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
