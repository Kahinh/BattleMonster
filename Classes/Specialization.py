class Specializations:
  def __init__(
    self, 
    name,
    description,
    damage,
    stacks,
    cost
    ):
    self.name = name
    self.description = description
    self.damage = damage
    self.stacks = stacks
    self.cost = cost

Specializations_list = {
  1: Specializations(
      name = "Guerrier",
      description = "test",
      damage = 300,
      stacks = 20,
      cost = 0
  ),
  2: Specializations(
      name = "Douleur",
      description = "test",
      damage = 400,
      stacks = 20,
      cost = 1000
  )
}
