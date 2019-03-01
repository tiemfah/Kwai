import arcade
from models import *
 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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
 

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)

        # create game sprite
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('resources/images/lama.png',
                                         model=self.world.player)

    def update(self, delta):
        # update game logic
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        
        # draw sprite
        self.pacman_sprite.draw()
 
 
def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()
