"""
Starting Template
Once you have learned how to use classes, you can begin your program with this
template.
If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SCREEN_WIDTH = 1350
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):
    """
    Main application class.
    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.wall_list = None


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        sprite_img = ":resources:images/tiles/brickBrown.png"

        for x in range(0, 1350, 64):
            wall_top = arcade.Sprite(sprite_img, 0.5)
            wall_top.center_x = x
            wall_top.center_y = 668
            self.wall_list.append(wall_top)

            wall_bottom = arcade.Sprite(sprite_img, 0.5)
            wall_bottom.center_x = x
            wall_bottom.center_y = 32
            self.wall_list.append(wall_bottom)

        for y in range(96, 636, 64):

            wall_left = arcade.Sprite(sprite_img, 0.5)
            wall_left.center_y = y
            wall_left.center_x = 32
            self.wall_list.append(wall_left)

            wall_right = arcade.Sprite(sprite_img, 0.5)
            wall_right.center_y = y
            wall_right.center_x = 1318
            self.wall_list.append(wall_right)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.wall_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

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


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()