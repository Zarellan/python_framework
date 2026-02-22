from Box2D import b2Filter
from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2_staticBody
from Libraries.TagRegistry import TagRegistry

class DynamicBody:
    def __init__(self, gameobject, world, **kwargs):
        self.gameobject = gameobject
        # Store the physics size for sprite scaling
        self.physics_size = kwargs.get('size', (1, 1))
        # create the Box2D body
        self.body = self._create_body(world, **kwargs)

    def _create_body(self, world, position=(0,0), size=(1,1), bodyType=None, density=1.0, friction=0.3):
        # Box2D expects half-widths for the box parameter
        half_width = size[0] / 2.0
        half_height = size[1] / 2.0
        
        body_def = world.CreateDynamicBody if bodyType == b2_dynamicBody else world.CreateStaticBody
        body = body_def(
            position=position,
            angle=0
        )
        box = body.CreatePolygonFixture(box=(half_width, half_height), density=density, friction=friction)
        return body

    def update_transform(self):
        # physics → transform
        self.gameobject.transform.x = self.body.position[0] * self.gameobject.PPU
        self.gameobject.transform.y = self.body.position[1] * self.gameobject.PPU
        self.gameobject.transform.rotation = self.body.angle
        
        # Calculate sprite scaling to match physics body size
        if self.gameobject.sprite:
            # Physical world size in pixels
            physics_width_px = self.physics_size[0] * self.gameobject.PPU
            physics_height_px = self.physics_size[1] * self.gameobject.PPU
            
            # Scale sprite to match physics dimensions
            self.gameobject.sprite.scale_x = physics_width_px / self.gameobject.sprite.original_width
            self.gameobject.sprite.scale_y = physics_height_px / self.gameobject.sprite.original_height

    def set_velocity(self, vx, vy):
        self.body.linearVelocity = (vx, vy)

    def apply_force(self, fx, fy):
        self.body.ApplyForceToCenter((fx, fy), True)

    def apply_impulse(self, ix, iy):
        self.body.ApplyLinearImpulse((ix, iy), self.body.worldCenter, True)

    # --- Forward colliders methods from SpriteDynamicGL ---
    def include_colliders(self, mask_tags):
        fixture = self.body.fixtures[0]
        f = fixture.filterData
        f.categoryBits = TagRegistry.get_category(self.gameobject.tag)
        mask = 0
        for tag in mask_tags:
            if tag in TagRegistry._tag_map:
                mask |= TagRegistry.get_category(tag)
            else:
                raise KeyError(f"**{tag}** doesn't exist in the tag (did you register it early?)")
        f.maskBits = mask
        fixture.filterData = f
        fixture.Refilter()

    def exclude_colliders(self, mask_tags):
        fixture = self.body.fixtures[0]
        f = fixture.filterData
        f.categoryBits = TagRegistry.get_category(self.gameobject.tag)
        mask = 0
        for tag in mask_tags:
            if tag in TagRegistry._tag_map:
                mask |= TagRegistry.get_category(tag)
            else:
                raise KeyError(f"**{tag}** doesn't exist in the tag")
        f.maskBits = 0xFFFF & ~mask
        fixture.filterData = f
        fixture.Refilter()