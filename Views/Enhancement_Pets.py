import lib

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

class Feed_Amount(lib.discord.ui.Modal):
    def __init__(self, cObject, cFood, max_food, cSlayer, bot):
        self.cObject = cObject
        self.cFood = cFood
        self.max_food = max_food
        self.cSlayer = cSlayer
        self.bot = bot
        super().__init__(title=f"Nourrir : {self.cObject.name}")

        #Item
        self.feed_amount = lib.discord.ui.TextInput(label=f"{self.cFood.display_emote} {self.cFood.name}",default=f"{self.max_food}", style=lib.discord.TextStyle.short, min_length=1, max_length=2)
        self.add_item(self.feed_amount)

    async def on_submit(self, interaction: lib.discord.Interaction):
        try:
            feed_amount = int(self.feed_amount.value)
            isInt = True
        except:
            isInt = False
        if isInt:
            if feed_amount <= self.max_food and feed_amount > 0:
                #Je retire de l'inventaire les gatherables utilisées
                if self.cObject.equipped: await self.cSlayer.unequip_item(self.cObject)
                await self.cSlayer.update_inventory_gatherables(self.cFood.id, -feed_amount)
                #Je up le niveau de l'item
                await self.cObject.update_item_level(feed_amount, self.cSlayer)
                if self.cObject.equipped: await self.cSlayer.equip_item(self.cObject)

                await self.bot.ActiveList.update_interface(interaction.user.id, "ameliopet")
                await interaction.response.send_message(f'Vous avez donné {feed_amount} {self.cFood.name} ({self.cFood.display_emote}) à {self.cObject.name}', ephemeral=True)
            else:
                await interaction.response.send_message(f'Le nombre renseigné est incorrect', ephemeral=True)
        else:
            await interaction.response.send_message(f'Il faut renseigner un nombre pour nourrir votre familier !', ephemeral=True)

class Feed_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Nourrir", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            cObject = self.view.pet_list[self.view.index]
            cFood = self.view.bot.PetFood[self.view.pet_list[self.view.index].id]
            max_food = int(min(100-int(self.view.pet_list[self.view.index].level), int(self.view.cSlayer.inventories["gatherables"].get(self.view.bot.PetFood[self.view.pet_list[self.view.index].id].id, 0))))
            await interaction.response.send_modal(Feed_Amount(cObject, cFood, max_food, self.view.cSlayer, self.view.bot))
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class EnhancementPetsView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction):
        super().__init__(timeout=60)
        self.bot = bot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.obsolete = False
        self.pet_list = self.create_pet_list()
        self.index = 0
        self.embed = self.create_embed()

        if self.pet_list != []:
            self.add_item(Previous_Button())
            self.add_item(Feed_Button())
            self.add_item(Next_Button())
            self.disable_enable_feed_button()
            self.disable_enable_previous_next_buttons()

    def disable_enable_previous_next_buttons(self):
        len_list = len(self.pet_list)
        if self.index == len_list - 1  or len_list == 0:
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
        if self.cSlayer.inventories["gatherables"].get(self.bot.PetFood[self.pet_list[self.index].id].id, 0) == 0:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="Nourrir":
                        item.disabled = True
        else:
            for item in self.children:
                if hasattr(item, "label"):
                    if item.label=="Nourrir":
                        item.disabled = False

    def create_pet_list(self):
        return [self.cSlayer.inventories["items"][item_id] for item_id in self.cSlayer.inventories["items"] if self.cSlayer.inventories["items"][item_id].slot == "pet" and self.cSlayer.inventories["items"][item_id].level != 100]

    def create_embed(self):
        return lib.Embed.create_embed_enhancement_pet(self.cSlayer, self.pet_list, self.index, self.bot)

    async def update_view(self, interaction=None):
        #Si le familier a atteint le niveau 100, on recalcule
        Pet_is100 = False
        for cObject in self.pet_list:
            if cObject.level == 100:
                Pet_is100 = True

        if Pet_is100:
            self.pet_list = self.create_pet_list()
            self.index = 0

        self.embed = self.create_embed()

        #Si la liste est vide, on supprime
        if self.pet_list == []:
            await self.close_view(self.embed)
            return

        self.disable_enable_previous_next_buttons()
        self.disable_enable_feed_button()

        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=self.embed, view=self)
        else:
            await interaction.response.edit_message(embed=self.embed, view=self) 

    async def close_view(self, embed=None):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "ameliopet")
        message = await self.interaction.original_response()
        if embed is not None:
            await message.edit(embed=embed, view=None)
        else:
            await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
