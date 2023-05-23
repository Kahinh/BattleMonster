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
    tracker_role_id: int

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
        self.tracker_role_id = rRarities["tracker_role_id"]
        self.tracker_role_id_banner = rRarities["tracker_role_id_banner"]

@dataclass
class Elements:
    name: str
    display_text: str
    display_emote: str

    def __init__(
        self, 
        rElements
        ):
        self.name = rElements["name"]
        self.display_text = rElements["display_text"]
        self.display_emote = rElements["display_emote"]