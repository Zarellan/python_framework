from Libraries.Libraries import *

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Pygame + OpenGL setup ---
pygame.init()
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF
)
pygame.display.set_caption("Box2D + OpenGL Test")
clock = pygame.time.Clock()

Windows.WIDTH = SCREEN_WIDTH
Windows.HEIGHT = SCREEN_HEIGHT
MainCamera.Set_Camera()
sprite_renderer = SpriteRendererGL(SCREEN_WIDTH, SCREEN_HEIGHT)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT)

# --- Box2D world ---
world = b2World(gravity=(0, 30))
WorldHandler.Set_World(world)
WorldHandler.world.contactListener = MyContactListener()

# --- Create ground ---
ground = GameObject("Ground")
ground.add_dynamic_body(world, position=(20, 20), size=(40, 20), bodyType=b2_staticBody)
ground.add_sprite("fish", camera)
ground.draw_colliders = True

# --- Create player ---
player = GameObject("Player")
player.add_dynamic_body(world, position=(5, 5), size=(2, 2), bodyType=b2_dynamicBody)
player.add_sprite("1", camera)
player.draw_colliders = True
player.dynamic_body.body.fixedRotation = True

# --- Create boxes ---
boxes = []
for i in range(5):
    box = GameObject("Box")
    box.add_dynamic_body(world, position=(20, 10 - (i * 2)), size=(1, 1),bodyType=b2_dynamicBody)
    box.add_sprite("background", camera)
    box.dynamic_body.include_colliders(["Ground", "Box", "Player"])
    boxes.append(box)

player.dynamic_body.include_colliders(["Ground", "Box"])
ground.dynamic_body.include_colliders(["Player", "Box"])

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000
    Deltatime.Set_Dt(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
    keys = pygame.key.get_pressed()
    speed_x = 5
    vel_x = 0
    if keys[pygame.K_LEFT]:
        vel_x = -speed_x
    elif keys[pygame.K_RIGHT]:
        vel_x = speed_x

    # Apply velocity via DynamicBody
    player.dynamic_body.set_velocity(vel_x, player.dynamic_body.body.linearVelocity.y)

    # --- Jump ---
    ray_start = player.dynamic_body.body.position
    ray_end = (ray_start[0], ray_start[1] + 2.1)
    callback = Raycast()
    world.RayCast(callback, ray_start, ray_end)

    if keys[pygame.K_UP] and callback.hit:
        player.dynamic_body.set_velocity(player.dynamic_body.body.linearVelocity.x, -10)

    # --- Step Box2D ---
    world.Step(dt, 6, 2)
    world.ClearForces()

    # --- Update GameObjects ---
    for obj in GameObject.all_objects:
        obj.update()  # DynamicBody → Transform → Sprite

    # --- Camera follow ---
    camera.follow(player.sprite, dt)

    # --- Render ---
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    sprite_renderer.draw([obj.sprite for obj in GameObject.all_objects if obj.sprite])
    GameObject.DrawDebugWorld(world, camera)

    pygame.display.flip()

# --- Cleanup ---
sprite_renderer.cleanup()
GameObject.destroy_all()
pygame.quit()