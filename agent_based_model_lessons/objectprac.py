class tree():
    def __init__(self,name):
      self.name = name
      self.height = 0
    def grow(self,x):
      self.height += x
      print(self.name, self.height)
    def fight(self, enemy):
      if enemy.height > self.height:
        print(self.name, "loses!")
        self.height -= 1
      elif enemy.height < self.height:
        print(self.name, "wins")
        enemy.height -= 1
      else:
        print("nobody wins, how boring :(")
        enemy.height -= 1
        self.height -= 1
class flower():
    def __init__(self,color):
      self.color = color
    def grow(self):
      print(self.color)
      

apple = tree("apple")
apple.grow(2)
apple.grow(5)
pine = tree("Pine")
pine.grow(9)
pine.fight(apple)
rose = flower("red")
rose.grow()