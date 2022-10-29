from pstats import Stats
import lib

class Profil_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Profil", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            embed = self.view.embed_Profil
            for item in self.view.children:
                if item.label=="Profil":
                    item.disabled = True
                if item.label=="Équipement":
                    item.disabled = False
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class Equipment_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équipement", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            embed = self.view.embed_Equipment
            for item in self.view.children:
                if item.label=="Équipement":
                    item.disabled = True
                if item.label=="Profil":
                    item.disabled = False
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class Achievements_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Succès", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            await interaction.response.edit_message(content="Test")
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !")

class SlayerView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction, avatar, interface_name="profil"):
        super().__init__(timeout=120)
        self.bot = bot
        self.interface_name=interface_name
        self.interaction = interaction
        self.Slayer = Slayer
        self.obsolete = False
        self.embed_Profil = lib.Embed.create_embed_profil(Slayer, avatar)
        self.embed_Equipment = lib.Embed.create_embed_equipment(bot, Slayer, avatar)

        self.add_item(Profil_Button())
        self.add_item(Equipment_Button())
        #self.add_item(Achievements_Button())

        for item in self.children:
            if item.label=="Profil":
                item.disabled = True

    async def update_view(self):
        pass

    async def close_view(self):
        if self.interface_name == "profil":
            self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, "profil")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
