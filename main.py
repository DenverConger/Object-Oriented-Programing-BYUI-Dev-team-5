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
MOVEMENT_SPEED = 7  
OFFSCREEN_SPACE = 300
LEFT_LIMIT = 0
RIGHT_LIMIT = SCREEN_WIDTH
BOTTOM_LIMIT = 0
TOP_LIMIT = SCREEN_HEIGHT
SPRITE_SPEED = 1    
starting_enemy_count = 10
personality = "random"


# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 250

class Scrolling():
    def __init__(self, player):
        self.view_bottom = 0
        self.view_left = 0
        self.player = player
        self.changed = False

    def scroll_left(self):
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.player.left
            self.changed = True

    def scroll_right(self):
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.player.right > right_boundary:
            self.view_left += self.player.player.right - right_boundary
            self.changed = True

    def scroll_up(self):
        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.player.top > top_boundary:
            self.view_bottom += self.player.player.top - top_boundary
            self.changed = True

    def scroll_down(self):
        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.player.bottom
            self.changed = True

        if self.changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

class EnemySprite(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        self.player_detected = False
        self.shot_timer = 30

    def detect_player(self, player):
        for enemy in self.enemy_list:
            if (math.sqrt(((enemy.center_y - player.center_y))**2 + ((enemy.center_x - player.center_x))**2) < 650): 
                if arcade.has_line_of_sight(player.position, enemy.position, self.map.wall_list):
                    enemy.player_detected = True
                else: 
                    enemy.player_detected = False

    def movement(self, player):
        for enemy in self.enemy_list:
            if enemy.player_detected:
                if enemy.center_y < player.center_y:
                    enemy.center_y += min(SPRITE_SPEED, player.center_y - enemy.center_y)
                elif enemy.center_y > player.center_y:
                    enemy.center_y -= min(SPRITE_SPEED, enemy.center_y - player.center_y)
                if enemy.center_x < player.center_x:
                    enemy.center_x += min(SPRITE_SPEED, player.center_x - enemy.center_x)
                elif enemy.center_x > player.center_x:
                    enemy.center_x -= min(SPRITE_SPEED, enemy.center_x - player.center_x)

    def attack(self, player):
        for enemy in self.enemy_list:
            if enemy.player_detected:
                if enemy.shot_timer % 60 == 0:
                    self.enemy_bullets.create_bullet(player.center_x, player.center_y, enemy.center_x, enemy.center_y)
                enemy.shot_timer += .5
                    
    def update_enemy(self):
        EnemySprite.detect_player(self, self.player.player)
        EnemySprite.movement(self, self.player.player)
        EnemySprite.attack(self, self.player.player)

        enemies = arcade.check_for_collision_with_list(self.player.player, self.enemy_list)
        if len(enemies) > 0:
                enemies[0].remove_from_sprite_lists()
                
        self.enemy_list.update()
        
        self.enemy_bullets.update(self.scrolling.view_left, self.scrolling.view_bottom, self.map.wall_list)
        
    def creation(self):
        for i in range(starting_enemy_count):
            image_no = random.randrange(4)
            enemy_sprite = EnemySprite("resources/images/enemy_square.png", SCALING * .5)
           
            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT + 100, TOP_LIMIT - 100)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT + 100, RIGHT_LIMIT - 100)

            self.enemy_list.append(enemy_sprite)

class Bullets():
    def __init__(self, bullet_speed):
        self.bullet_list = arcade.SpriteList()
        self.bullet_speed = bullet_speed
        self.bullet_sprite = "resources/images/laserBlue01.png"
    
    def create_bullet(self, dest_x, dest_y, start_x, start_y):
        self.bullet = arcade.Sprite(self.bullet_sprite)
        self.bullet.position = (start_x, start_y)

        diff_x = dest_x - start_x 
        diff_y = dest_y - start_y
        bullet_angle = math.atan2(diff_y, diff_x)
        
        # determine bullet velocity
        self.bullet.velocity = (math.cos(bullet_angle) * self.bullet_speed, math.sin(bullet_angle) * self.bullet_speed)
        # rotate sprite image so the bullet shoots straight
        self.bullet.radians = bullet_angle

        self.bullet_list.append(self.bullet)

    def draw(self):
        self.bullet_list.draw()

    def update(self, view_left, view_bottom, wall_list):
        self.bullet_list.update()
        for bullet in self.bullet_list:

            # remove bullet if it leaves screen
            if bullet.center_x < view_left or bullet.center_x > view_left + SCREEN_WIDTH or bullet.center_y < view_bottom or bullet.center_y > view_bottom + SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

            # If bullet hits a wall, remove bullet
            if len(arcade.check_for_collision_with_list(bullet, wall_list)) > 0:
                bullet.remove_from_sprite_lists()

    def update_hit(self, view_left, view_bottom, enemy_list):
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, enemy_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                
                hit_list[0].remove_from_sprite_lists()

    def update_hit_player(self, view_left, view_bottom, player, player_instance):
        self.bullet_list.update()
        for bullet in self.bullet_list:
            if arcade.check_for_collision(bullet, player):
                player_instance.change_health(-1)
                bullet.remove_from_sprite_lists()
            if player_instance.health == 0:
                quit()

class Map():
    def __init__(self):
        self.map = None
        self.wall_physics = None

    def load_map(self, map, player):
        self.map = map
        self.wall_list = arcade.tilemap.process_layer(self.map, 'Walls', 2)
        self.floor_list = arcade.tilemap.process_layer(self.map, 'Floor', 2)
        self.background_list = arcade.tilemap.process_layer(self.map, 'Ground', 2)

        self.wall_physics = arcade.PhysicsEngineSimple(player, self.wall_list)

    def draw_bottom(self):
        self.background_list.draw()
        self.floor_list.draw()

    def draw_walls(self):
        self.wall_list.draw()
    
    def update(self):
        self.wall_physics.update()

class Player():
    health = 3
    def __init__(self):
        self.player = arcade.Sprite("resources/images/player_circle.png", SCALING)
        self.player.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.player_triangle = arcade.Sprite("resources/images/player_arrow.png", SCALING)
        self.player_triangle.position = self.player.position

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.triangle_list = arcade.SpriteList()
        self.triangle_list.append(self.player_triangle)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        self.bullets = Bullets(50)
        self.shooting = False
        self.shot_ticker = 0


    def draw(self):
        self.bullets.draw()
        self.player_list.draw()
        self.triangle_list.draw()

    def start_movement(self, key):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True

    def stop_movement(self, key):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False

    def move_player(self):
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

    def update_triangle(self, mouse_x, mouse_y):
        self.player_triangle.position = self.player.position        # This line uncommented makes it wobbly. I kind of like it wobbly. Needs to be uncommented even if you also use the line below.  
        self.player_triangle.velocity = self.player.velocity        # This line uncommented makes it strict. 

        diff1 = mouse_y - self.player_triangle.center_y
        diff2 = mouse_x - self.player_triangle.center_x
        if diff2 == 0:
            diff2 = 1
        angle = (180 / math.pi) * (math.atan(diff1 / diff2)) - 90
        if diff2 < 0:
            self.player_triangle.angle = angle + 180
        else:
            self.player_triangle.angle = angle

        self.triangle_list.update()

    def shoot(self, mouse_x, mouse_y):
        if self.shot_ticker % 15 == 0:        
            self.bullets.create_bullet(mouse_x, mouse_y, self.player.center_x, self.player.center_y)
        self.shot_ticker += 1

    """def check_hit(self, bullet, bullet_list):
        hit = arcade.check_for_collision_with_list(self.player, self.bullet_list)
        if len(hit) > 0:
            if self.health > 0:
                self.health -= 1
            else:
                quit()"""

    def update(self, mouse_x, mouse_y, view_left, view_bottom, enemy_list, wall_list, player):
        self.move_player()
        self.update_triangle(mouse_x, mouse_y)

        if self.shooting == True:
            self.shoot(mouse_x, mouse_y)

        self.player_list.update()
        self.bullets.update(view_left, view_bottom, wall_list)
        self.bullets.update_hit(view_left, view_bottom, enemy_list)
    
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        self.player = Player()
        self.map = Map()


        # Sprite Lists Initialization
        # self.all_sprites = None
        self.enemy_list = None

        self.mouse_x = 1
        self.mouse_y = 1
        
        # Lets us use relative file paths
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.scrolling = Scrolling(self.player)
        self.map.load_map(arcade.tilemap.read_tmx('resources/maps/map0.tmx'), self.player.player)
        EnemySprite.creation(self)
        self.enemy_bullets = Bullets(5)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Drawing map lists
        self.map.draw_bottom()
        self.map.draw_walls()

        # Call draw() on all your sprite lists below
        self.enemy_list.draw()
        self.enemy_bullets.draw()
        self.player.draw()

        arcade.draw_text("Player Health: " + str(self.player.health), self.scrolling.view_left, self.scrolling.view_bottom + SCREEN_HEIGHT - 20, arcade.color.BLACK)

    def on_update(self, delta_time):
        self.map.update()       # Updates the player and wall physics. 

        EnemySprite.update_enemy(self)

        self.player.update(self.mouse_x, self.mouse_y, self.scrolling.view_left, self.scrolling.view_bottom, self.enemy_list, self.map.wall_list, self.player.player)
        self.enemy_bullets.update_hit_player(self.scrolling.view_left, self.scrolling.view_bottom, self.player.player, self.player)

        self.scrolling.scroll_left()
        self.scrolling.scroll_right()
        self.scrolling.scroll_up()
        self.scrolling.scroll_down()
        
    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        self.player.start_movement(key)

        if key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, key_modifiers):       
        self.player.stop_movement(key)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x + self.scrolling.view_left
        self.mouse_y = y + self.scrolling.view_bottom

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.player.shooting = True
        self.player.shot_ticker = 0
        self.mouse_x = x + self.scrolling.view_left
        self.mouse_y = y + self.scrolling.view_bottom

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.player.shooting = False

def main():
    """ Main method """
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main() 
