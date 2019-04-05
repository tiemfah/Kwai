"TODO add trap, enemy"

import arcade.key
from random import choice, choices
from math import ceil, floor
from map_pool import *

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
    MOVE_WAIT = 0.15

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
        self.score = 0

    def move(self, direction):
        self.x += GRID * DIR_OFFSETS[direction][0]
        self.y -= GRID * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.wait_time += delta
        if self.wait_time > Player.MOVE_WAIT:
            next_block = self.what_next(self.next_direction)
            if self.next_direction != DIR_STILL:
                if next_block == 'gold':
                    self.remove_this(self.next_direction)
                    self.pickup_score += 1
                elif next_block == 'dirt':
                    self.remove_this(self.next_direction)
                elif next_block in ['air', 'trap']:
                    self.direction = self.next_direction
                    self.move(self.direction)
                self.next_direction = DIR_STILL
            else:
                next_block = self.what_next(DIR_DOWN)
                if next_block == 'gold':
                    self.remove_this(self.next_direction)
                    self.next_direction = DIR_STILL
                    self.pickup_score += 1
                if self.check_fall():
                    self.move(DIR_DOWN)
            self.wait_time = 0
        self.depth_score = (self.starting_point - self.y) // 32
        self.score = self.pickup_score + self.battle_score + (self.depth_score//3)

    def get_row(self):
        return 18 - ceil(self.y / self.GRID)

    def get_col(self):
        return floor(self.x / self.GRID)
    
    def check_fall(self):
        new_r = self.get_row()+1
        new_c = self.get_col()
        return self.world.level.what_is_at(new_r, new_c) in ['air', 'gold', 'trap']
    
    def remove_this(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        self.world.level.remove_this(new_r, new_c)
    
    def what_next(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        return self.world.level.what_is_at(new_r, new_c)
    
    def die(self):
        print('dedededed')


class Trap:
    def __init__(self, world, r, c):
        self.world = world
        self.r = r
        self.c = c
        self.is_near = self.is_player_near_me()
    
    def did_player_hit_me(self):
        return self.r == self.world.player.get_row() and self.c == self.world.player.get_col()
    
    def is_player_near_me(self):
        """
        show true color!
        """
        if self.world.player.get_row()-1<= self.r <= self.world.player.get_row()+1:
            if self.world.player.get_col()-1 <= self.c <= self.world.player.get_col()+1:
                return True
    
    def update(self):
        self.is_near = self.is_player_near_me()
        if self.did_player_hit_me():
            self.world.player.die()


class Level:
    def __init__(self, world):
        self.world = world
        self.map = self.start_map(9)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.previous_score = self.world.player.depth_score
        self.trap_list = []

    def start_map(self, n):
        temp = []
        for num in range(n):
            temp += self.choose_map()
        return temp

    def choose_map(self):
        """
        pick random map that gives 2 block
        """
        if self.world.player.depth_score < LEV_1_CAP:
            return [wild_random(1), choice(level_1_map)]
        else:
            return [wild_random(2), choice(level_2_map)]

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
        elif self.map[r][c] == 'T':
            return "trap"
        elif self.map[r][c] == ".":
            return "air"
        elif self.map[r][c] == "G":
            return "gold"
    
    def remove_this(self, r, c):
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
        
        for trap in self.trap_list:
            trap.update()


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, GRID // 2 + 3 * GRID, GRID * 17 + GRID // 2)
        self.level = Level(self)

    def update(self, delta):
        self.player.update(delta)
        self.level.update()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.player.next_direction = KEY_MAP[key]

    def on_key_release(self):
        self.player.direction = DIR_STILL
