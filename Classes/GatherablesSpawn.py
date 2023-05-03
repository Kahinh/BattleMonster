from dataclasses import dataclass

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