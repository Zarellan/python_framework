from Libraries.camera import Camera
from Libraries.Windows import Windows

class MainCamera:

    camera = None
    def __init__(self):
        pass

    @classmethod
    def Set_Camera(cls):
        cls.camera = Camera(Windows.WIDTH,Windows.HEIGHT,Windows.HEIGHT)
