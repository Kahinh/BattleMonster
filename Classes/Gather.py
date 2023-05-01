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
    self.stock = random.randint(cGatherable.stock_min, cGatherable.stock_max)

  async def spawnGather(self):
    embed = lib.Embed.create_embed_gatherables(self)
    view = lib.GatherView(self)
    channel = self.bot.get_channel(self.channel_id)
    view.message = await channel.send(embed=embed, view=view)
    self.bot.ActiveList.add_gather(view.message.id, view)