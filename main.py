"""
Starting Template
Once you have learned how to use classes, you can begin your program with this
template.
If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import os
import math

SCREEN_WIDTH = 1344
SCREEN_HEIGHT = 704
SCREEN_TITLE = "Arena"
SCALING = 0.5
MOVEMENT_SPEED = 10



class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        # Sprite Lists Initialization
        self.player_list = None
        self.all_sprites = None
        self.wall_list = None
        
        self.mouse_x = 1
        self.mouse_y = 1
        
        # Lets us use relative file paths
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.player = arcade.Sprite("resources/images/player_circle.png", SCALING)
        self.player_triangle = arcade.Sprite("resources/images/player_arrow.png", SCALING)
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.all_sprites = arcade.SpriteList()
        wall_img = ":resources:images/tiles/brickBrown.png"
        

        for x in range(32, SCREEN_WIDTH, 64):
            wall_top = arcade.Sprite(wall_img, SCALING)
            wall_top.center_x = x
            wall_top.center_y = SCREEN_HEIGHT - 32
            self.wall_list.append(wall_top)
            self.all_sprites.append(wall_top)

            wall_bottom = arcade.Sprite(wall_img, SCALING)
            wall_bottom.center_x = x
            wall_bottom.center_y = 32
            self.wall_list.append(wall_bottom)
            self.all_sprites.append(wall_bottom)
        for y in range(96, SCREEN_HEIGHT - 64, 64):
            wall_left = arcade.Sprite(wall_img, SCALING)
            wall_left.center_y = y
            wall_left.center_x = 32
            self.wall_list.append(wall_left)
            self.all_sprites.append(wall_left)

            wall_right = arcade.Sprite(wall_img, SCALING)
            wall_right.center_y = y
            wall_right.center_x = SCREEN_WIDTH - 32
            self.wall_list.append(wall_right)
            self.all_sprites.append(wall_right)
        
        self.player.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_triangle.position = self.player.position
        self.player_list.append(self.player)
        self.all_sprites.append(self.player)
        self.player_list.append(self.player_triangle)
        self.all_sprites.append(self.player_triangle)


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
        self.player.change_x = 0
        self.player.change_y = 0

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
        
        self.player_triangle.position = self.player.position        # This line uncommented makes it wobbly. I kind of like it wobbly. Needs to be uncommented even if you also use the line below.  
        self.player_triangle.velocity = self.player.velocity        # This line uncommented makes it strict. 

        diff1 = self.mouse_y - self.player_triangle.center_y
        diff2 = self.mouse_x - self.player_triangle.center_x
        if diff2 == 0:
            diff2 = 1
        angle = (180 / math.pi) * (math.atan(diff1 / diff2)) - 90
        if diff2 < 0:
            self.player_triangle.angle = angle + 180
        else:
            self.player_triangle.angle = angle

        # Updates all sprites. Do we want to update even the walls and whatnot? We will probably need to for screen scrolling. 
        self.all_sprites.update()   
        
    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """

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
        # self.player.position = (self.player.center_x + dx, self.player.center_y + dy)       # Change Mouse Movement
        # self.player.position = (x, y)                                                       # Mouse Movement

        self.mouse_x = x
        self.mouse_y = y

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
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()