import lib

class Rarity_Dropdown(lib.discord.ui.Select):
    def __init__(self, Rarities):
        options = []
        options.append(lib.discord.SelectOption(label="Toutes", value="None", emoji="♾️"))
        for rarity in Rarities:
            options.append(lib.discord.SelectOption(label=Rarities[rarity].display_text.capitalize(), value=rarity, emoji=Rarities[rarity].display_emote))

        super().__init__(placeholder='Filtrer la rareté...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if self.values[0] == "None": self.values[0] = None
            self.view.rarity = self.values[0]
            self.view.items_list_filtered = self.view.filter_items_list()
            self.view.index = 0
            self.itemID_compare = 0

            for option in self.options:
                if option.value == self.values[0]:
                    option.default = True
                else:
                    option.default = False
            
            await self.view.update_view(interaction) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Element_Dropdown(lib.discord.ui.Select):
    def __init__(self, Elements):
        options = []
        options.append(lib.discord.SelectOption(label="Tous", value="None", emoji="♾️"))
        for element in Elements:
            options.append(lib.discord.SelectOption(label=Elements[element].display_text.capitalize(), value=element, emoji=Elements[element].display_emote))

        super().__init__(placeholder="Filtrer l'élément...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if self.values[0] == "None": self.values[0] = None
            self.view.element = self.values[0]
            self.view.items_list_filtered = self.view.filter_items_list()
            self.view.index = 0
            self.itemID_compare = 0

            for option in self.options:
                if option.value == self.values[0]:
                    option.default = True
                else:
                    option.default = False

            await self.view.update_view(interaction) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Slot_Dropdown(lib.discord.ui.Select):
    def __init__(self, Slots):
        options = []
        options.append(lib.discord.SelectOption(label="Tous", value="None", emoji="♾️"))
        for slot in Slots:
            if Slots[slot].activated:
                options.append(lib.discord.SelectOption(label=Slots[slot].display_text.capitalize(), value=slot, emoji=Slots[slot].display_emote))

        super().__init__(placeholder="Filtrer l'emplacement...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if self.values[0] == "None": self.values[0] = None
            self.view.slot = self.values[0]
            self.view.items_list_filtered = self.view.filter_items_list()
            self.view.index = 0
            self.itemID_compare = 0

            for option in self.options:
                if option.value == self.values[0]:
                    option.default = True
                else:
                    option.default = False

            await self.view.update_view(interaction) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Previous_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="<<", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.index = max(self.view.index - 1, 0)
            self.itemID_compare = 0
            
            await self.view.update_view(interaction)        
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Next_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label=">>", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.index += 1 
            self.view.index = min(self.view.index + 1, len(self.view.items_list_filtered) - 1)
            self.itemID_compare = 0
            
            await self.view.update_view(interaction)   
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            empty_slot, only_one_place_on_slot = self.view.cSlayer.item_can_be_equipped(self.view.bot.Slots[self.view.items_list_filtered[self.view.index].slot])
            self.itemID_compare = 0

            if any([empty_slot, only_one_place_on_slot]):
                if only_one_place_on_slot and not empty_slot:
                    await self.view.cSlayer.unequip_item(self.view.cSlayer.slot_items_equipped(self.view.bot.Slots[self.view.items_list_filtered[self.view.index].slot])[0])
                await self.view.cSlayer.equip_item(self.view.items_list_filtered[self.view.index])
                await self.view.update_view(interaction) 
                await self.view.bot.ActiveList.update_interface(self.view.cSlayer.id, "LootReview")
                await interaction.followup.send(content="L'objet a été équipé !", ephemeral=True) 
            else:
                if len(self.view.cSlayer.slot_items_equipped(self.view.bot.Slots[self.view.items_list_filtered[self.view.index].slot])) == 0:
                    await interaction.response.send_message(content="Une erreur est survenue !", ephemeral=True)
                else:
                    viewMult = lib.MultEquipView(self.view.bot, self.view.cSlayer, self.view.cSlayer.slot_items_equipped(self.view.bot.Slots[self.view.items_list_filtered[self.view.index].slot]), interaction, self.view.items_list_filtered[self.view.index])
                    await self.view.bot.ActiveList.add_interface(interaction.user.id, "mult_equip", viewMult)
                    await interaction.response.send_message(content="Tous les emplacements sont déjà utilisés, quel objet souhaitez-vous remplacer ?", view=viewMult, ephemeral=True)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Compare_Dropdown(lib.discord.ui.Select):
    def __init__(self, itemsequipped_list):
        options = []
        for cObject in itemsequipped_list:
            options.append(lib.discord.SelectOption(label=cObject.name, value=cObject.id))

        super().__init__(placeholder="Objet à comparer...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            await self.view.update_view(interaction, self.values[0]) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class InventoryView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction):
        super().__init__(timeout=60)
        self.bot = bot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.obsolete = False

        self.slot = None
        self.element = None
        self.rarity = None

        self.items_list_filtered = self.filter_items_list()
        self.index = 0
        #self.itemsequipped_list = self.cSlayer.current_loadout.items
        #self.itemID_compare = itemID_compare

        self.add_item(Previous_Button())
        self.add_item(Equip_Button())
        self.add_item(Next_Button())
        self.add_item(Slot_Dropdown(self.bot.Slots))
        self.add_item(Rarity_Dropdown(self.bot.Rarities))
        self.add_item(Element_Dropdown(self.bot.Elements))

        self.disable_enable_InventoryView()

    def filter_items_list(self):
        filtered_list = []
        items_list = self.cSlayer.inventories["items"]
        for id in items_list:
            if (items_list[id].slot == self.slot or self.slot is None) and (items_list[id].element == self.element or self.element is None) and (items_list[id].rarity == self.rarity or self.rarity is None):
                filtered_list.append(items_list[id])
        return filtered_list

    def get_itemsequipped_list(self):
        self.itemsequipped_list = []
        #On get si on a des items équipés à cet endroit là
        if self.items_list_filtered != []:
            self.itemsequipped_list = self.cSlayer.slot_items_equipped(self.bot.Slots[self.items_list_filtered[self.index].slot])

    async def items_compare_view(self):
        for item in self.children:
            if hasattr(item, "placeholder"):
                if item.placeholder=="Objet à comparer...":
                    self.remove_item(item)
        if len(self.itemsequipped_list) > 1:
            self.add_item(Compare_Dropdown(self.itemsequipped_list))

    def get_embed(self, cObject=None):
        return lib.Embed.create_embed_item(self.bot, self.cSlayer, None if self.items_list_filtered == [] else self.items_list_filtered[self.index], cObject)
            

    async def update_view(self, interaction=None, itemID_Compare=0, itemID_Updated=None):
        if itemID_Updated is None or itemID_Updated in self.items_list_filtered[self.index].id:
            if interaction is None: self.items_list_filtered = self.filter_items_list()
            
            self.get_itemsequipped_list()
            await self.items_compare_view()
            if len(self.itemsequipped_list) > 1:
                if itemID_Compare == 0:
                    cObject = self.itemsequipped_list[0]
                else:
                    for item in self.itemsequipped_list:
                        if int(item.id) == int(itemID_Compare):
                            cObject = item
                            break
            elif len(self.itemsequipped_list) == 1:
                cObject = self.itemsequipped_list[0]
            else:
                cObject = None

            embed = self.get_embed(cObject)
            self.disable_enable_InventoryView()
            view = self  

            if interaction is None:
                message = await self.interaction.original_response()
                await message.edit(embed=embed, view=view)
            else:
                await interaction.response.edit_message(embed=embed, view=view) 

    def disable_enable_InventoryView(self):
        len_list = len(self.items_list_filtered)
        if self.index >= len_list - 1 or len_list == 0:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label==">>":
                        item.disabled = True   
        if self.index > 0:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="<<":
                        item.disabled = False 
        if self.index == 0:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="<<":
                        item.disabled = True
        if self.index < len_list - 1:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label==">>":
                        item.disabled = False
        for item in self.children:
            if hasattr(item, "label"):
                if item.label=="Équiper":
                    if len(self.items_list_filtered) > 0 :
                        if self.items_list_filtered[self.index].equipped:
                            item.disabled = True
                        else:
                            item.disabled = False
                    else:
                        item.disabled = True

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "inventaire")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
