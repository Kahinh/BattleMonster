from dataclasses import dataclass

@dataclass
class Rarity:
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
class Element:
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

@dataclass
class Slot:
    name: str
    count: int
    display_text: str
    display_emote: str
    activated: bool

    def __init__(
        self, 
        rSlots
        ):
        self.name = rSlots["slot"]
        self.count = rSlots["count"]
        self.display_text = rSlots["display_text"]
        self.display_emote = rSlots["display_emote"]
        self.activated = rSlots["activated"]
        self.group = rSlots["group"]

@dataclass
class Statistic:
    name: str
    sub_l: bool
    sub_h: bool
    sub_s: bool
    display_text: str
    display_emote: str
    reverse: bool
    percentage: bool

    def __init__(
        self, 
        rStatistics
        ):
        self.name = rStatistics["name"]
        self.sub_l = rStatistics["sub_l"]
        self.sub_h = rStatistics["sub_h"]
        self.sub_s = rStatistics["sub_s"]
        self.display_name = rStatistics["display_name"]
        self.display_emote = rStatistics["display_emote"]
        self.reverse = rStatistics["reverse"]
        self.percentage = rStatistics["percentage"]
        self.cap_min = float(rStatistics["cap_min"]) if rStatistics["is_cap_min"] else None
        self.cap_max = float(rStatistics["cap_max"]) if rStatistics["is_cap_max"] else None

    def sub_division(self):
        if any([self.sub_l, self.sub_h, self.sub_s]):
            division_list = []
            if self.sub_l: division_list.append(self.name+"_l")
            if self.sub_h: division_list.append(self.name+"_h")
            if self.sub_s: division_list.append(self.name+"_s")
            return division_list
        else:
            return [self.name]