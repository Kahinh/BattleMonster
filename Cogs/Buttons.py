from time import time
from tkinter import DISABLED

from async_timeout import Timeout, timeout
import lib

class Buttons_Battle(lib.discord.ui.View):
    def __init__(self, Run):
        super().__init__()
        self.Run = Run

    @lib.discord.ui.button(label='Attaque Légère', style=lib.discord.ButtonStyle.green)
    async def light(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Run_Functions.attack(self.Run, interaction, "L")
        if isDead:
            for item in self.children:
                item.disabled = True
            self.stop()

    @lib.discord.ui.button(label='Attaque Lourde', style=lib.discord.ButtonStyle.blurple)
    async def heavy(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Run_Functions.attack(self.Run, interaction, "L")
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
    def __init__(self, Run, slayer_id, loot, isAlready):
        super().__init__(timeout=300)
        self.Run = Run
        self.slayer_id = slayer_id
        self.loot = loot
        if isAlready:
            self.remove_item(self.equip)
            self.remove_item(self.sell)


    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=None)
        self.stop()

    @lib.discord.ui.button(label='Détails', style=lib.discord.ButtonStyle.green)
    async def details(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Run, interaction, True, "detailed", self.loot)}', ephemeral=True)
        
    @lib.discord.ui.button(label='Équiper', style=lib.discord.ButtonStyle.blurple)
    async def equip(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        if self.slayer_id == interaction.user.id:
            self.Run.slayerlist[interaction.user.id].slots[self.Run.BDD["Items_list"][self.loot].slot] = self.loot
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Run, interaction, True, "equip", self.loot)}', ephemeral=True)

            #Puis on désactive les autres boutons
            for item in self.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await self.message.edit(view=self)

        else:
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Run, interaction, False, "equip", self.loot)}', ephemeral=True)

    @lib.discord.ui.button(label='Vendre', style=lib.discord.ButtonStyle.red)
    async def sell(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        if self.slayer_id == interaction.user.id:
            self.Run.slayerlist[interaction.user.id].money += self.Run.BDD["Rarities_list"][self.Run.BDD["Items_list"][self.loot].rarity]["price"]
            self.Run.slayerlist[interaction.user.id].inventory_items.remove(self.loot)
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Run, interaction, True, "sell", self.loot)}', ephemeral=True)

            #Puis on désactive les autres boutons
            for item in self.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await self.message.edit(view=self)

        else:
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Run, interaction, False, "sell", self.loot)}', ephemeral=True)