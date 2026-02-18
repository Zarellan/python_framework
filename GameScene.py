from SceneManager.Scene import Scene
from SceneManager.SceneManager import SceneManager

from Libraries.spriteGL import SpriteGL
from OpenGL.GL import *
from Libraries.camera import Camera
import pygame
from Libraries.Windows import Windows
from Libraries.Deltatime import Deltatime
from Libraries.MainCamera import MainCamera
from Libraries.CharacterController import CharacterController
from SceneManager.Persistent import Persistent
from Libraries.KeyPress import KeyPress
from GameScene2 import GameScene2
from Libraries.GameObject import GameObject

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
        self.tes.create_sprite("1",200,200,MainCamera.camera)
        self.player = CharacterController("1",200,200)
        self.player.player.sprite.set_animation(["1","2"],0.3,True)
        Persistent.dont_destroy_on_load(self.tes)
        self.create_map()

        # Create player, map, world here
        # create_map()
        # self.player = ...
        # self.camera = ...
        pass
    def create_map(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == 1:
                    wall = GameObject("wall")
                    wall.create_sprite("background", x * 32, y * 32, MainCamera.camera)
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
        glClear(GL_COLOR_BUFFER_BIT)
        # Draw sprites here
        pass

    def destroy(self):
        print("GameScene destroyed")
        super().destroy()
