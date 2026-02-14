from Box2D import b2RayCastCallback

class Raycast(b2RayCastCallback):
    def __init__(self):
        super().__init__()
        self.hit = False
        self.point = None
        self.fixture = None
        self.normal = None
        self.fraction = 1.0
        self.name = ""

    def ReportFixture(self, fixture, point, normal, fraction):
        # Any other fixture is a hit
        if not self.hit or fraction < self.fraction:
            self.hit = True
            self.point = point
            self.normal = normal
            self.fixture = fixture
            self.fraction = fraction
            self.name = fixture.body.userData

        return 1  # continue to find closest hit
