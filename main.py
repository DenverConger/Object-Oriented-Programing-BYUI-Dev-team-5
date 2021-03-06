"""
This game was created by
Denver Conger   con19037@byui.edu
Rhys Benson Bensonrhys702@gmail.com
Kyler Mellor mel17006@byui.edu
Trevor Lamoglia trevorlamoglia21@gmail.com
"""
import arcade
import os
import math

SCREEN_WIDTH = 1344
SCREEN_HEIGHT = 704
SCREEN_TITLE = "The Dungeon"
SCALING = 0.5
SCALING_MAP = 2
TILE_SIZE = 32
MAP_WIDTH = (TILE_SIZE * SCALING_MAP * 100) - 1
MAP_HEIGHT = (TILE_SIZE * SCALING_MAP * 100) - 1
MAP_NAME = 'resources/maps/level0.tmx'

PLAYER_SPEED = 7
ENEMY_SPEED = 1

class Scrolling():
    def __init__(self, player):
        self.LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 4
        self.RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 4
        self.BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT / 4
        self.TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT / 4

        self.player = player
        self.view_bottom = self.player.player.center_y
        self.view_left = self.player.player.center_x
        
        self.changed = False

    def update(self):
        # Scroll left
        left_boundary = self.view_left + self.LEFT_VIEWPORT_MARGIN
        if self.player.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.player.left
            self.changed = True
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - self.RIGHT_VIEWPORT_MARGIN
        if self.player.player.right > right_boundary:
            self.view_left += self.player.player.right - right_boundary
            self.changed = True
        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - self.TOP_VIEWPORT_MARGIN
        if self.player.player.top > top_boundary:
            self.view_bottom += self.player.player.top - top_boundary
            self.changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + self.BOTTOM_VIEWPORT_MARGIN
        if self.player.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.player.bottom
            self.changed = True

        if self.changed:
            # Only scroll to integers. Otherwise we end up with pixels that don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        
        # If the margins were changed to center the viewport, this will change the viewport back. 
        if self.LEFT_VIEWPORT_MARGIN == SCREEN_WIDTH / 2:
            self.change_viewport_margins(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4)

    def change_viewport_margins(self, width_margin, height_margin):
        self.LEFT_VIEWPORT_MARGIN = width_margin
        self.RIGHT_VIEWPORT_MARGIN = width_margin
        self.BOTTOM_VIEWPORT_MARGIN = height_margin
        self.TOP_VIEWPORT_MARGIN = height_margin

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
                    enemy.center_y += min(ENEMY_SPEED, player.center_y - enemy.center_y)
                elif enemy.center_y > player.center_y:
                    enemy.center_y -= min(ENEMY_SPEED, enemy.center_y - player.center_y)
                if enemy.center_x < player.center_x:
                    enemy.center_x += min(ENEMY_SPEED, player.center_x - enemy.center_x)
                elif enemy.center_x > player.center_x:
                    enemy.center_x -= min(ENEMY_SPEED, enemy.center_x - player.center_x)

    def attack(self, player):
        for enemy in self.enemy_list:
            if enemy.player_detected:
                if enemy.shot_timer % 60 == 0:
                    self.enemy_bullets.create_bullet(player.center_x, player.center_y, enemy.center_x, enemy.center_y)
                enemy.shot_timer += 1
                    
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
        self.enemy_layer_list = arcade.tilemap.process_layer(arcade.tilemap.read_tmx(MAP_NAME), 'Enemies', SCALING_MAP)
        for enemy in self.enemy_layer_list:
            enemy_sprite = EnemySprite("resources/images/enemy_square.png", SCALING * .5)
            enemy_sprite.center_x = enemy.center_x
            enemy_sprite.center_y = enemy.center_y
            enemy_sprite.remove_from_sprite_lists()
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

            # Remove bullets when they leave the screen.
            if bullet.center_x < view_left or bullet.center_x > view_left + SCREEN_WIDTH or bullet.center_y < view_bottom or bullet.center_y > view_bottom + SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

            # Remove bullets when they hit a wall.
            if len(arcade.check_for_collision_with_list(bullet, wall_list)) > 0:
                bullet.remove_from_sprite_lists()

    def update_hit(self, view_left, view_bottom, enemy_list):
        self.bullet_list.update()
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
        self.lock_physics = None

    def load_map(self, map, player):
        self.map = map
        self.player = player
        self.top_list = arcade.tilemap.process_layer(self.map, 'Top', SCALING_MAP, use_spatial_hash = True)
        self.lock_list = arcade.tilemap.process_layer(self.map, 'Locks', SCALING_MAP, use_spatial_hash = True)
        self.wall_list = arcade.tilemap.process_layer(self.map, 'Walls', SCALING_MAP, use_spatial_hash = True)
        self.key_list = arcade.tilemap.process_layer(self.map, 'Keys', SCALING_MAP)
        self.floor_list = arcade.tilemap.process_layer(self.map, 'Floor', SCALING_MAP, use_spatial_hash = True)
        self.background_list = arcade.tilemap.process_layer(self.map, 'Ground', SCALING_MAP, use_spatial_hash = True)

        self.maze_layer = arcade.tilemap.process_layer(self.map, 'Maze_Walls', SCALING_MAP, use_spatial_hash= False)
        self.maze_layer_transparent = arcade.SpriteList()
        for maze_block in self.maze_layer:
            transparency = arcade.Sprite("resources/images/Transparent Tile.png", SCALING_MAP, hit_box_algorithm= 'None')
            transparency.center_x = maze_block.center_x
            transparency.center_y = maze_block.center_y
            transparency.remove_from_sprite_lists()
            self.maze_layer_transparent.append(transparency)

        self.wall_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.maze_physics = arcade.PhysicsEngineSimple(self.player, self.maze_layer_transparent)

    def collide_with_lock(self, item_list):
        # I had to manually do collision physics because arcade doesn't allow you to use a check_for_collision statement and physics
        # for the same object(s).
        for lock in self.lock_list:
            if arcade.check_for_collision(self.player, lock) and len(item_list) == 0 and self.player.top >= lock.bottom and lock.top > self.player.top:
                self.player.top = lock.bottom
            if arcade.check_for_collision(self.player, lock) and len(item_list) == 0:
                self.player.bottom = lock.top

    def draw_bottom(self):
        self.background_list.draw()
        self.floor_list.draw()

    def draw_walls(self):
        self.wall_list.draw()
        self.lock_list.draw()
        self.maze_layer_transparent.draw()
        # self.maze_layer_transparent.draw_hit_boxes(color= (255, 0, 0))

    def draw_top(self):
        self.key_list.draw()
        self.top_list.draw()
    
    def update(self, item_list):
        self.wall_physics.update()
        self.maze_physics.update()
        self.collide_with_lock(item_list)

class Player():   
    def __init__(self):
        self.player = arcade.Sprite("resources/images/player_circle.png", SCALING)
        self.player.position = (3200, 3200)

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

        self.health = 3

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
            self.player.change_y = PLAYER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -PLAYER_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_SPEED

    def update_triangle(self, mouse_x, mouse_y):
        self.player_triangle.position = self.player.position        # This line uncommented makes it wobbly.
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

    def change_health(self, change):
        self.health += change

    def update(self, mouse_x, mouse_y, view_left, view_bottom, enemy_list, wall_list, player):
        self.move_player()
        self.update_triangle(mouse_x, mouse_y)

        if self.shooting == True:
            self.shoot(mouse_x, mouse_y)

        self.player_list.update()
        self.bullets.update(view_left, view_bottom, wall_list)
        self.bullets.update_hit(view_left, view_bottom, enemy_list)
    
class Inventory():
    def __init__(self, map, player):
        self.item_list = []
        self.map = map
        self.player = player

    def add_item(self, item):
        self.item_list.append(item)

    def key_collision(self):
        for key in self.map.key_list:
            if arcade.check_for_collision(key, self.player.player):
                self.add_item(key)
                

        for lock in self.map.lock_list:
            if arcade.check_for_collision(lock, self.player.player) and len(self.item_list) > 0:
                self.item_list[len(self.item_list) - 1].kill()
                self.item_list.remove(self.item_list[len(self.item_list) - 1])
                
                lock.kill()

    def update(self, view_bottom, view_left, player):
        self.key_collision()
        for i, item in enumerate(self.item_list):
            if len(self.item_list) > 0:
                item.center_y = view_bottom + 32
                item.center_x = view_left + (i * 32 * SCALING_MAP) + 32

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.center_window()
        arcade.set_background_color(arcade.color.WHITE)

        self.player = Player()
        self.map = Map()
        self.inventory = Inventory(self.map, self.player)


        # Sprite Lists Initialization
        self.enemy_list = None

        self.mouse_x = 1
        self.mouse_y = 1
        
        # Lets us use relative file paths
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.map.load_map(arcade.tilemap.read_tmx(MAP_NAME), self.player.player)
        
        self.enemy_list = arcade.SpriteList()
        EnemySprite.creation(self)
        self.enemy_bullets = Bullets(5)

        # Brings player to the center and centers the viewport. Viewport is changed to normal in scrolling.update()
        self.player.player.position = (MAP_WIDTH / 2, MAP_HEIGHT / 2)
        self.scrolling = Scrolling(self.player)
        self.scrolling.change_viewport_margins(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on layers to be below the player here. 
        self.map.draw_bottom()
        self.map.draw_walls()

        # Call draw() on all your sprite lists below.
        self.enemy_list.draw()
        self.enemy_bullets.draw()
        self.player.draw()

        arcade.draw_text("Player Health: " + str(self.player.health), self.scrolling.view_left, self.scrolling.view_bottom + SCREEN_HEIGHT - 20, arcade.color.BLACK)
        
        # Call draw() on layers to be on top of the player here.
        self.map.draw_top()

    def on_update(self, delta_time):
        self.map.update(self.inventory.item_list)       # Updates the player/wall and player/lock physics. 
        self.inventory.update(self.scrolling.view_bottom, self.scrolling.view_left, self.player.player)

        EnemySprite.update_enemy(self)

        self.player.update(self.mouse_x, self.mouse_y, self.scrolling.view_left, self.scrolling.view_bottom, self.enemy_list, self.map.wall_list, self.player.player)
        self.enemy_bullets.update_hit_player(self.scrolling.view_left, self.scrolling.view_bottom, self.player.player, self.player)

        self.scrolling.update()

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