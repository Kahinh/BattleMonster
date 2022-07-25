class Specializations:
  def __init__(
    self, 
    name,
    damage,
    stacks,
    cost
    ):
    self.name = name
    self.damage = damage
    self.stacks = stacks
    self.cost = cost

Specializations_list = {
  1: Specializations(
      name = "Guerrier",
      damage = 300,
      stacks = 20,
      cost = 0
  ),
  2: Specializations(
      name = "Douleur",
      damage = 400,
      stacks = 20,
      cost = 1000
  )
}
