class Specialization:
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

Specializations = {
  1: Specialization(
      name = "Guerrier",
      description = "test",
      damage = 300,
      stacks = 20,
      cost = 0
  ),
  2: Specialization(
      name = "Douleur",
      description = "test",
      damage = 400,
      stacks = 20,
      cost = 1000
  )
}
