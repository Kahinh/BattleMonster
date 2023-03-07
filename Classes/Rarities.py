from dataclasses import dataclass

@dataclass
class Rarities:
    name: str
    display_text: str
    display_color: str
    gearscore: int
    price: int
    display_emote: str
    gatherables_spawn: int

    def __init__(
        self, 
        rRarities
        ):
        self.name = rRarities["name"]
        self.display_text = rRarities["display_text"]
        self.display_color = rRarities["display_color"]
        self.gearscore = rRarities["gearscore"]
        self.price = rRarities["price"]
        self.display_emote = rRarities["display_emote"]
        self.gatherables_spawn = rRarities["gatherables_spawn"]