import pygame
from OpenGL.GL import *
from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2_staticBody
from Libraries.SpriteRendererGL import SpriteRendererGL
from Libraries.SpriteDynamicGL import SpriteDynamicGL
from Libraries.spriteGL import SpriteGL
from Libraries.camera import Camera
from Libraries.Deltatime import Deltatime
from Libraries.Raycast import Raycast
from Libraries.WorldHandler import WorldHandler
from Libraries.MyContactListener import MyContactListener
from Box2D import b2Filter
from Libraries.TagRegistry import TagRegistry
import numpy as np
import sys
import math

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Pygame + OpenGL setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Box2D + OpenGL Test")
clock = pygame.time.Clock()

sprite_renderer = SpriteRendererGL(SCREEN_WIDTH, SCREEN_HEIGHT)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT)

# --- Box2D world ---
world = b2World(gravity=(0, 30))

WorldHandler.Set_World(world)
# def pixels_to_meters(px):
#     return px / SpriteDynamicGL.PPM
WorldHandler.world.contactListener = MyContactListener()

GROUND = 0x0001
PLAYER = 0x0002
ENEMY  = 0x0004

ground_sprite = SpriteDynamicGL(
    world, camera,
    texture_name="fish", 
    position=(20, 20),
    size=(40, 20),   # width in meters, height in meters
    density=0,                     # static body can have 0 density
    friction=0.6,
    color=(0,1,0),
    tag="Ground",
    bodyType=b2_staticBody
)
ground_sprite.set_size(40,20)
ground_sprite.draw_colliders = True

# Create player sprite using the new class
player_sprite = SpriteDynamicGL(world, camera,
                                position=(5,5),
                                size=(2, 2),
                                color=(1,0,0),texture_name="1",friction=0, tag="Player")
player_sprite.draw_colliders = True


player_fixture = player_sprite.body.fixtures[0]
f = b2Filter()
f = player_fixture.filterData  # get existing filter
f.categoryBits = PLAYER         # this fixture *is* player
f.maskBits = GROUND             # only collides with ground
player_fixture.filterData = f
player_fixture.Refilter()

print(TagRegistry.get_category("Player"))
print(TagRegistry.get_category("Player"))

print(TagRegistry.get_category("Ground"))
print(TagRegistry.get_category("Ground"))


for i in range(5):
    sprite_2 = SpriteDynamicGL(world,camera, position=(20,10 - (i * 2)), size=(1, 1), color=(1,0,0),bodyType=b2_dynamicBody,friction=0.3,tag="Box")
    sprite_2.include_colliders(["Ground","Box"])


ground_sprite.include_colliders(["Player","Box"])
player_sprite.include_colliders(["Ground","Box"])

# --- Main loop ---


print(TagRegistry.get_category("Player"))

running = True
while running:
    dt = clock.tick(60) / 1000
    Deltatime.Set_Dt(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera.follow(player_sprite,dt)

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_UP]):
        camera.zoom += 0.01
    elif (keys[pygame.K_DOWN]):
        camera.zoom -= 0.09

    camera.zoom = 1

    # --- Input example: simple horizontal control ---
    force = 50
    speed = 5  # meters per second
    
    # Start by keeping current Y velocity (gravity works)
    new_vel_x = 0
    if keys[pygame.K_LEFT]:
        new_vel_x = -5
    elif keys[pygame.K_RIGHT]:
        new_vel_x = 5

    player_sprite.apply_linear(new_vel_x, player_sprite.body.linearVelocity.y)

    player_pos = player_sprite.body.position
    ray_start = (player_pos[0], player_pos[1])
    ray_end = (player_pos[0], player_pos[1] + 1.1)  # 5 meters down

    callback = Raycast()
    world.RayCast(callback, ray_start, ray_end)

    if keys[pygame.K_UP] and callback.hit:
        player_sprite.apply_linear(player_sprite.body.linearVelocity.x, -10)

    player_sprite.body.fixedRotation = True

    # --- Step Box2D world ---

    # --- Sync Sprite positions with Box2D bodies ---
    # for sprite in [ground_sprite, player_sprite]:
    #     sprite.update_draw()
    # ground_sprite.set_size(SpriteDynamicGL.get_fixture_size(ground_sprite.body.fixtures[0])[0],SpriteDynamicGL.get_fixture_size(ground_sprite.body.fixtures[0])[1]+0.05)
    world.Step(dt, 6, 2)
    world.ClearForces()
    
    # Cast ray downward from player center to check if grounded
    # Ray goes from player position down 5 meters (to ensure hitting ground)

    SpriteDynamicGL.UpdateAllDraw()
    # --- Render ---
    glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT)
    sprite_renderer.draw([ground_sprite, player_sprite])
    # ---- FORCE CLEAN DEBUG STATE ----
    # glUseProgram(0)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)

    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()

    # debug_draw_world(world)
    SpriteDynamicGL.DrawDebugWorld(world,camera)
    pygame.display.flip()

# --- Cleanup ---
sprite_renderer.cleanup()
SpriteGL.destroy_all()
pygame.quit()
sys.exit()
