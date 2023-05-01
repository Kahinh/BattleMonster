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
    def __init__(self, cPet, cFood, max_food, Slayer, bot):
        self.cPet = cPet
        self.cFood = cFood
        self.max_food = max_food
        self.Slayer = Slayer
        self.bot = bot
        super().__init__(title=f"Nourrir : {self.cPet.name}")

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
                await self.Slayer.update_inventory_gatherables(self.cFood.id, -feed_amount)
                #Je up le niveau de l'item
                await self.cPet.update_item_level(feed_amount, self.Slayer.cSlayer)

                #Puis on update les stats du joueur si l'item est équipé
                if self.cPet.equipped:
                    await self.Slayer.updateSlayer()

                await self.bot.ActiveList.update_interface(interaction.user.id, "ameliopet")
                await interaction.response.send_message(f'Vous avez donné {feed_amount} {self.cFood.name} ({self.cFood.display_emote}) à {self.cPet.name}', ephemeral=True)
            else:
                await interaction.response.send_message(f'Le nombre renseigné est incorrect', ephemeral=True)
        else:
            await interaction.response.send_message(f'Il faut renseigner un nombre pour nourrir votre familier !', ephemeral=True)

class Feed_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Nourrir", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            cPet = self.view.pet_list[self.view.index]
            cFood = self.view.bot.PetFood[self.view.pet_list[self.view.index].id]
            max_food = int(min(100-int(self.view.pet_list[self.view.index].level), int(self.view.Slayer.cSlayer.inventory_gatherables.get(self.view.bot.PetFood[self.view.pet_list[self.view.index].id].id, 0))))
            await interaction.response.send_modal(Feed_Amount(cPet, cFood, max_food, self.view.Slayer, self.view.bot))
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class EnhancementPetsView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction):
        super().__init__(timeout=60)
        self.bot = bot
        self.Slayer = Slayer
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
        if self.Slayer.cSlayer.inventory_gatherables.get(self.bot.PetFood[self.pet_list[self.index].id].id, 0) == 0:
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
        return [self.Slayer.cSlayer.inventory_items[item_id] for item_id in self.Slayer.cSlayer.inventory_items if self.Slayer.cSlayer.inventory_items[item_id].slot == "pet" and self.Slayer.cSlayer.inventory_items[item_id].level != 100]

    def create_embed(self):
        return lib.Embed.create_embed_enhancement_pet(self.Slayer, self.pet_list, self.index, self.bot)

    async def update_view(self, interaction=None):
        self.embed = self.create_embed()
        self.disable_enable_previous_next_buttons()
        self.disable_enable_feed_button()

        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=self.embed, view=self)
        else:
            await interaction.response.edit_message(embed=self.embed, view=self) 

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.id, "inventaire")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
