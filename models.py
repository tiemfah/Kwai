import arcade

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

KEY_MAP = { arcade.key.UP: DIR_UP,
            arcade.key.DOWN: DIR_DOWN,
            arcade.key.LEFT: DIR_LEFT,
            arcade.key.RIGHT: DIR_RIGHT, }


class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
    
    def move(self, direction):
        self.x += DIR_OFFSETS[direction][0]
        self.y += DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        self.move(self.direction)
 
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.player = Player(self, width // 2, height // 2)
 
    def update(self, delta):
        self.player.update(delta)
    
    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.player.direction = KEY_MAP[key]
    
    def on_key_release(self):
        self.player.direction = DIR_STILL
