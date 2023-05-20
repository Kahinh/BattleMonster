from dataclasses import dataclass
import random
import lib

@dataclass
class Gather:
  def __init__(
    self, 
    bot,
    cGatherable,
    channel_id
    ):
    self.bot = bot
    self.end = False
    self.channel_id = channel_id
    self.gatherable_id = cGatherable.id
    self.type = cGatherable.type
    self.name = cGatherable.name
    self.description = cGatherable.description
    self.img_url = cGatherable.img_url
    self.rarity = cGatherable.rarity
    self.display_emote = cGatherable.display_emote
    self.tracker_role_id = cGatherable.tracker_role_id
    self.stock = random.randint(cGatherable.stock_min, cGatherable.stock_max)

  async def spawnGather(self):
    embed = lib.Embed.create_embed_gatherables(self)
    view = lib.GatherView(self)
    channel = self.bot.get_channel(self.channel_id)
    view.message = await channel.send(content=self.role_tracker_content(), embed=embed, view=view)
    self.bot.ActiveList.add_gather(view.message.id, view)

  def role_tracker_content(self):
    if self.tracker_role_id == 0:
      return ""
    else:
      return f"<@&{self.tracker_role_id}>"
  
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

@dataclass
class GatherablesSpawn:
    id: int
    channel_id: int
    description: str
    spawn_weight: float
    gatherables: list

    def __init__(
        self, 
        rGatherablesSpawn,
        Gatherables
        ):
        self.id = rGatherablesSpawn["id"]
        self.channel_id = rGatherablesSpawn["channel_id"]
        self.description = rGatherablesSpawn["description"]
        self.spawn_weight = float(rGatherablesSpawn["spawn_weight"])
        
        #class ID des gatherables
        gatherables_id = rGatherablesSpawn["gatherables_ids"].strip('][').split(',')
        self.gatherables = []
        for id in gatherables_id:
            self.gatherables.append(Gatherables[int(id)])