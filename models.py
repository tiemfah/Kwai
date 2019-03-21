import arcade


class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
 
    def update(self, delta):
        pass
 
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.player = Player(self, width // 2, height // 2)
 
    def update(self, delta):
        self.player.update(delta)
    