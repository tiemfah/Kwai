import arcade

GRID = 32

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
    """
    can move, 
    can hit (dirt, enemy, coin),
    can fall 
    """
    MOVE_WAIT = 0.1
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.wait_time = 0
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL  # check off here
    
    def move(self, direction):
        self.x += GRID * DIR_OFFSETS[direction][0]
        self.y += GRID * DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        self.wait_time += delta

        if self.wait_time >= Player.MOVE_WAIT:
            self.move(self.direction)
            self.wait_time = 0
    
    def check_next(self, next_direction):  # check off here
        """
        HERERHERHERHER
        """
        next_x = self.x+ GRID * DIR_OFFSETS[direction][0]
        next_y = self.y+ GRID * DIR_OFFSETS[direction][1]


class Dirt:
    """
    can be destroy by player
    can block player
    """
    pass


class Nondirt:
    """
    can block player
    can have many "skin"
    """
    pass

 
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
