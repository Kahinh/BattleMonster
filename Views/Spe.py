import lib

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
        pass

class Buy_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Vendre", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        pass

class SpeView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.Slayer = Slayer
        self.interaction = interaction
        self.index = 0

        self.add_item(Previous_Button())
        self.add_item(Equip_Button())
        self.add_item(Buy_Button())
        self.add_item(Next_Button())

        lib.Toolbox.disable_enable_SpeView(self.children, self.bot.rSpe, self.index)

    async def update_view(self, interaction=None):
        embed = lib.Embed.create_embed_spe(self.Slayer, self.bot.rSpe[self.index])
        lib.Toolbox.disable_enable_SpeView(self.children, self.bot.rSpe, self.index)
        view = self  
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view) 

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, "inventaire_spe")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
