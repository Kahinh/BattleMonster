import lib

class Rarity_Dropdown(lib.discord.ui.Select):
    def __init__(self, rRarities):
        options = []
        options.append(lib.discord.SelectOption(label="Toutes", value="None", emoji="♾️"))
        for rarity in rRarities:
            options.append(lib.discord.SelectOption(label=rRarities[rarity]["display_text"].capitalize(), value=rarity, emoji=rRarities[rarity]["display_emote"]))

        super().__init__(placeholder='Filtrer la rareté...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.values[0] == "None": self.values[0] = None
        self.view.rarity = self.values[0]
        self.view.items_list_filtered = lib.Toolbox.filter_items_list(self.view.Slayer.cSlayer.inventory_items, self.view.slot, self.view.element, self.view.rarity)
        
        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False
        self.index = 0

        await self.view.update_view(interaction) 

class Element_Dropdown(lib.discord.ui.Select):
    def __init__(self, rElements):
        options = []
        options.append(lib.discord.SelectOption(label="Tous", value="None", emoji="♾️"))
        for element in rElements:
            options.append(lib.discord.SelectOption(label=rElements[element]["display_text"].capitalize(), value=element, emoji=rElements[element]["display_emote"]))

        super().__init__(placeholder="Filtrer l'élément...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.values[0] == "None": self.values[0] = None
        self.view.element = self.values[0]
        self.view.items_list_filtered = lib.Toolbox.filter_items_list(self.view.Slayer.cSlayer.inventory_items, self.view.slot, self.view.element, self.view.rarity)
        
        self.index = 0
        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False

        await self.view.update_view(interaction) 

class Slot_Dropdown(lib.discord.ui.Select):
    def __init__(self, rSlots):
        options = []
        options.append(lib.discord.SelectOption(label="Tous", value="None", emoji="♾️"))
        for slot in rSlots:
            options.append(lib.discord.SelectOption(label=rSlots[slot]["display_text"].capitalize(), value=slot, emoji=rSlots[slot]["display_emote"]))

        super().__init__(placeholder="Filtrer l'emplacement...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.values[0] == "None": self.values[0] = None
        self.view.slot = self.values[0]
        self.view.items_list_filtered = lib.Toolbox.filter_items_list(self.view.Slayer.cSlayer.inventory_items, self.view.slot, self.view.element, self.view.rarity)
        
        self.index = 0
        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False

        await self.view.update_view(interaction) 

class Previous_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="<<", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.index -= 1
        
        await self.view.update_view(interaction)        

class Next_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label=">>", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.index += 1 
        
        await self.view.update_view(interaction)   

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        isEquipped, List = await self.view.Slayer.equip_item(self.view.items_list_filtered[self.view.index])

        if isEquipped:
            await self.view.update_view(interaction) 
            await interaction.followup.send(content="L'objet a été équipé !", ephemeral=True) 
        else:
            if len(List) == 0:
                await interaction.response.send_message(content="Une erreur est survenue !", ephemeral=True)
            else:
                viewMult = lib.MultEquipView(self.view.bot, self.view.Slayer, List, interaction, self.view.items_list_filtered[self.view.index])
                await self.view.bot.ActiveList.add_interface(interaction.user.id, "mult_equip", viewMult)
                await interaction.response.send_message(content="Tous les emplacements sont déjà utilisés, quel objet souhaitez-vous remplacer ?", view=viewMult, ephemeral=True)

class Sell_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Vendre", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):

            Sold = await self.view.Slayer.sell_item(self.view.items_list_filtered[self.view.index])
            self.view.items_list_filtered = lib.Toolbox.filter_items_list(self.view.Slayer.cSlayer.inventory_items, self.view.slot, self.view.element, self.view.rarity)
            self.index = 0

            await self.view.update_view(interaction)   

            if Sold:
                await interaction.followup.send("L'objet a été vendu !", ephemeral=True)
            else:
                await interaction.followup.send("Une erreur s'est produite !", ephemeral=True)

class InventoryView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.Slayer = Slayer
        self.interaction = interaction

        self.slot = None
        self.element = None
        self.rarity = None

        self.items_list_filtered = lib.Toolbox.filter_items_list(self.Slayer.cSlayer.inventory_items, self.slot, self.element, self.rarity)
        self.index = 0


        self.add_item(Previous_Button())
        self.add_item(Equip_Button())
        self.add_item(Sell_Button())
        self.add_item(Next_Button())
        self.add_item(Slot_Dropdown(self.bot.rSlots))
        self.add_item(Element_Dropdown(self.bot.rElements))
        self.add_item(Rarity_Dropdown(self.bot.rRarities))

        lib.Toolbox.disable_enable_InventoryView(self.children, self.items_list_filtered, self.index)

    async def update_view(self, interaction=None):
        if interaction is None: self.items_list_filtered = lib.Toolbox.filter_items_list(self.Slayer.cSlayer.inventory_items, self.slot, self.element, self.rarity)
        embed = lib.Embed.create_embed_item(self.bot, None if self.items_list_filtered == [] else self.items_list_filtered[self.index])
        lib.Toolbox.disable_enable_InventoryView(self.children, self.items_list_filtered, self.index)
        view = self  

        if interaction is None:
            message = await self.interaction.original_message()
            await message.edit(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view) 

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, "inventaire")
        message = await self.interaction.original_message()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()