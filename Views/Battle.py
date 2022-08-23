import lib

class Light_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Légère", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        isEnd = await self.view.Battle.getAttack(interaction, "L")
        if isEnd:
            await self.view.Battle.calculateLoot()
            await self.view.Battle.endBattle(interaction.message)
            self.view.stop()

class Heavy_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Lourde", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        isEnd = await self.view.Battle.getAttack(interaction, "H")
        if isEnd:
            await self.view.Battle.calculateLoot()
            await self.view.Battle.endBattle(interaction.message)
            self.view.stop()

class Special_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Capacité Spéciale", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        isEnd = await self.view.Battle.getAttack(interaction, "S")
        if isEnd:
            await self.view.Battle.calculateLoot()
            await self.view.Battle.endBattle(interaction.message)
            self.view.stop()

class BattleView(lib.discord.ui.View):
    def __init__(self, Battle):
        super().__init__(timeout=600)
        self.Battle = Battle

        # Adds the dropdown to our view object.
        self.add_item(Light_Button())
        self.add_item(Heavy_Button())
        self.add_item(Special_Button())

    async def on_timeout(self) -> None:
        if hasattr(self, "interaction"): message = await self.interaction.original_message()
        if hasattr(self, "message"): message = self.message
        await self.Battle.calculateLoot()
        await self.Battle.endBattle(message, False)
        self.stop()