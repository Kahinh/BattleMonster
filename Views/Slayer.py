from pstats import Stats
import lib

class Profil_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Profil", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Profil"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class Equipment_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équipement", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Équipement"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class Achievements_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Prouesses", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Prouesses"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class SlayerView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction, avatar, interface_name="profil"):
        super().__init__(timeout=60)
        self.bot = bot
        self.interface_name=interface_name
        self.interaction = interaction
        self.Slayer = Slayer
        self.obsolete = False
        self.tab = "Profil"
        self.avatar = avatar

        self.add_item(Profil_Button())
        self.add_item(Equipment_Button())
        self.add_item(Achievements_Button())

        for item in self.children:
            if item.label=="Profil":
                item.disabled = True

    async def update_view(self, interaction=None):
        if self.tab == "Équipement":
            embed = lib.Embed.create_embed_equipment(self.bot, self.Slayer, self.avatar)
        elif self.tab == "Prouesses":
            embed = lib.Embed.create_embed_achievement(self.Slayer, self.avatar)
        else: #Profil
            embed = lib.Embed.create_embed_profil(self.Slayer, self.avatar)

        for item in self.children:
            if item.label==self.tab:
                item.disabled = True
            else:
                item.disabled = False
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed) 
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    async def close_view(self):
        if self.interface_name == "profil":
            self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, "profil")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
