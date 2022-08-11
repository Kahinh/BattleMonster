from pstats import Stats
import lib

class Stats_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="<<", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.edit_message(content="Test", ephemeral=True)

class Items_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label=">>", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.edit_message(content="Test", ephemeral=True)

class Achievements_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.edit_message(content="Test", ephemeral=True)

class SlayerView(lib.discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Stats_Button())
        self.add_item(Items_Button())
        self.add_item(Achievements_Button())