"""
Platformer Game
"""
import arcade

# Constants
PLAYER_MOVEMENT_SPEED = 1
SAW_MOVEMENT_SPEED = 2
PIXELS_PER_TILE = 50
SCREEN_SIZE_TILES = (20, 10)
SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES = SCREEN_SIZE_TILES
SCREEN_SIZE_PIXELS = tuple([
    tiles*PIXELS_PER_TILE for tiles in SCREEN_SIZE_TILES
])
SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS = SCREEN_SIZE_PIXELS

SCREEN_TITLE = "Platformer"
HALF = PIXELS_PER_TILE/2
def tile2pixel(tile):
    return HALF+tile*PIXELS_PER_TILE
def pixel2tile(pixel):
    return (pixel-HALF)/PIXELS_PER_TILE
def MySprite(img, x, y):
    """ x and y are in units of tiles from bottom left """
    sprite = arcade.Sprite(img)
    sprite.center_x = tile2pixel(x)
    sprite.center_y = tile2pixel(y)
    return sprite

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.scene = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Saw")
        self.scene.add_sprite_list("Blocks", use_spatial_hash=True)
        self.player_sprite = MySprite("knife_shredder.png",1,1)
        self.scene.add_sprite("Player", self.player_sprite)
        for x in range(SCREEN_WIDTH_TILES):
            self.scene.add_sprite("Blocks", MySprite("block.png",x,0))
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Blocks")
        )
        self.saw_physics = None
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.B:
            x = pixel2tile(self.player_sprite.center_x)+1
            y = pixel2tile(self.player_sprite.center_y)
            saw_sprite = MySprite("flying_saw.png",x,y)
            saw_sprite.change_x = SAW_MOVEMENT_SPEED
            saw_sprite.change_y = SAW_MOVEMENT_SPEED
            self.scene.add_sprite("saw", saw_sprite)
            self.saw_physics = arcade.PhysicsEngineSimple(
                saw_sprite, self.scene.get_sprite_list("Blocks")
            )
            print(x)
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    def on_update(self, delta_time):
        """Movement and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()
        if self.saw_physics is not None:
            self.saw_physics.update()
    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Draw our sprites
        self.scene.draw()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
