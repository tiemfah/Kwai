import arcade
from models import *
 
GRID = GRID
SCREEN_WIDTH = GRID * 9
SCREEN_HEIGHT = GRID * 18


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


class LevelGenerator():
    def __init__(self, Levelmap):
        self.level = Levelmap
        self.width = self.level.width
        self.height = self.level.height

        self.sky_sprite = arcade.Sprite('resources/images/sky.png')
        self.dirt_sprite = arcade.Sprite('resources/images/dirt.png')
        self.stone_sprite = arcade.Sprite('resources/images/stone.png')

    def get_sprite_pos(self, r, c):
        x = (c * GRID + (GRID // 2))
        y = SCREEN_HEIGHT- ((r-1) * GRID + (GRID + (GRID // 2)))
        return x,y
    
    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_pos(r, c)
        sprite.set_position(x, y)
        sprite.draw()
    
    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                iden =  self.level.what_is_at(r, c)
                if iden == "sky":
                    self.draw_sprite(self.sky_sprite, r, c)
                elif iden == "dirt":
                    self.draw_sprite(self.dirt_sprite, r, c)
                elif iden == "stone":
                    self.draw_sprite(self.stone_sprite, r, c)
 

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.WHITE)
        
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('resources/images/mc.png',
                                         model=self.world.player)
        self.map = LevelGenerator(self.world.level)

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        
        self.map.draw()
        self.player.draw()
    
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
