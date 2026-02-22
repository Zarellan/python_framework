from Libraries.spriteGL import SpriteGL
from Libraries.SpriteDynamicGL import SpriteDynamicGL
from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2_staticBody
from Box2D import b2Filter
from Libraries.TagRegistry import TagRegistry
from OpenGL.GL import *
from Libraries.Transform import Transform
from Libraries.DynamicBody import DynamicBody

import math

class GameObject:
    all_objects = []
    all_tags = []
    PPU = 32
    def __init__(self, tag):
        self.sprite = None
        self.tag = tag
        self.transform = Transform()
        # per-object flag that forwards to the sprite when present
        self._draw_colliders = False
        self.__class__.all_objects.append(self)

        if self.tag not in GameObject.all_tags:
            TagRegistry.ensure_tag(self.tag)
            GameObject.all_tags.append(self.tag)


    def add_sprite(self, image_path, camera):
        self.sprite = SpriteGL(image_path, self.transform.x, self.transform.y, camera)
        return self.sprite

    def create_sprite(self,imagePath,x,y,camera):
        self.sprite = SpriteGL(imagePath,x,y,camera)
        pass

    def add_dynamic_body(self, world, **kwargs):
        self.dynamic_body = DynamicBody(self, world, **kwargs)
        return self.dynamic_body

    def create_dynamic_sprite(self, world, camera, position=(5,5), size=(1,1),
                 density=1.0, friction=0.3, texture_name="background", color=(1,0,0), bodyType = b2_dynamicBody, ppu=None):
        self.sprite = SpriteDynamicGL(world, camera, position=position, size=size,
                 density=density, friction=friction, texture_name=texture_name, color=color, tag = self.tag, bodyType = bodyType, ppu=ppu)
        # propagate draw_colliders flag to the sprite if it was set on the GameObject
        if getattr(self, '_draw_colliders', False) and hasattr(self.sprite, 'draw_colliders'):
            self.sprite.draw_colliders = True
        pass
    def destroy(self):
        """Destroy this GameObject and its sprite."""
        # Destroy sprite safely
        if self.sprite:
            self.sprite.destroy()
            self.sprite = None

        if self in self.__class__.all_objects:
            self.__class__.all_objects.remove(self)

    def apply_linear(self, x, y):
        self.body.linearVelocity = (x, y)

    def apply_linear_Impulse(self, x, y):
        self.body.ApplyLinearImpulse((x,y),self.body.worldCenter, False)

    def apply_force(self, fx, fy):
        self.body.ApplyForceToCenter((fx, fy), True)

    def apply_impulse(self, ix, iy):
        self.body.ApplyLinearImpulse((ix, iy), self.body.worldCenter, True)

    @classmethod
    def destroy_all(cls, skip=None):
        """
        Destroy all non-persistent objects.
        skip: optional list of objects to preserve
        """
        if skip is None:
            skip = []

        # Make a copy to avoid modifying list while iterating
        for obj in cls.all_objects[:]:
            if obj in skip:
                continue
            obj.destroy()

    @property
    def draw_colliders(self):
        """Property to get/set collider-draw flag on the GameObject and its sprite."""
        return getattr(self, '_draw_colliders', False)

    @draw_colliders.setter
    def draw_colliders(self, value):
        self._draw_colliders = bool(value)
        # If sprite exists and supports the flag, sync it immediately
        if self.sprite is not None and hasattr(self.sprite, 'draw_colliders'):
            self.sprite.draw_colliders = bool(value)

    # ✅ Class method to get all sprites by tag
    @classmethod
    def get_all_by_tag(cls, tag_name):
        return [obj for obj in cls.all_objects if obj.tag == tag_name]
    
    def update_draw_dynamic(self):
        if self.sprite and isinstance(self.sprite, SpriteDynamicGL):
            # center the sprite on the physics body
            self.transform.x = self.sprite.body.position[0] * self.PPU
            self.transform.y = self.sprite.body.position[1] * self.PPU
            self.transform.rotation = self.sprite.body.angle

            # sprite mirrors the transform
            self.sprite.x = self.transform.x - self.sprite.width / 2
            self.sprite.y = self.transform.y - self.sprite.height / 2
            self.sprite.rotation = self.transform.rotation    # Class method to draw all sprites
        pass

    def set_position(self,x,y):
        self.transform.x = x
        self.transform.y = y

    def update(self):
        # 1️⃣ Physics → Transform
        if self.dynamic_body:
            self.dynamic_body.update_transform()

        # 2️⃣ Transform → Sprite
        if self.sprite:
            self.sprite.x = self.transform.x - self.sprite.width / 2
            self.sprite.y = self.transform.y - self.sprite.height / 2
            self.sprite.rotation = self.transform.rotation

        # 3️⃣ Play animation if applicable
        if self.sprite and getattr(self.sprite, "animation_frames", None):
            self.sprite.play_animation()

    @classmethod
    def UpdateAllDraw(cls, display, camera):
        for i in range(4):
            for obj in cls.all_objects:
                if (obj.sprite.layer_index == i):
                    obj.sprite.update_draw(display, camera)
    def update(self):
        # Physics → Transform
        if hasattr(self, "dynamic_body") and self.dynamic_body:
            self.dynamic_body.update_transform()

        # Transform → Sprite
        if self.sprite:
            if isinstance(self.sprite, SpriteDynamicGL):
                self.update_draw_dynamic()
            else:  # SpriteGL
                self.update_draw_static()

        # Play animation if applicable
        if self.sprite and getattr(self.sprite, "animation_frames", None):
            self.sprite.play_animation()

    def update_draw_static(self):
        if self.sprite and isinstance(self.sprite, SpriteGL):
            # Center sprite on transform
            self.sprite.x = self.transform.x - self.sprite.width / 2
            self.sprite.y = self.transform.y - self.sprite.height / 2
            self.sprite.rotation = self.transform.rotation
    @classmethod
    def UpdateAllDrawDynamic(cls):
        for obj in cls.all_objects:
            obj.update_draw_dynamic()
        pass
    
    @classmethod
    def UpdateAllObjects(cls):
        for obj in cls.all_objects:
            obj.update()
        pass
    @classmethod
    def UpdateAllAnimation(cls):
        for obj in cls.all_objects:
            if (obj.sprite.animation_frames):
                obj.sprite.play_animation()

    @property
    def x(self):
        return self.sprite.x if self.sprite else None

    @property
    def y(self):
        return self.sprite.y if self.sprite else None
    
    def include_colliders(self, mask_tags):
        # Only dynamic sprites have Box2D bodies
        if not isinstance(self.sprite, SpriteDynamicGL):
            print(f"GameObject {self.tag} has no physics body to set colliders")
            return

        fixture = self.sprite.body.fixtures[0]
        f = fixture.filterData

        # Set this object's category
        f.categoryBits = TagRegistry.get_category(self.tag)

        # Build mask bits from given tags
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
        # Only dynamic sprites have Box2D bodies
        if not isinstance(self.sprite, SpriteDynamicGL):
            print(f"GameObject {self.tag} has no physics body to set colliders")
            return

        fixture = self.sprite.body.fixtures[0]
        f = fixture.filterData
        f.categoryBits = TagRegistry.get_category(self.tag)

        mask = 0
        for tag in mask_tags:
            if tag in TagRegistry._tag_map:
                mask |= TagRegistry.get_category(tag)
            else:
                raise KeyError(f"**{tag}** doesn't exist in the tag")

        f.maskBits = 0xFFFF & ~mask
        fixture.filterData = f
        fixture.Refilter()

    @staticmethod
    def draw_polygon(sprite, body, polygon, camera):
        """Draw a single polygon fixture (immediate-mode)."""
        if (not sprite.draw_colliders):
            return
        glBegin(GL_LINE_LOOP)
        for v in polygon.vertices:
            world_v = body.transform * v
            sx, sy = SpriteDynamicGL.world_to_screen(world_v[0], world_v[1], camera)
            glVertex2f(sx, sy)
        glEnd()

    @staticmethod
    def draw_circle(sprite, body, circle, camera):
        """Draw a single circle fixture (immediate-mode)."""
        if (not sprite.draw_colliders):
            return
        glBegin(GL_LINE_LOOP)
        center = body.transform * circle.pos
        radius = circle.radius

        for i in range(24):
            angle = 2 * math.pi * i / 24
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            sx, sy = SpriteDynamicGL.world_to_screen(x, y, camera)
            glVertex2f(sx, sy)

        glEnd()

    @classmethod
    def DrawDebugWorld(cls, world, camera):

        if (not SpriteDynamicGL.DEBUG_ENABLED):
            return 
        """Draw all bodies' fixtures in the Box2D world using immediate-mode GL.

        This mirrors the working `debug_draw_world` in `pythonPhysics.py` and is
        intentionally standalone so you can edit it easily.
        """
        glUseProgram(0)
        glColor3f(0, 1, 0)
        glLineWidth(2)

        # Setup simple ortho to map pixel coordinates to screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, camera.width, camera.height, 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        all_sprites = [obj.sprite for obj in GameObject.all_objects if obj.sprite is not None]

        try:
            for sprite in all_sprites:
                if isinstance(sprite, SpriteDynamicGL) and hasattr(sprite, 'body') and sprite.body is not None:
                    for fixture in sprite.body.fixtures:
                        shape = fixture.shape
                        if shape.type == 0:  # circle
                            cls.draw_circle(sprite,sprite.body, shape, camera)
                        elif shape.type == 2:  # polygon
                            cls.draw_polygon(sprite,sprite.body, shape, camera)
        finally:
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()



