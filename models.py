import arcade.key
from random import choice, choices
from math import ceil, floor

GRID = 32

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_DOWN: (0, 1),
               DIR_LEFT: (-1, 0)}

KEY_MAP = {arcade.key.W: DIR_UP,
           arcade.key.S: DIR_DOWN,
           arcade.key.A: DIR_LEFT,
           arcade.key.D: DIR_RIGHT, }


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
        self.next_direction = DIR_STILL
        self.GRID = GRID
        self.starting_point = y
        self.depth_score = 0
        self.pickup_score = 0
        self.battle_score = 0
        self.score = self.depth_score + self.pickup_score + self.battle_score

    def move(self, direction):
        self.x += GRID * DIR_OFFSETS[direction][0]
        self.y -= GRID * DIR_OFFSETS[direction][1]

    def update(self):
        if self.next_direction != DIR_STILL:
            if self.check_moveable(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = DIR_STILL
                self.move(self.direction)
            elif self.check_destructable(self.next_direction):
                self.destroy(self.next_direction)
                self.next_direction = DIR_STILL
        self.depth_score = (self.starting_point - self.y) // 32

    def get_row(self):
        return 18 - ceil(self.y / self.GRID)

    def get_col(self):
        return floor(self.x / self.GRID)
    
    def check_moveable(self, next_direction):
        # print('current', self.get_row(), self.get_col())
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        # print('next', new_r, new_c)
        return self.world.level.what_is_at(new_r, new_c) == 'air'
    
    def check_destructable(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        return self.world.level.what_is_at(new_r, new_c) == 'dirt'

    def destroy(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        self.world.level.break_dirt(new_r, new_c)


class Dirt:
    """
    can be destroy by player
    can block player
    """

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_dead = False


class Nondirt:
    """
    can block player
    can have many "skin"
    """

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Level:
    LEV_1_CAP = 20
    LEV_2_CAP = 40
    level_1_map = ['$$#...#$$',
                   '$$#DD.#$$',
                   '$$#D.D#$$',
                   '$$#.DD#$$']
    level_2_map = ['$#.....#$',
                   '$#DDDD.#$',
                   '$#DDD..#$',
                   '$#.DDDD#$',
                   '$#DD.DD#$',
                   '$#D.DDD#$',]
    """
    make platform
    TODO may be add coin?
    """

    def __init__(self, worldx):
        self.world = worldx
        self.map = self.start_map(9)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.previous_score = self.world.player.depth_score

    def start_map(self, n):
        temp = []
        for num in range(n):
            temp += self.choose_map()
        return temp
    
    def choice_n_time(self, n):
        possibility = ['.','.','.','#','D','D','D']
        temp = []
        for num in range(n):
            temp.append(choice(possibility))
        return temp
    
    def wild_random(self, level):
        if level == 1:
            return ''.join(['$$#'] + self.choice_n_time(3) + ['#$$'])
        elif level == 2:
            return ''.join(['$#'] + self.choice_n_time(5) + ['#$'])

    def choose_map(self):
        """
        pick random map that gives 2 block
        """
        if self.world.player.pickup_score < Level.LEV_1_CAP:
            return [self.wild_random(1), choice(Level.level_1_map)]
        else:
            return [Level.level_2_map[0], choice(Level.level_2_map)]

    def what_is_at(self, r, c):
        """
        name implies
        """
        if self.map[r][c] == "D":
            return "dirt"
        elif self.map[r][c] == "$":
            return "sky"
        elif self.map[r][c] == "#":
            return "stone"
        elif self.map[r][c] == ".":
            return "air"
    
    def break_dirt(self, r, c):
        self.map[r] = self.map[r][:c]+'.'+self.map[r][c+1:]

    def update(self):
        """
        see if map need new "block"
        """
        if self.previous_score + 1 == self.world.player.depth_score:
            self.map += self.choose_map()
            self.height = len(self.map)
            self.width = len(self.map[0])
            self.previous_score = self.world.player.depth_score


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, GRID // 2 + 3 * GRID, GRID * 17 + GRID // 2)
        self.level = Level(self)

    def update(self, delta):
        self.player.update()
        self.level.update()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.player.next_direction = KEY_MAP[key]

    def on_key_release(self):
        self.player.direction = DIR_STILL
