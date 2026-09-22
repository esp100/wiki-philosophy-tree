class Node:
  def __init__(self, value):
    self.value = value
    self.child = {}

  def contains(self, value):
    if self.value == value:
      return True
    return any(child.contains(value) for child in self.child.values())

  def search(self, value):
    if self.value == value:
      return self

    for child in self.child.values():
      found = child.search(value)
      if found:
        return found
    return None

  def basic_print(self, level=0):
    print("  " * level + str(self.value))
    for child in self.child.values():
      child.basic_print(level + 1)