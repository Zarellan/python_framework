class Windows:
    
    WIDTH = 0
    HEIGHT = 0
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

    @classmethod
    def Set_size(cls, width, height):
        cls.WIDTH = width
        cls.HEIGHT = height
