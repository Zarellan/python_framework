from Libraries.Libraries import *
from GameScene import GameScene

# setup

force_garbage_collection = True # if you worried about unexpected memory leak, change it to true
PPM = 32.0  # pixels per meter
TRACEMALLOC = False
# --

if (TRACEMALLOC):
    tracemalloc.start()
    print("Memory profiling started...")


# Count remaining SpriteGL instances

# from Libraries.utils import y_correction

Windows(1280, 720)
Windows.Set_size(1280, 720)
MainCamera()
MainCamera.Set_Camera()
SCREEN_WIDTH = Windows.WIDTH
SCREEN_HEIGHT = Windows.HEIGHT

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

WorldHandler.Set_World(world)
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

dt = 0
speed_x = 100
jump_power = 7

pressed = 0

ui_camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT, True)
# heart_sprite = SpriteGL("1", 0, 0, ui_camera, tag="UI")
# heart_sprite = SpriteGL("background", SCREEN_WIDTH / 2 , 200, ui_camera, tag="UI")
# heart_sprite.width = 300



def Update(events):
    global pressed




def Destroy():
    print("error occur")


frame_count = 0
stopit = False
xxx = 0
yyy = 0
def print_world():
    print("hello world")


def shutdown_engine():
    print("Shutting down engine...")

    SceneManager.destroy_immediate()
    sprite_renderer.cleanup()

    if (TRACEMALLOC):
        current, peak = tracemalloc.get_traced_memory()
        #print(f"Final memory: Current: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB")
        print(f"Frame {frame_count}: Current memory: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB, Sprites: {len(GameObject.all_objects)}")
        tracemalloc.stop()

    if force_garbage_collection:
        gc.collect()

    pygame.quit()
    sys.exit()

# t = Tween.x(heart_sprite, heart_sprite.x + 600 - 32, 1.0, ease=Tween.ease_in_quad,on_complete=lambda: print("finished"))
# t = Tween.x(heart_sprite, 200, 1, ease=Tween.ease_out_quad,on_complete=lambda: print("finished"))
# Tween.camera_zoom(ui_camera, 1.05, 1, ease=Tween.ease_out_quad,on_complete=lambda: print("finished"))
SceneManager.load_scene(GameScene())

try:
    while running:
        dt = clock.tick(60) / 1000
        Deltatime.Set_Dt(dt)
        events = pygame.event.get()
        python_exit(events)

        KeyPress.update_key(events)

        SceneManager.update()

        # Update(events)

        world.Step(Deltatime.dt, 6, 2)
        world.ClearForces()
        Timer.UpdateAllTimers()
        GameObject.UpdateAllObjects()
        Tween.UpdateAllTweens()
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        # SpriteDynamicGL.UpdateAllDraw()
        sprite_renderer.draw(GameObject.all_objects)
        pygame.display.flip()
        
        # Memory check every 60 frames (1 second at 60 FPS)
        if (TRACEMALLOC):
            frame_count += 1
            if frame_count % 60 == 0:
                current, peak = tracemalloc.get_traced_memory()
                print(f"Frame {frame_count}: Current memory: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB, Sprites: {len(GameObject.all_objects)}")

except KeyboardInterrupt:
    shutdown_engine()
except Exception as e:
    print("Exception:", e)
    import traceback
    traceback.print_exc()
    shutdown_engine()
finally:
    shutdown_engine()