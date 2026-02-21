from Libraries.Libraries import *

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Pygame + OpenGL setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Box2D + OpenGL Test")
clock = pygame.time.Clock()

Windows.WIDTH = 1280
Windows.HEIGHT = 720
MainCamera.Set_Camera()
sprite_renderer = SpriteRendererGL(SCREEN_WIDTH, SCREEN_HEIGHT)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT)

# --- Box2D world ---
world = b2World(gravity=(0, 30))
WorldHandler.Set_World(world)
WorldHandler.world.contactListener = MyContactListener()

# --- Create ground using GameObject ---
ground = GameObject("Ground")
ground.create_dynamic_sprite(
    world, camera,
    position=(20, 20),
    size=(40, 20),
    color=(0,1,0),
    texture_name="fish",
    bodyType=b2_staticBody
)
ground.draw_colliders = True
ground.sprite.set_size(40, 20)

# --- Create player using GameObject ---
player = GameObject("Player")
player.create_dynamic_sprite(
    world, camera,
    position=(5, 5),
    size=(2, 2),
    color=(1,0,0),
    texture_name="1",
    bodyType=b2_dynamicBody,
    friction=0
)
player.draw_colliders = True
player.sprite.body.fixedRotation = True


# --- Create some boxes using GameObject ---
boxes = []
for i in range(5):
    box = GameObject("Box")
    box.create_dynamic_sprite(
        world, camera,
        position=(20, 10 - (i * 2)),
        size=(1, 1),
        color=(1,0,0),
        bodyType=b2_dynamicBody,
        friction=0.3
    )
    box.sprite.include_colliders(["Ground", "Box", "Player"])
    boxes.append(box)

player.include_colliders(["Ground", "Box"])
ground.include_colliders(["Player", "Box"])

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000
    Deltatime.Set_Dt(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Camera follow ---
    # Pass the sprite (has rect.center) so camera centers correctly
    camera.follow(player.sprite, dt)

    # --- Input ---
    keys = pygame.key.get_pressed()
    speed_x = 5

    new_vel_x = 0
    if keys[pygame.K_LEFT]:
        new_vel_x = -speed_x
    elif keys[pygame.K_RIGHT]:
        new_vel_x = speed_x

    player.sprite.apply_linear(new_vel_x, player.sprite.body.linearVelocity.y)

    # --- Jump / raycast ---
    ray_start = player.sprite.body.position
    ray_end = (ray_start[0], ray_start[1] + 1.1)

    callback = Raycast()
    world.RayCast(callback, ray_start, ray_end)

    if keys[pygame.K_UP] and callback.hit:
        player.sprite.apply_linear(player.sprite.body.linearVelocity.x, -10)

    # --- Step Box2D ---
    world.Step(dt, 6, 2)
    world.ClearForces()

    # --- Draw ---
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    GameObject.UpdateAllDrawDynamic()
    # Draw all GameObjects
    sprite_renderer.draw([obj.sprite for obj in GameObject.all_objects if obj.sprite])

    # Use the same camera instance used for sprites so debug draw follows the world
    GameObject.DrawDebugWorld(world, camera)
    # Draw Box2D debug
    # GameObject.UpdateAllDraw(screen, MainCamera.camera)
    pygame.display.flip()

# --- Cleanup ---
sprite_renderer.cleanup()
GameObject.destroy_all()
pygame.quit()