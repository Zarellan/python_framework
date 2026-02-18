from SceneManager.Scene import Scene
from Libraries.spriteGL import SpriteGL
from OpenGL.GL import *
from Libraries.camera import Camera
import pygame
from Libraries.Windows import Windows
from Libraries.Deltatime import Deltatime
from Libraries.MainCamera import MainCamera
from Libraries.CharacterController import CharacterController
from SceneManager.Persistent import Persistent
from Libraries.GameObject import GameObject
from Libraries.KeyPress import KeyPress

class GameScene2(Scene):


    def start(self):

        pass
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        # MainCamera.camera.follow(GameObject.get_all_by_tag("pl")[0],Deltatime.dt)
        if KeyPress.up:
            MainCamera.camera.follow(GameObject.get_all_by_tag("pl")[0],Deltatime.dt)
        # Put your Update(events) logic here
        pass

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # Draw sprites here
        pass

    def destroy(self):
        pass
