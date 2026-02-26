class Windows:
    
    WIDTH = 0
    HEIGHT = 0
    VIRTUALWIDTH = 0
    VIRTUALHEIGHT = 0
    def __init__(cls, width, height):
        cls.WIDTH = width
        cls.HEIGHT = height
        cls.VIRTUALWIDTH = width
        cls.VIRTUALHEIGHT = height

    @classmethod
    def Set_size(cls, width, height):
        cls.WIDTH = width
        cls.HEIGHT = height
        cls.VIRTUALWIDTH = width
        cls.VIRTUALHEIGHT = height

    @classmethod
    def Set_size_virtual(cls, width, height):
        cls.VIRTUALWIDTH = width
        cls.VIRTUALHEIGHT = height

