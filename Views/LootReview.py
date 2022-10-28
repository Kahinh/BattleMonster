import lib

class Loot_Dropdown(lib.discord.ui.Select):
    def __init__(self, bot, loot_recap):
        options = []
        options.append(lib.discord.SelectOption(label="Recap", value="None", emoji="♾️"))
        for cItem in loot_recap["items"]:
            options.append(lib.discord.SelectOption(label=cItem.name, value=cItem.item_id, emoji=bot.rSlots[cItem.slot]["display_emote"]))

        super().__init__(placeholder='Filtrer le butin ...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.values[0] == "None": self.values[0] = None
        if self.values[0] is None:
            embed = lib.Embed.create_embed_recap_loot(self.view.bot, self.view.recap_loot)
            await interaction.response.edit_message(embed=embed) 
        else:
            for item in self.view.recap_loot["items"]:
                if int(item.item_id) == int(self.values[0]):
                    cItem = item
                    break
            embed = lib.Embed.create_embed_item(self.view.bot, cItem, self.view.Slayer)
            await interaction.response.edit_message(embed=embed)
        
class LootReviewView(lib.discord.ui.View):
    def __init__(self, bot, recap_loot, Slayer, interaction):
        super().__init__(timeout=600)
        self.bot = bot
        self.recap_loot = recap_loot
        self.Slayer = Slayer
        self.interaction = interaction

        # Adds the dropdown to our view object.
        self.add_item(Loot_Dropdown(self.bot, self.recap_loot))

    async def end_view(self):
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.end_view()