class Block:
  """Block Class: This class represents the individual blocks on the game board. It contains the color of the block and methods to set and get the color."""
  def __init__(self, color):
    self.color = color

  def set_color(self, color):
    self.color = color

  def get_color(self):
    return self.color

  def __str__(self):
    return f"Colored {self.color} block"

  def __repr__(self):
    return f"<Color: {self.color}>"
