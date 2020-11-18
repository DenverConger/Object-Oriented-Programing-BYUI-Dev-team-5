"""
Starting Template
Once you have learned how to use classes, you can begin your program with this
template.
If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import os
import random
import math

SCREEN_WIDTH = 1344
SCREEN_HEIGHT = 704
SCREEN_TITLE = "Arena"
SCALING = 0.5
MOVEMENT_SPEED = 10
OFFSCREEN_SPACE = 300
LEFT_LIMIT = 0
RIGHT_LIMIT = SCREEN_WIDTH
BOTTOM_LIMIT = 0
TOP_LIMIT = SCREEN_HEIGHT
starting_enemy_count = 3

class EnemySprite(arcade.Sprite):
    """ Sprite that represents an enemy. """

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0

    def update(self):
        """ Move the enemy around. """
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = LEFT_LIMIT
            self.change_x *= -1
        if self.center_x > RIGHT_LIMIT:
            self.center_x = RIGHT_LIMIT
            self.change_x *= -1
        if self.center_y > TOP_LIMIT:
            self.center_y = TOP_LIMIT
            self.change_y *= -1
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = BOTTOM_LIMIT
            self.change_y *= -1

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        # Sprite Lists Initialization
        self.all_sprites = None
        self.wall_list = None
        self.enemy_list = None
        
        # Lets us use relative file paths
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.player = arcade.Sprite("resources/images/player_circle.png", SCALING)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.all_sprites = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
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
        self.all_sprites.append(self.player)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        """



        Having an issue trying to figure out how to make enemy_sprite global 
        so it can be used betetr in collision detection against walls
        for lines below when used in on_update for collisions




        """
        for i in range(starting_enemy_count):
            image_no = random.randrange(4)
            enemy_sprite = EnemySprite("resources/images/enemy_square.png", SCALING * .5)

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1


            enemy_sprite.size = 4

            #self.all_sprites.append(enemy_sprite)
            self.enemy_list.append(enemy_sprite)


    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.all_sprites.draw()
        self.enemy_list.draw()
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
        
        # Updates all sprites. Do we want to update even the walls and whatnot? We might need to for screen scrolling. 
        self.all_sprites.update()
        self.enemy_list.update()

        enemies = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if len(enemies) > 0:
                enemies[0].remove_from_sprite_lists()


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
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()