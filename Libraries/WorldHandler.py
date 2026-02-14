class WorldHandler:
    
    world = None
    def __init__(self):
        self.world = None

    @classmethod
    def Set_World(self, world):
        self.world = world