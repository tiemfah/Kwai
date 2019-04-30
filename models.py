import arcade.key
from math import ceil, floor
from time import time
from map_pool import *

GRID = 32
SCREEN_HEIGHT = GRID * 18

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
           arcade.key.D: DIR_RIGHT}


class Player:
    MOVE_WAIT = 0.15

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.wait_time = 0
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL
        self.starting_point = y
        self.depth_score = 0
        self.pickup_score = 0
        self.score = 0
        self.torchlife = 100
        self.opacity = 255
        self.facing = 'r0'

    def move(self, direction):
        self.x += GRID * DIR_OFFSETS[direction][0]
        self.y -= GRID * DIR_OFFSETS[direction][1]
        
    def update_facing(self, direction):
        if direction == DIR_RIGHT:
            self.facing = f'r{int(time())%2}'
        elif direction == DIR_LEFT:
            self.facing = f'l{int(time())%2}'
        else:
            self.facing = f's{int(time())%2}'

    def update(self, delta):
        self.wait_time += delta
        self.pick_up_at_me()
        if self.wait_time > Player.MOVE_WAIT:
            self.update_facing(self.next_direction)
            self.get_opacity()
            self.torchlife -= 1
            if self.torchlife <= 0:
                self.die()
            next_block = self.what_next(self.next_direction)
            if self.next_direction != DIR_STILL:
                if next_block == 'torch':
                    self.remove_this(self.next_direction)
                    self.picked_torch()
                elif next_block == 'dirt':
                    self.remove_this(self.next_direction)
                elif next_block in ['air', 'trap']:
                    self.direction = self.next_direction
                    self.move(self.direction)
                self.next_direction = DIR_STILL
            else:
                next_block = self.what_next(DIR_DOWN)
                if self.check_fall():
                    self.move(DIR_DOWN)
            self.wait_time = 0
        self.depth_score = (self.starting_point - self.y) // 32
        self.score = self.pickup_score + self.depth_score//3

    def get_row(self):
        return 18 - ceil(self.y / GRID)

    def get_col(self):
        return floor(self.x / GRID)
    
    def check_fall(self):
        return self.world.level.what_is_at(self.get_row()+1, self.get_col()) in ['air', 'torch', 'trap']
    
    def remove_this(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        self.world.level.remove_this(new_r, new_c)
    
    def what_next(self, next_direction):
        new_r = self.get_row() + DIR_OFFSETS[self.next_direction][1]
        new_c = self.get_col() + DIR_OFFSETS[self.next_direction][0]
        return self.world.level.what_is_at(new_r, new_c)
    
    def picked_torch(self):
        self.pickup_score += 1
        self.torchlife += 40
        if self.torchlife > 100:
            self.torchlife = 100
    
    def pick_up_at_me(self):
        r, c = self.get_row(), self.get_col()
        if self.world.level.what_is_at(r, c) == 'torch':
            self.remove_this(DIR_STILL)
            self.picked_torch()

    def die(self):
        self.world.game_over = True

    def get_opacity(self):
        if self.torchlife <= 0:
            self.die()
        else:
            self.opacity = int(255 - 255*((self.world.player.torchlife-20)/100))


class Trap:
    def __init__(self, world, r, c):
        self.world = world
        self.r = r
        self.c = c
        self.is_near = self.is_player_near_me()
    
    def did_player_hit_me(self):
        return self.r == self.world.player.get_row() and self.c == self.world.player.get_col()
    
    def is_player_near_me(self):
        if self.world.player.get_row()-2<= self.r <= self.world.player.get_row()+2:
            if self.world.player.get_col()-2 <= self.c <= self.world.player.get_col()+2:
                return True
    
    def update(self):
        self.is_near = self.is_player_near_me()
        if self.did_player_hit_me():
            self.world.player.die()


class Level:
    def __init__(self, world):
        self.world = world
        self.map = []+get_map()
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.previous_score = self.world.player.depth_score
        self.trap_list = []
        self.trap_list_index = []
        self.item_dict = {'-1': 'air',
                          '0': 'dirt',
                          '1': 'dirt',
                          '2': 'dirt',
                          '3': 'dirt',
                          '4': 'dirt',
                          '5': 'dirt',
                          '6': 'dirt',
                          '7': 'dirt',
                          '8': 'dirt',
                          '9': 'stone',
                          '10': 'stone',
                          '11': 'stone',
                          '14': 'torch',
                          '15': 'trap',
                          '16': 'trap',
                          '17': 'trap',
                          '18': 'trap',
                          '19': 'trap',
                          '20': 'trap',
                          '21': 'trap',
                          '22': 'trap',
                          '23': 'trap',}

    def what_is_at(self, r, c):
        return self.item_dict[self.map[r][c]]
    
    def remove_this(self, r, c):
        self.map[r][c] = '-1'

    def update(self):
        if self.previous_score + 9 == self.world.player.depth_score:
            add_map(self.map)
            self.height = len(self.map)
            self.previous_score = self.world.player.depth_score
        
        for trap in self.trap_list:
            if SCREEN_HEIGHT - (trap.r * GRID + GRID // 2) > self.world.player.y + GRID*9:
                self.trap_list.remove(trap)
            trap.update()


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, GRID // 2 + 3 * GRID, GRID * 17 + GRID // 2)
        self.level = Level(self)
        self.game_over = False

    def update(self, delta):
        self.player.update(delta)
        self.level.update()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.player.next_direction = KEY_MAP[key]

    def on_key_release(self):
        self.player.direction = DIR_STILL
