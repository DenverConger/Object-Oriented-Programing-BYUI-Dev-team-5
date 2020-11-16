"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import os

SCREEN_WIDTH = 1350
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Arena"
MOVEMENT_SPEED = 50


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        # Sprite Lists Initialization
        self.all_sprites = arcade.SpriteList()
        
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        
        self.player = arcade.Sprite("images/player_circle.png", 1)
        self.player.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # self.player.center_y = SCREEN_HEIGHT / 2
        # self.player.center_x = SCREEN_WIDTH / 2

        self.all_sprites.append(self.player)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.all_sprites.draw()

    def on_update(self, delta_time):
        self.player.change_y = 0
        self.player.change_x = 0


        # Keyboard Movement
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVEMENT_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        # If you press both up and down, you can move the player right, but not left. If you press right and left, you can move the player down, but not up.

        # Hitting Edges of Screen
        if self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH
        

        self.all_sprites.update()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True

        if key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        # These two lines are two types of player motion based on the mouse. Uncomment to unlock the motion.
        self.player.position = (self.player.center_x + dx, self.player.center_y + dy)       # Change Mouse Movement
        self.player.position = (x, y)                                                       # Mouse Movement

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
#this is a comment

def main():
    """ Main method """
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()