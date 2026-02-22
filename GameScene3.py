from Libraries.Libraries import *

class GameScene3(Scene):
        
    def start(self):
        self.test = GameObject("hello")
        self.test.add_component(SpriteGL,"1",0,0,MainCamera.camera)
        self.test.set_position(400,200)

        Tween.x(self.test,300,0.3)
        pass
