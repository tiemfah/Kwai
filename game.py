import arcade

from models import *

GRID = 32

SCREEN_TITLE = 'LAMA X'
SCREEN_WIDTH = GRID * 9
SCREEN_HEIGHT = GRID * 18
VIEWPORT_MARGIN = GRID * 8


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class LevelDrawer():
    def __init__(self, levelmap):
        self.level = levelmap
        self.width = self.level.width
        self.height = self.level.height
        self.model_dict = {'0': ModelSprite('resource/img/0.png'),
                           '1': ModelSprite('resource/img/1.png'),
                           '2': ModelSprite('resource/img/2.png'),
                           '3': ModelSprite('resource/img/3.png'),
                           '4': ModelSprite('resource/img/4.png'),
                           '5': ModelSprite('resource/img/5.png'),
                           '6': ModelSprite('resource/img/6.png'),
                           '7': ModelSprite('resource/img/7.png'),
                           '8': ModelSprite('resource/img/8.png'),
                           '9': ModelSprite('resource/img/9.png'),
                           '10': ModelSprite('resource/img/10.png'),
                           '11': ModelSprite('resource/img/11.png'),
                           '12': ModelSprite('resource/img/12.png'),
                           '13': ModelSprite('resource/img/13.png'),
                           '14': ModelSprite('resource/img/14.png'), }

    def get_sprite_position(self, r, c):
        x = c * GRID + (GRID // 2)
        y = SCREEN_HEIGHT - (r * GRID + GRID // 2)
        return x, y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        start = self.level.world.player.depth_score - 10 if self.level.world.player.depth_score > 10 else 0
        stop = self.level.world.player.depth_score + 9 if self.level.world.player.depth_score > 10 else 18
        for r in range(start, stop):
            for c in range(self.width):
                identity = self.level.what_is_at(r, c)
                if identity == "trap":
                    if (r, c) not in self.level.trap_list_index:
                        self.level.trap_list.append(Trap(self.level.world, r, c))
                        self.level.trap_list_index.append((r, c))
                elif identity == 'air':
                    pass
                else:
                    self.draw_sprite(self.model_dict[self.level.map[r][c]], r, c)

    def update(self, Levelmap):
        self.level = Levelmap
        self.height = self.level.height


class TrapDrawer():
    def __init__(self, world):
        self.world = world
        self.trap_list = world.level.trap_list
        self.trap_sprite_dict = {'15': ModelSprite('resource/img/15.png'),
                                 '16': ModelSprite('resource/img/16.png'),
                                 '17': ModelSprite('resource/img/17.png'),
                                 '18': ModelSprite('resource/img/18.png'),
                                 '19': ModelSprite('resource/img/19.png'),
                                 '20': ModelSprite('resource/img/20.png'),
                                 '21': ModelSprite('resource/img/21.png'),
                                 '22': ModelSprite('resource/img/22.png'),
                                 '23': ModelSprite('resource/img/23.png'),
                                 'alerted': ModelSprite('resource/img/trap_alert.png')}

    def get_sprite_position(self, r, c):
        x = c * GRID + (GRID // 2)
        y = SCREEN_HEIGHT - (r * GRID + GRID // 2)
        return x, y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for trap in self.trap_list:
            if trap.is_near:
                self.draw_sprite(self.trap_sprite_dict['alerted'], trap.r, trap.c)
            else:
                self.draw_sprite(self.trap_sprite_dict[self.world.level.map[trap.r][trap.c]], trap.r, trap.c)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bg = arcade.load_texture('resource/img/bg.png')
        self.help = arcade.load_texture('resource/img/help.png')
        self.top = arcade.load_texture('resource/img/top.png')
        self.pause = arcade.load_texture('resource/img/pause.png')
        self.gameover = arcade.load_texture('resource/img/gameover.png')
        self.player_dict = {'l0': ModelSprite('resource/img/player/l0.png', model=self.world.player),
                            'l1': ModelSprite('resource/img/player/l1.png', model=self.world.player),
                            'r0': ModelSprite('resource/img/player/r0.png', model=self.world.player),
                            'r1': ModelSprite('resource/img/player/r1.png', model=self.world.player),
                            's0': ModelSprite('resource/img/player/s0.png', model=self.world.player),
                            's1': ModelSprite('resource/img/player/s1.png', model=self.world.player),
                            'd0': ModelSprite('resource/img/player/d0.png', model=self.world.player)}
        self.map = LevelDrawer(self.world.level)
        self.traps = TrapDrawer(self.world)
        self.view_bottom = 0

    def change_view(self):
        changed = True
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.world.player.y + 16 > top_bndry:
            self.view_bottom += self.world.player.y + 16 - top_bndry
            changed = True

        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.world.player.y - 16 < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.world.player.y - 16
            changed = True

        if changed:
            arcade.set_viewport(0, SCREEN_WIDTH,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def update(self, delta):
        self.world.update(delta)
        self.map.update(self.world.level)
        self.change_view()
    
    def getting_dark(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, self.world.player.y + 48, SCREEN_WIDTH, 
                                        SCREEN_HEIGHT, (25, 14, 27, self.world.player.opacity))
    
    def draw_torchbar(self):
        torch_length = 0 if self.world.player.torchlife == 0 else self.world.player.torchlife // 2
        arcade.draw_line(SCREEN_WIDTH // 2 - torch_length, self.world.player.y + 288,
                            SCREEN_WIDTH // 2 + torch_length, self.world.player.y + 289,
                            arcade.color.WHITE, 5)
    
    def draw_gameover(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, self.world.player.y + 70, 288, 95, self.gameover)
        arcade.draw_text(f"{self.world.player.score}", SCREEN_WIDTH // 1.8, self.world.player.y + 45, arcade.color.GOLD, 20)

    def draw_score(self):
        x_increment = 35
        for char in str(self.world.player.score):
            arcade.draw_texture_rectangle(SCREEN_WIDTH//2 + x_increment, self.view_bottom + SCREEN_HEIGHT//2, 30, 34, arcade.load_texture(f'resource/img/number/{char}.png'))
            x_increment += 35

    def on_draw(self):
        arcade.start_render()
        # draw the game
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, self.view_bottom + SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.map.draw()
        self.traps.draw()
        self.player_dict[self.world.player.facing].draw()
        if self.world.player.depth_score < 10:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, self.world.player.starting_point + 144, 288, 256, self.top)
        else:
            self.getting_dark()
            self.draw_torchbar()
        # draw overlay -> help, pause, gameover
        if self.world.state == 'HELP':
            arcade.draw_texture_rectangle(SCREEN_WIDTH//2, self.view_bottom + SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.help)
        elif self.world.state == 'PAUSE':
            arcade.draw_texture_rectangle(SCREEN_WIDTH//2, self.view_bottom + SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.pause)
        elif self.world.state == 'OVER':
            arcade.draw_texture_rectangle(SCREEN_WIDTH//2, self.view_bottom + SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.gameover)
            self.draw_score()

    def on_key_press(self, key, modifiers):
        self.world.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.world.on_key_release()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.world.state == 'OVER':
                self.restart()

    def restart(self):
        arcade.set_background_color((25, 14, 27))
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.map = LevelDrawer(self.world.level)
        self.player_dict = {'l0': ModelSprite('resource/img/player/l0.png', model=self.world.player),
                            'l1': ModelSprite('resource/img/player/l1.png', model=self.world.player),
                            'r0': ModelSprite('resource/img/player/r0.png', model=self.world.player),
                            'r1': ModelSprite('resource/img/player/r1.png', model=self.world.player),
                            's0': ModelSprite('resource/img/player/s0.png', model=self.world.player),
                            's1': ModelSprite('resource/img/player/s1.png', model=self.world.player),
                            'd0': ModelSprite('resource/img/player/d0.png', model=self.world.player)}
        self.traps = TrapDrawer(self.world)
        self.view_bottom = 0


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
