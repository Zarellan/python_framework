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
        self.tes.add_sprite("1",MainCamera.camera)
        self.tes.set_position(200,200)
        self.player = CharacterController("1",200,200)
        self.player.player.sprite.set_layer(2)
        Persistent.dont_destroy_on_load(self.tes)
        self.player.player.sprite.set_animation(["1","2"],0.3,True)
        self.create_map()

        # for i in range(50):
        #     fish = GameObject("wal1l")
        #     fish.add_sprite("fish", 200, 1 * i, MainCamera.camera)
        #     fish.transform.x = 200

        # Create player, map, world here
        # create_map()
        # self.player = ...
        # self.camera = ...
        pass
        # for i in range(30):
        #     wall = GameObject("walld")
        #     wall.create_sprite("fish", 300, 0, MainCamera.camera)

    def create_map(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == 1:
                    wall = GameObject("wall")
                    wall.add_sprite("background", MainCamera.camera)
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


        # Put your Update(events) logic here
        pass

    def render(self):
        # Draw sprites here
        pass

    def destroy(self):
        super().destroy()
        pass