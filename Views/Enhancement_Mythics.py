import lib

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
            self.view.index = 0
            self.view.mythic_list = self.view.create_mythic_list()

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
            self.view.index = 0
            self.view.mythic_list = self.view.create_mythic_list()

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
            self.view.index -= 1
            await self.view.update_view(interaction)        
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Next_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label=">>", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.index += 1 
            await self.view.update_view(interaction)   
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Feed_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Améliorer", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            new_level = lib.random.randint(1, 40)

            if self.view.mythic_list[self.view.index].equipped: await self.view.cSlayer.current_loadout.remove_item_for_enhancement(self.view.mythic_list[self.view.index])
            
            #On ajuste tous les loadout si besoin
            for _, cLoadout in self.view.cSlayer.loadouts.items():
                if self.view.mythic_list[self.view.index].equipped:
                    await cLoadout.remove_item_for_enhancement(self.view.mythic_list[self.view.index])
            #Je retire de l'inventaire les gatherables utilisées
            await self.view.cSlayer.update_inventory_gatherables(5, -1)
            #Je up le niveau de l'item
            await self.view.mythic_list[self.view.index].update_item_level(new_level-self.view.mythic_list[self.view.index].level, self.view.cSlayer)
            if self.view.mythic_list[self.view.index].equipped: await self.view.cSlayer.current_loadout.add_item_for_enhancement(self.view.mythic_list[self.view.index])
            
            #On ajuste tous les loadout si besoin
            for _, cLoadout in self.view.cSlayer.loadouts.items():
                if self.view.mythic_list[self.view.index].equipped:
                    await cLoadout.add_item_for_enhancement(self.view.mythic_list[self.view.index])

            if new_level == 40:
                self.view.mythic_list = self.view.create_mythic_list()
                self.view.index = 0
            await interaction.response.send_message(content=f"Ton item est passé niveau {new_level} !", ephemeral=True)
            await self.view.update_view()
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class EnhancementMythicsView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction):
        super().__init__(timeout=60)
        self.bot = bot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.obsolete = False
        self.slot = None
        self.element = None
        self.mythic_list = self.create_mythic_list()
        self.index = 0
        self.embed = self.create_embed()

        if self.mythic_list != []:
            self.add_items()

    def add_items(self):
        self.clear_items()
        self.add_item(Previous_Button())
        self.add_item(Feed_Button())
        self.add_item(Next_Button())
        self.disable_enable_feed_button()
        self.disable_enable_previous_next_buttons()
        self.add_item(Slot_Dropdown(self.bot.Slots))
        self.add_item(Element_Dropdown(self.bot.Elements))

    def disable_enable_previous_next_buttons(self):
        len_list = len(self.mythic_list)
        if self.index == len_list - 1:
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

    def disable_enable_feed_button(self):
        if self.cSlayer.inventories["gatherables"].get(5, 0) == 0:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="Améliorer":
                        item.disabled = True
        else:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="Améliorer":
                        item.disabled = False

    def create_mythic_list(self, check=False):
        if self.slot is None and self.element is None or check:
            return [self.cSlayer.inventories["items"][item_id] for item_id in self.cSlayer.inventories["items"] if self.cSlayer.inventories["items"][item_id].rarity == "mythic" and self.cSlayer.inventories["items"][item_id].slot != "pet" and self.cSlayer.inventories["items"][item_id].level != 40]
        elif self.slot is None and self.element is not None:
            return [self.cSlayer.inventories["items"][item_id] for item_id in self.cSlayer.inventories["items"] if self.cSlayer.inventories["items"][item_id].rarity == "mythic" and self.cSlayer.inventories["items"][item_id].slot != "pet" and self.cSlayer.inventories["items"][item_id].level != 40 and self.cSlayer.inventories["items"][item_id].element == self.element]
        elif self.slot is not None and self.element is None:
            return [self.cSlayer.inventories["items"][item_id] for item_id in self.cSlayer.inventories["items"] if self.cSlayer.inventories["items"][item_id].rarity == "mythic" and self.cSlayer.inventories["items"][item_id].slot != "pet" and self.cSlayer.inventories["items"][item_id].level != 40 and self.cSlayer.inventories["items"][item_id].slot == self.slot]
        else:
            return [self.cSlayer.inventories["items"][item_id] for item_id in self.cSlayer.inventories["items"] if self.cSlayer.inventories["items"][item_id].rarity == "mythic" and self.cSlayer.inventories["items"][item_id].slot != "pet" and self.cSlayer.inventories["items"][item_id].level != 40 and self.cSlayer.inventories["items"][item_id].slot == self.slot and self.cSlayer.inventories["items"][item_id].element == self.element]

    def create_embed(self):
        return lib.Embed.create_embed_enhancement_mythic(self.cSlayer, self.mythic_list, self.index, self.bot)

    async def update_view(self, interaction=None):
        self.embed = self.create_embed()
        if self.create_mythic_list(True) == []:
            await self.close_view(embed=self.embed)
            return
        self.disable_enable_previous_next_buttons()
        self.disable_enable_feed_button()

        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=self.embed, view=self)
        else:
            await interaction.response.edit_message(embed=self.embed, view=self) 

    async def close_view(self, embed=None):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "ameliomythic")
        message = await self.interaction.original_response()
        if embed is not None:
            await message.edit(embed=embed, view=None)
        else:
            await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
