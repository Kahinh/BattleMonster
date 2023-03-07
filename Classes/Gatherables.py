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
        self.spawn_rate = float(spawn_rate)