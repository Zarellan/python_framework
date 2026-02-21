from Libraries.Libraries import *

class GameScene2(Scene):

    # --- Box2D world ---
    # WorldHandler.world.contactListener = MyContactListener()

    def start(self):

        pass
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        # MainCamera.camera.follow(GameObject.get_all_by_tag("pl")[0],Deltatime.dt)
        # if KeyPress.up:
        #     MainCamera.camera.follow(GameObject.get_all_by_tag("pl")[0],Deltatime.dt)
        # Put your Update(events) logic here
        pass

    def render(self):
        pass

    def destroy(self):
        pass
