from dataclasses import dataclass

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