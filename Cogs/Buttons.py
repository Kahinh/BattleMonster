from async_timeout import Timeout, timeout
import lib

print("Buttons : √")

class Buttons_Battle(lib.discord.ui.View):
    def __init__(self, Main, cMonster, rElement, rRarity):
        super().__init__()
        self.Main = Main
        self.cMonster = cMonster
        self.rElement = rElement
        self.rRarity = rRarity

    @lib.discord.ui.button(label='Attaque Légère', style=lib.discord.ButtonStyle.green)
    async def light(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Battle_Functions.attack(self, interaction, "L")
        if isDead:
            for item in self.children:
                item.disabled = True
            del(self.cMonster)
            self.stop()

    @lib.discord.ui.button(label='Attaque Lourde', style=lib.discord.ButtonStyle.blurple)
    async def heavy(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Battle_Functions.attack(self, interaction, "H")
        if isDead:
            for item in self.children:
                item.disabled = True
            del(self.cMonster)
            self.stop()

    @lib.discord.ui.button(label='Spécial', style=lib.discord.ButtonStyle.red)
    async def special(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await lib.Battle_Functions.attack(self, interaction, "S")
        if isDead:
            for item in self.children:
                item.disabled = True
            del(self.cMonster)
            self.stop()


class Buttons_Loot(lib.discord.ui.View):
    def __init__(self, Buttons_Battle, slayer_id, loot, isAlready, rPrice, rRarity):
        super().__init__(timeout=300)
        self.Buttons_Battle = Buttons_Battle
        self.slayer_id = slayer_id
        self.loot = loot
        self.rPrice = rPrice
        self.rRarity = rRarity
        if isAlready:
            self.remove_item(self.equip)
            self.remove_item(self.sell)


    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(view=None)
        except:
            pass
        self.stop()

    @lib.discord.ui.button(label='Détails', style=lib.discord.ButtonStyle.green)
    async def details(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Buttons_Battle, interaction, True, "detailed", self.loot, self.rPrice, self.rRarity)}', ephemeral=True)
        
    @lib.discord.ui.button(label='Équiper', style=lib.discord.ButtonStyle.blurple)
    async def equip(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        if self.slayer_id == interaction.user.id:
            self.Buttons_Battle.Main.bot.slayers_list[interaction.user.id].slots[self.loot["slot"]] = self.loot["id"]
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Buttons_Battle, interaction, True, "equip", self.loot, self.rPrice, self.rRarity)}', ephemeral=True)

            #Puis on désactive les autres boutons
            for item in self.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await self.message.edit(view=self)

        else:
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Buttons_Battle, interaction, False, "equip", self.loot, self.rPrice, self.rRarity)}', ephemeral=True)

    @lib.discord.ui.button(label='Vendre', style=lib.discord.ButtonStyle.red)
    async def sell(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        if self.slayer_id == interaction.user.id:
            self.Buttons_Battle.Main.bot.slayers_list[interaction.user.id].money += 0
            self.Buttons_Battle.Main.bot.slayers_list[interaction.user.id].inventory_items.remove(self.loot["id"])
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Buttons_Battle, interaction, True, "sell", self.loot, self.rPrice, self.rRarity)}', ephemeral=True)

            #Puis on désactive les autres boutons
            for item in self.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await self.message.edit(view=self)

        else:
            await interaction.response.send_message(f'{lib.Ephemeral.get_ephemeralLootReaction(self.Buttons_Battle, interaction, False, "sell", self.loot, self.rPrice, self.rRarity)}', ephemeral=True)