from Libraries.Libraries import *

class GameScenePhysics(Scene):

    def start(self):
        # --- Screen & Camera Setup ---

        MainCamera.camera.set_zoom(1)
        self.uiCamera = Camera(Windows.VIRTUALWIDTH,Windows.VIRTUALHEIGHT,Windows.VIRTUALHEIGHT,True)
        self.UI_LOL = GameObject("play",True)
        self.UI_LOL.add_component(SpriteGL, "background", self.uiCamera, is_world=False)
        self.UI_LOL.transform.width = 100
        self.UI_LOL.transform.pivot = (0.5,0.5)
        self.UI_LOL.set_position(-600,0)
        self.UI_LOL.get_component(SpriteGL).set_layer(7)

        # --- Box2D World ---
        self.world = b2World(gravity=(0, 30))
        WorldHandler.Set_World(self.world)
        self.world.contactListener = MyContactListener()

        # --- Ground ---
        self.ground = GameObject("Ground")
        self.ground.add_component(DynamicBody, self.world, position=(20, 20), size=(40, 20), bodyType=b2_staticBody)
        self.ground.add_component(SpriteGL, "fish", MainCamera.camera)
        self.ground.draw_colliders = True
    
        # --- Player ---
        self.player = GameObject("Player")
        self.player.add_component(DynamicBody, self.world, position=(5, 5), size=(2, 2), bodyType=b2_dynamicBody)
        self.player.add_component(SpriteGL, "1", MainCamera.camera)
        self.player.draw_colliders = True
        self.player.dynamic_body.body.fixedRotation = True

        # --- Boxes ---
        self.boxes = []
        for i in range(5):
            box = GameObject("Box")
            box.add_component(DynamicBody, self.world, position=(0,0), size=(1,1), bodyType=b2_dynamicBody)
            box.add_component(SpriteGL, "background", MainCamera.camera)
            box.set_position(20, (10 - i*2))
            box.dynamic_body.include_colliders(["Ground", "Box", "Player"])
            self.boxes.append(box)

        # Include colliders
        self.player.dynamic_body.include_colliders(["Ground", "Box"])
        self.ground.dynamic_body.include_colliders(["Player", "Box"])

        # --- Clock ---
        self.clock = pygame.time.Clock()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        # --- Delta time ---
        dt = self.clock.tick(60) / 1000
        Deltatime.Set_Dt(dt)

        # --- Input ---
        keys = pygame.key.get_pressed()
        speed_x = 5
        vel_x = 0
        if keys[pygame.K_LEFT]:
            vel_x = -speed_x
        elif keys[pygame.K_RIGHT]:
            vel_x = speed_x

        # Apply velocity via DynamicBody
        self.player.dynamic_body.set_velocity(vel_x, self.player.dynamic_body.body.linearVelocity.y)

        # --- Jump ---
        ray_start = self.player.dynamic_body.body.position
        ray_end = (ray_start[0], ray_start[1] + 1.1)
        callback = Raycast()
        self.world.RayCast(callback, ray_start, ray_end)
        if keys[pygame.K_UP] and callback.hit:
            self.player.dynamic_body.set_velocity(self.player.dynamic_body.body.linearVelocity.x, -10)

        # --- Camera follow ---
        MainCamera.camera.follow(self.player.sprite, dt)


        pygame.display.flip()

    def destroy(self):
        pass
