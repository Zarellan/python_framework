from Box2D import b2ContactListener
from Libraries.WorldHandler import WorldHandler

class MyContactListener(b2ContactListener):
    def BeginContact(self, contact):
        a = contact.fixtureA.body.userData
        b = contact.fixtureB.body.userData

        # ignore collision between player and a specific "ghost" object
        if a == "player" and b == "ghost":
            contact.enabled = False  # disables this contact for this step
        elif b == "player" and a == "ghost":
            contact.enabled = False
