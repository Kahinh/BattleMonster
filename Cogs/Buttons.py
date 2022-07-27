from time import time

from async_timeout import Timeout, timeout
import lib

class Buttons_Battle(lib.discord.ui.View):
    def __init__(self, Run):
        super().__init__()
        self.Run = Run

    @lib.discord.ui.button(label='Attaque Légère', style=lib.discord.ButtonStyle.green)
    async def light(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Functions.Run.Functions.attack(self.Run, interaction, "L")
        if isDead:
            for item in self.children:
                item.disabled = True
            self.stop()

    @lib.discord.ui.button(label='Attaque Lourde', style=lib.discord.ButtonStyle.blurple)
    async def heavy(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Functions.Run.Functions.attack(self.Run, interaction, "L")
        if isDead:
            for item in self.children:
                item.disabled = True
            self.stop()

    #@lib.discord.ui.button(label='Spécial', style=lib.discord.ButtonStyle.red)
    #async def special(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        ##Check Guild ID & User ID
        #global global_slayerlist
        #global global_battleslist
        #global_slayerlist = await lib.Functions.Global.Tools.checkifguildslayerexist(global_slayerlist, interaction.guild_id, interaction.user)

    #    await interaction.response.send_message('Special', ephemeral=True)


class Buttons_Loot(lib.discord.ui.View):
    def __init__(self, Run):
        super().__init__(timeout=600)
        self.Run = Run

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=None)
        self.stop()

    @lib.discord.ui.button(label='Détails', style=lib.discord.ButtonStyle.green)
    async def details(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        pass

    @lib.discord.ui.button(label='Équiper', style=lib.discord.ButtonStyle.blurple)
    async def equip(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        pass

    @lib.discord.ui.button(label='Vendre', style=lib.discord.ButtonStyle.red)
    async def sell(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        pass