import arcade
import time
import collections
from models import *

GRID = 32

SCREEN_TITLE = 'LAMA X'
SCREEN_WIDTH = GRID * 9
SCREEN_HEIGHT = GRID * 18
VIEWPORT_MARGIN = GRID * 8

"""FPS"""
class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


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
        self.drawing_plan = {'sky': ModelSprite('resources/images/sky.png'),
                             'dirt': ModelSprite('resources/images/dirt.png'),
                             'stone': ModelSprite('resources/images/stone.png'),
                             'gold': ModelSprite('resources/images/gold.png')}

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
        stop = self.level.world.player.depth_score + 8 if self.level.world.player.depth_score > 10 else 18
        for r in range(start, stop):
            for c in range(self.width):
                identity = self.level.what_is_at(r, c)
                if identity == "trap":
                    if (r,c) not in self.level.trap_list_index:
                        self.level.trap_list.append(Trap(self.level.world, r, c))
                        self.level.trap_list_index.append((r,c))
                elif identity == "air":
                    pass
                else:
                    self.draw_sprite(self.drawing_plan[identity], r, c)
                    

    def update(self, Levelmap):
        self.level = Levelmap


class TrapDrawer():
    def __init__(self, world):
        self.world = world
        self.trap_list = world.level.trap_list
        self.trap_sprite = ModelSprite('resources/images/trap.png')
        self.trap_alerted_sprite = ModelSprite('resources/images/trap_alert.png')
    
    def get_sprite_position(self, r, c):
        x = c * GRID + (GRID // 2)
        y = SCREEN_HEIGHT - (r * GRID + GRID // 2)
        return x, y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()
    
    def in_screen(self, r):
        return self.world.player.x - SCREEN_WIDTH//2<= SCREEN_HEIGHT - (r * GRID + GRID // 2) <= self.world.player.x + SCREEN_HEIGHT//2

    def draw(self):
        for trap in self.trap_list:
            if trap.is_near:
                self.draw_sprite(self.trap_alerted_sprite, trap.r, trap.c)
            else:
                self.draw_sprite(self.trap_sprite, trap.r, trap.c)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('resources/images/mc.png',
                                  model=self.world.player)
        self.map = LevelDrawer(self.world.level)
        self.traps = TrapDrawer(self.world)
        self.view_bottom = 0

        """FPS"""
        self.fps = FPSCounter()

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

    def on_draw(self):
        arcade.start_render()
        if not self.world.game_over:
            self.map.draw()
            self.traps.draw()
            self.player.draw()
            
            """FPS"""
            arcade.draw_text(f'{self.fps.get_fps():.0f}', SCREEN_WIDTH//2, self.world.player.y+30, arcade.color.GOLD, 20)
            self.fps.tick()
        else:
            arcade.draw_text('GAME OVER', SCREEN_WIDTH//3.5,self.world.player.y+60, arcade.color.BLACK, 20)
            arcade.draw_text(f"Score: {self.world.player.score}", SCREEN_WIDTH//3,self.world.player.y+30, arcade.color.GOLD, 20)
            arcade.draw_text('click to restart',SCREEN_WIDTH//4.4,self.world.player.y, arcade.color.BLACK, 20)

    def on_key_press(self, key, modifiers):
        self.world.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.world.on_key_release()
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.world.game_over:
                self.restart()
    
    def restart(self):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('resources/images/mc.png', model=self.world.player)
        self.map = LevelDrawer(self.world.level)
        self.traps = TrapDrawer(self.world)
        self.view_bottom = 0


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
