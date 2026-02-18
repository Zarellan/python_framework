from Libraries.GameObject import GameObject
from Libraries.MainCamera import MainCamera

class Scene:
    def __init__(self):
        self.initialized = False

    def start(self):
        """Called once when scene becomes active"""
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def destroy(self):

        from SceneManager.Persistent import Persistent
        try:
            print(Persistent.get_all())
            GameObject.destroy_all(skip=Persistent.get_all())
        except Exception as e:
            print("Error while destroying Sprites:", e)
        pass
