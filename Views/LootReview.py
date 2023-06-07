import lib

class Loot_Dropdown(lib.discord.ui.Select):
    def __init__(self, bot, loot_recap):
        options = []
        options.append(lib.discord.SelectOption(label="Recap", value="None", emoji="♾️"))
        for cObject in loot_recap["items"]:
            options.append(lib.discord.SelectOption(label=cObject.name, value=cObject.id, emoji=bot.Slots[cObject.slot].display_emote))

        super().__init__(placeholder='Filtrer le butin ...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if self.values[0] == "None": self.values[0] = None
            self.view.item_displayed = self.values[0]
            await self.view.update_view(interaction=interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:

            for cObject in self.view.recap_loot["items"]:
                if int(cObject.id) == int(self.view.item_displayed):
                    cObject_equipped = cObject

            isEquipped, List = await self.view.cSlayer.equip_item(cObject_equipped)

            if isEquipped:
                await self.view.update_view(interaction) 
                await self.view.bot.ActiveList.update_interface(self.view.cSlayer.id, "inventaire")
                await interaction.followup.send(content="L'objet a été équipé !", ephemeral=True) 
            else:
                if len(List) == 0:
                    await interaction.response.send_message(content="Une erreur est survenue !", ephemeral=True)
                else:
                    viewMult = lib.MultEquipView(self.view.bot, self.view.cSlayer, List, interaction, cObject_equipped)
                    await self.view.bot.ActiveList.add_interface(interaction.user.id, "mult_equip", viewMult)
                    await interaction.response.send_message(content="Tous les emplacements sont déjà utilisés, quel objet souhaitez-vous remplacer ?", view=viewMult, ephemeral=True)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Sell_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Vendre", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            for cObject in self.view.recap_loot["items"]:
                if int(cObject.id) == int(self.view.item_displayed):
                    cObject_sold = cObject
            Sold = await self.view.cSlayer.sell_item(cObject_sold)
            await self.view.update_view(interaction)   
            if Sold:
                await self.view.bot.ActiveList.update_interface(self.view.cSlayer.id, "inventaire")
                await interaction.followup.send("L'objet a été vendu !", ephemeral=True)
            else:
                await interaction.followup.send("Une erreur s'est produite !", ephemeral=True)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class LootReviewView(lib.discord.ui.View):
    def __init__(self, bot, recap_loot, cSlayer, interaction):
        super().__init__(timeout=30)
        self.bot = bot
        self.recap_loot = recap_loot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.obsolete = False
        self.item_displayed = None

        # Adds the dropdown to our view object.
        self.add_item(Loot_Dropdown(self.bot, self.recap_loot))

    async def update_view(self, interaction=None):
        if self.item_displayed is not None: self.item_displayed = int(self.item_displayed)
        self.clear_items()
        if self.item_displayed is not None:
            self.add_item(Equip_Button())
            #self.add_item(Sell_Button())

        self.add_item(Loot_Dropdown(self.bot, self.recap_loot))
        if self.item_displayed is None:
            embed = lib.Embed.create_embed_recap_loot(self.bot, self.recap_loot)
            await interaction.response.edit_message(embed=embed, view=self) 
        else:
            for item in self.recap_loot["items"]:
                if int(item.id) == int(self.item_displayed):
                    cObject = item
                    break
            embed = lib.Embed.create_embed_item(self.bot, self.cSlayer, cObject)
            lib.Toolbox.disable_enable_LootReviewView(self.children, self.cSlayer, int(self.item_displayed))
            await interaction.response.edit_message(embed=embed, view=self)

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "LootReview")
        try:
            message = await self.interaction.original_response()
            await message.edit(view=None)
        except:
            pass
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()