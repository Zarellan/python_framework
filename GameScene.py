from Libraries.Libraries import *
from GameScene2 import GameScene2

class GameScene(Scene):


    def start(self):

        self.game_map = [
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


        # self.player = SpriteGL("1", 200, 200,MainCamera.camera,"player",1)
        # self.player.set_animation(["1","2"],0.3,True)
        # self.tes = SpriteGL("1",200,200,MainCamera.camera,"pl")
        self.tes = GameObject("pl")
        # self.tes.add_sprite("1",MainCamera.camera)
        self.tes.add_component(SpriteGL, "1", MainCamera.camera)
        self.sprite_tes2 = self.tes.get_component(SpriteGL)
        self.sprite_tes2.set_animation(["1","2"],0.3,True)
        self.tes.set_position(200,200)
        # self.tes.add_component(DynamicBody, world=WorldHandler.world, position=(0,0), size=(40,20),bodyType=b2_dynamicBody)
        self.player = CharacterController("1",200,200)
        self.player.player.sprite.set_layer(2)
        Persistent.dont_destroy_on_load(self.tes)
        self.player.player.sprite.set_animation(["1","2"],0.3,True)
        self.create_map()
        
        self.uiCamera = Camera(Windows.WIDTH,Windows.HEIGHT,Windows.HEIGHT,True)
        self.UI_LOL = GameObject("play",True)
        self.UI_LOL.add_component(SpriteGL, "background", self.uiCamera, is_world=False)
        self.UI_LOL.transform.width = 100
        self.UI_LOL.transform.pivot = (0.5,0.5)
        self.UI_LOL.set_position(720 - 80,0)
        pass

    def create_map(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == 1:
                    wall = GameObject("wall")
                    wall.add_component(SpriteGL,"background", MainCamera.camera)
                    wall.transform.x = x * 32
                    wall.transform.y = y * 32
                x += 1
            y += 1
            x = 0
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        self.player.player_movement()
        MainCamera.camera.follow(self.player.player,Deltatime.dt)

        if (KeyPress.down):
            SceneManager.load_scene(GameScene2())

        pass

    def render(self):
        # Draw sprites here
        pass

    def destroy(self):
        super().destroy()
        pass