import pygame
import sys
import tracemalloc
from Libraries.sprite import Sprite
from Libraries.spriteGL import SpriteGL
from Libraries.SpriteDynamicGL import SpriteDynamicGL
from Libraries.camera import Camera
from Libraries.SpriteRendererGL import SpriteRendererGL
from OpenGL.GL import *
from Libraries.Texture import Texture
import gc
from Libraries.Deltatime import Deltatime
from Libraries.Timer import Timer
from Libraries.Tween import Tween
from Box2D import b2World, b2PolygonShape
from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2_staticBody

# setup

force_garbage_collection = True # if you worried about unexpected memory leak, change it to true
PPM = 32.0  # pixels per meter

# --

tracemalloc.start()
print("Memory profiling started...")


# Count remaining SpriteGL instances

# from Libraries.utils import y_correction
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# initialize
pygame.init()
pygame.display.set_caption("test game")
# pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
#--


# box2D
world = b2World(gravity=(0, 9.8))
# --

def pixels_to_meters(px):
    return px / SpriteDynamicGL.PPM



def python_exit(events):
    global running
    for event in events:
        if event.type == pygame.QUIT:
            running = False

def collision(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)

class Keypress:
    left = False
    up = False
    down = False
    right = False

    def __init__(self):
        pass
    def update_key(self, events):
        condition = True
        for event in events:
            condition = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = condition
                elif event.key == pygame.K_RIGHT:
                    self.right = condition
                elif event.key == pygame.K_UP:
                    self.up = condition
                elif event.key == pygame.K_DOWN:
                    self.down = condition
            condition = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = condition
                elif event.key == pygame.K_RIGHT:
                    self.right = condition
                elif event.key == pygame.K_UP:
                    self.up = condition
                elif event.key == pygame.K_DOWN:
                    self.down = condition

def move_player(player, dx, dy, walls):
    player.x += dx
    for wall in walls:
        if player.rect.colliderect(wall.rect):
            if dx > 0:
                player.x = wall.rect.left - player.rect.width
            elif dx < 0:
                player.x = wall.rect.right

    player.y += dy
    for wall in walls:
        if player.rect.colliderect(wall.rect):
            if dy > 0:
                player.y = wall.rect.top - player.rect.height
            elif dy < 0:
                player.y = wall.rect.bottom

def resolve_collisions(player, walls):
    # X-axis
    for wall in walls:
        if player.rect.colliderect(wall.rect):
            if player.rect.centerx < wall.rect.centerx:
                # player is left of wall -> push left
                player.x = wall.rect.left - player.rect.width
            else:
                # player is right of wall -> push right
                player.x = wall.rect.right

    # Y-axis
    for wall in walls:
        if player.rect.colliderect(wall.rect):
            if player.rect.bottom <= wall.rect.centery:
                # player above wall -> stand on top
                player.y = wall.rect.top - player.rect.height
            else:
                # player below wall -> hit ceiling
                player.y = wall.rect.bottom



# def destroy_walls_right_of_player(player, y_margin=0, limit_x = 40):
#     """
#     Destroys all walls that are:
#     - Strictly to the right of the player
#     - Within the vertical range of player.y ± y_margin
#     """
#     player_right = player.x + player.width
#     for wall in Sprite.get_all_by_tag("wall"):
#         # Check if wall is right of player
#         if wall.x > player_right and (wall.x - player.x < limit_x):
#             # Check if wall is within vertical range
#             if wall.y >= (player.y - y_margin) and wall.y <= (player.y + player.height + y_margin):
#                 wall.destroy()


def check_ground(player, walls, margin=2):
    # Check a slightly taller rectangle under feet
    feet_rect = pygame.Rect(player.rect.left, player.rect.bottom, player.rect.width, margin)
    for wall in walls:
        if feet_rect.colliderect(wall.rect):
            return True
    return False

def check_ceil(player, walls, margin=1):
    # Small rectangle just above the player's head
    head_rect = pygame.Rect(player.rect.left, player.rect.top - margin, player.rect.width, margin)
    for wall in walls:
        if head_rect.colliderect(wall.rect):
            return True
    return False



def player_movement(key:Keypress):
    global dx
    global dy
    dx = 0
    if key_press.left:
        dx = -2 * speed_x * Deltatime.dt
    elif key_press.right:
        dx = 2 * speed_x * Deltatime.dt

    if check_ground(player, SpriteGL.get_all_by_tag("wall")):
        dy = 0
    elif check_ceil(player, SpriteGL.get_all_by_tag("wall")):
        dy = max(dy, 0.4)
    else:
        dy += gravity * Deltatime.dt

    if key_press.up and check_ground(player, SpriteGL.get_all_by_tag("wall")):
        dy = -jump_power



key_press = Keypress()

game_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,0,0],]

# display = pygame.Surface((600,400))

dx = 0
dy = 0
gravity = 30

sprite_renderer = SpriteRendererGL(SCREEN_WIDTH, SCREEN_HEIGHT)
camera = Camera(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_HEIGHT)

def create_map():
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == 1:
                SpriteGL("background", x * 32, y * 32, camera, "wall")
            x += 1
        y += 1
        x = 0

create_map()
dt = 0
speed_x = 100
jump_power = 7



def change_size(widtho, heighto):
    # Compute current visual width/height (floats) and center/bottom without using pygame.Rect
    cur_w = player.width * getattr(player, 'scale_x', 1.0)
    cur_h = player.height * getattr(player, 'scale_y', 1.0)
    if getattr(player, 'origin_centered', False):
        old_centerx = float(player.x)
        old_bottom = float(player.y + cur_h / 2)
    else:
        old_centerx = float(player.x + cur_w / 2)
        old_bottom = float(player.y + cur_h)

    # Apply size change to base dimensions
    player.width = widtho
    player.height = heighto

    # Treat this as changing the base/original size so scale stays consistent
    player.original_width = player.width
    player.original_height = player.height
    player.scale_x = 1.0
    player.scale_y = 1.0

    # New visual size
    new_w = player.width * player.scale_x
    new_h = player.height * player.scale_y

    # Reposition so center-x and bottom remain unchanged (use floats)
    if getattr(player, 'origin_centered', False):
        player.x = old_centerx
        player.y = old_bottom - new_h / 2
    else:
        player.x = old_centerx - new_w / 2
        player.y = old_bottom - new_h

def change_scale(x, y):
    # Compute current visual width/height (floats) and center/bottom without using pygame.Rect
    cur_w = player.width * getattr(player, 'scale_x', 1.0)
    cur_h = player.height * getattr(player, 'scale_y', 1.0)
    if getattr(player, 'origin_centered', False):
        old_centerx = float(player.x)
        old_bottom = float(player.y + cur_h / 2)
    else:
        old_centerx = float(player.x + cur_w / 2)
        old_bottom = float(player.y + cur_h)

    player.scale_x = x
    player.scale_y = y

    # Use floats internally
    new_width = player.original_width * player.scale_x
    new_height = player.original_height * player.scale_y

    # Reposition so center-x and bottom remain unchanged
    if getattr(player, 'origin_centered', False):
        player.x = old_centerx
        player.y = old_bottom - new_height / 2
    else:
        player.x = old_centerx - new_width / 2
        player.y = old_bottom - new_height

pressed = 0

def ui_sprite_rect(sprite, camera, screen_height):
    zoom = camera.zoom

    # Screen center
    cx = camera.width / 2
    cy = camera.height / 2

    # Sprite center (screen space)
    sx = sprite.x + sprite.width / 2
    sy = screen_height - sprite.y - sprite.height / 2

    # Apply centered zoom
    x = cx + (sx - cx) * zoom - (sprite.width * zoom) / 2
    y = cy + (sy - cy) * zoom - (sprite.height * zoom) / 2

    w = sprite.width * zoom
    h = sprite.height * zoom

    return pygame.Rect(x, y, w, h)


ui_camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT, True)
# heart_sprite = SpriteGL("1", 0, 0, ui_camera, tag="UI")
heart_sprite = SpriteGL("background", SCREEN_WIDTH / 2 , 200, ui_camera, tag="UI")
heart_sprite.width = 300

player = SpriteGL("1", 200, 200,camera,"player",1)
player.set_animation(["1","2"],0.3,True)


def Update(events):
    global pressed
    key_press.update_key(events)

    player_movement(key_press)
    move_player(player, dx, dy, SpriteGL.get_all_by_tag("wall"))
    
    if heart_sprite.MouseIsOverlap(ui_camera):
        print("Mouse over UI sprite")

    camera.follow(player, dt)
    resolve_collisions(player, SpriteGL.get_all_by_tag("wall"))

def Destroy():
    print("error occur")


frame_count = 0
stopit = False
xxx = 0
yyy = 0
def print_world():
    print("hello world")


# t = Tween.x(heart_sprite, heart_sprite.x + 600 - 32, 1.0, ease=Tween.ease_in_quad,on_complete=lambda: print("finished"))
# t = Tween.x(heart_sprite, 200, 1, ease=Tween.ease_out_quad,on_complete=lambda: print("finished"))
# Tween.camera_zoom(ui_camera, 1.05, 1, ease=Tween.ease_out_quad,on_complete=lambda: print("finished"))

try:
    while running:
        dt = clock.tick(60) / 1000
        Deltatime.Set_Dt(dt)
        events = pygame.event.get()
        python_exit(events)

        Update(events)

        world.Step(Deltatime.dt, 6, 2)
        world.ClearForces()
        Timer.UpdateAllTimers()
        SpriteGL.UpdateAllAnimation()
        Tween.UpdateAllTweens()
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        SpriteDynamicGL.UpdateAllDraw()
        sprite_renderer.draw(SpriteGL.all_sprites)
        pygame.display.flip()
        
        # Memory check every 60 frames (1 second at 60 FPS)
        frame_count += 1
        if frame_count % 60 == 0:
            current, peak = tracemalloc.get_traced_memory()
            print(f"Frame {frame_count}: Current memory: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB, Sprites: {len(SpriteGL.all_sprites)}")

except KeyboardInterrupt:
    Destroy()
    sprite_renderer.cleanup()  # Clean up shader, VAO, VBO
    SpriteGL.destroy_all()  # Clean up all sprite textures
except Exception as e:
    print("Exception:", e)
    import traceback
    traceback.print_exc()
    Destroy()
finally:
    print("Cleaning up OpenGL resources...")
    sprite_renderer.cleanup()  # Clean up shader, VAO, VBO
    SpriteGL.destroy_all()  # Clean up all sprite textures
    print("Remaining SpriteGL instances:", len(SpriteGL.all_sprites))
    current, peak = tracemalloc.get_traced_memory()
    print(f"Final memory: Current: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()
    if (force_garbage_collection):
        gc.collect()
    pygame.quit()
    sys.exit()