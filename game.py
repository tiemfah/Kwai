import arcade
from models import *

GRID = 32

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
    """
    TODO fix: generated block not being draw.
    """
    def __init__(self, levelmap):
        self.level = levelmap
        self.width = self.level.width
        self.height = self.level.height

        self.sky_sprite = arcade.Sprite('resources/images/sky.png')
        self.dirt_sprite = arcade.Sprite('resources/images/dirt.png')
        self.stone_sprite = arcade.Sprite('resources/images/stone.png')

    def get_sprite_position(self, r, c):
        x = c * GRID + (GRID // 2)
        y = SCREEN_HEIGHT - (r * GRID + GRID // 2)
        return x, y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                identity = self.level.what_is_at(r, c)
                if identity == "sky":
                    self.draw_sprite(self.sky_sprite, r, c)
                elif identity == "dirt":
                    self.draw_sprite(self.dirt_sprite, r, c)
                elif identity == "stone":
                    self.draw_sprite(self.stone_sprite, r, c)

    def update(self, Levelmap):
        self.level = Levelmap
        self.width = self.level.width
        self.height = self.level.height


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('resources/images/mc.png',
                                  model=self.world.player)

        self.map = LevelDrawer(self.world.level)
        self.view_bottom = 0

    def change_view(self):
        changed = True
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.world.player.y + 16 > top_bndry:
            self.view_bottom += self.world.player.y + 16 - top_bndry
            changed = True

        # Scroll down
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
        self.level_drawer = LevelDrawer(self.world.level)
        self.change_view()

    def on_draw(self):
        arcade.start_render()

        self.level_drawer.draw()
        self.player.draw()

        # show score
        output = f"Score: {self.world.player.score}"
        arcade.draw_text(output, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.RED, 14)

    def on_key_press(self, key, modifiers):
        self.world.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.world.on_key_release()


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
