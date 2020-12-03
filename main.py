"""
This is our game
"""
import arcade
import os
import random
import math
from datetime import datetime, timedelta # For seeding random number generation.
import sys

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
starting_enemy_count = 30
personality = "random"
SPRITE_SPEED = 0.5

class EnemySprite(arcade.Sprite):
    """ Sprite that represents an enemy. 
        Denver - I plan on Adding a intelligence to the enemy
        there is no documentation for it so 
        i have to do it custom"""

        # """Kyler: Could we add all of enemy's behaviors into this class?"""

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0



    def movement(self, player, enemy):

            if enemy.center_y < player.center_y:
                enemy.center_y += min(SPRITE_SPEED, player.center_y - enemy.center_y)
            elif enemy.center_y > player.center_y:
                enemy.center_y -= min(SPRITE_SPEED, enemy.center_y - player.center_y)
            if enemy.center_x < player.center_x:
                enemy.center_x += min(SPRITE_SPEED, player.center_x - enemy.center_x)
            elif enemy.center_x > player.center_x:
                enemy.center_x -= min(SPRITE_SPEED, enemy.center_x - player.center_x)

class Bullets():

    def __init__(self):
        self.bullet_list = arcade.SpriteList()
        self.bullet_speed = 50
        self.bullet_sprite = ":resources:images/space_shooter/laserBlue01.png"
    
    def create_bullet(self, mouse_x, mouse_y, player_x, player_y):
        self.bullet = arcade.Sprite(self.bullet_sprite)
        self.bullet.position = (player_x, player_y)

        diff_x = mouse_x - player_x 
        diff_y = mouse_y - player_y
        bullet_angle = math.atan2(diff_y, diff_x)

        self.bullet.velocity = (math.cos(bullet_angle) * self.bullet_speed, math.sin(bullet_angle) * self.bullet_speed)
        self.bullet.radians = bullet_angle

        self.bullet_list.append(self.bullet)

    def draw(self):
        self.bullet_list.draw()

    def update(self):
        self.bullet_list.update()
        
        
        
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        # Sprite Lists Initialization
        self.all_sprites = None
        self.wall_list = None
        self.enemy_list = None
        self.player_list = None
        self.player = None
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
        self.enemy_list = arcade.SpriteList()
        wall_img = ":resources:images/tiles/brickBrown.png"
        self.player.center_x = 50
        self.player.center_y = 50
        self.bullets = Bullets()
        
        
        # Summoning Walls
        """for x in range(32, SCREEN_WIDTH, 64):
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
            self.all_sprites.append(wall_right)"""
        
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

        self.current_map = None
        self.load_map(self.current_map)

        for i in range(starting_enemy_count):
            image_no = random.randrange(4)
            enemy_sprite = EnemySprite("resources/images/enemy_square.png", SCALING * .5)

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT + 100, TOP_LIMIT - 100)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT + 100, RIGHT_LIMIT - 100)

            self.all_sprites.append(enemy_sprite)
            self.enemy_list.append(enemy_sprite)
    
    def load_map(self, map):
        map = arcade.tilemap.read_tmx('resources/maps/map1.tmx')

        self.wall_list = arcade.tilemap.process_layer(map, 'Walls', 2)
        self.floor_list = arcade.tilemap.process_layer(map, 'Floor', 2)
        self.background_list = arcade.tilemap.process_layer(map, 'Ground', 2)
        
        self.wall_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    
    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Drawing map lists
        self.background_list.draw()
        self.floor_list.draw()
        self.wall_list.draw()
        self.bullets.draw()

        # Call draw() on all your sprite lists below
        self.all_sprites.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        # self.physics_engine.update()
        self.wall_physics.update()
        self.player.change_y = 0
        self.player.change_x = 0
        playa = 0


        for enemy in self.enemy_list:
            
            EnemySprite.movement(self, self.player, enemy)


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

        # Updates all sprites. Do we want to update even the walls and whatnot? We might need to for screen scrolling. 
        self.all_sprites.update()
        self.enemy_list.update()

        enemies = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if len(enemies) > 0:
                enemies[0].remove_from_sprite_lists()
        
        for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                    enemy.change_y *= -1
        for enemy in self.enemy_list:
                # If the enemy hits an enemy, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.enemy_list)) > 0:
                    enemy.change_x *= -1
                    enemy.change_y *= -1
        self.bullets.update()

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
        self.bullets.create_bullet(x, y, self.player.center_x, self.player.center_y)

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
