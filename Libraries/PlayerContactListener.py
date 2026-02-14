from Box2D import b2ContactListener

class PlayerContactListener(b2ContactListener):
    def __init__(self, body):
        super().__init__()
        self.player_body = body
        self.ground_contacts = 0
        self.on_ground = False

    def BeginContact(self, contact):
        if contact.fixtureA.userData == "foot" or contact.fixtureB.userData == "foot":
            self.ground_contacts += 1
            self.on_ground = True

    def EndContact(self, contact):
        if contact.fixtureA.userData == "foot" or contact.fixtureB.userData == "foot":
            self.ground_contacts -= 1
            self.on_ground = self.ground_contacts > 0
