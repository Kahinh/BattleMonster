from dataclasses import dataclass

@dataclass
class Gatherables:
    id: int
    name: str
    type: str
    description: str
    img_url: str
    rarity: str
    spawn_rate: int
    stock_min: int
    stock_max: int
    display_emote: str

    def __init__(
        self, 
        rGatherables,
        spawn_rate
        ):
        self.id = rGatherables["id"]
        self.type = rGatherables["type"]
        self.name = rGatherables["name"]
        self.description = rGatherables["description"]
        self.img_url = rGatherables["img_url"]
        self.rarity = rGatherables["rarity"]
        self.stock_min = rGatherables["stock_min"]
        self.stock_max = rGatherables["stock_max"]
        self.display_emote = rGatherables["display_emote"]
        self.tracker_role_id = rGatherables["tracker_role_id"]
        self.spawn_rate = float(spawn_rate)