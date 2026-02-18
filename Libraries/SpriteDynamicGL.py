from Libraries.spriteGL import SpriteGL
from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2_staticBody
import pygame
from Libraries.Texture import Texture
from OpenGL.GL import *
import math
from Box2D import b2Filter
from Libraries.TagRegistry import TagRegistry

class SpriteDynamicGL(SpriteGL):
    PPU = 32  # pixels per unit (default)
    DEBUG_ENABLED = True
    draw_colliders = False

    @classmethod
    def set_ppu(cls, ppu_value):
        cls.PPU = ppu_value

    def __init__(self, world, camera, position=(5,5), size=(1,1),
                 density=1.0, friction=0.3, texture_name="background", color=(1,0,0), tag="None", bodyType = b2_dynamicBody, ppu=None):
        """
        world        : Box2D world
        camera       : Camera object for SpriteGL
        position     : (x, y) in world units
        size         : (width, height) in world units
        density      : Box2D fixture density
        friction     : Box2D fixture friction
        texture_name : sprite name
        color        : RGB tuple
        tag          : optional tag
        ppu          : pixels per unit override (optional)
        """
        # choose PPU (instance override or class default)
        self.PPU = ppu if ppu is not None else self.__class__.PPU

        # --- Create Box2D dynamic body ---
        if (bodyType == b2_dynamicBody):
            self.body = world.CreateDynamicBody(position=position)
        else:
            self.body = world.CreateStaticBody(position=position)
        self.body.CreatePolygonFixture(box=(size[0]/2, size[1]/2), density=density, friction=friction)

        self.body.userData = tag

        self.body.type = bodyType
        # Compute pixel size
        width_px = size[0] * self.PPU
        height_px = size[1] * self.PPU

        # Initialize SpriteGL
        super().__init__(
            texture_name,
            self.body.position[0]*self.PPU - width_px/2,
            self.body.position[1]*self.PPU - height_px/2,
            camera,
            tag=tag
        )

        self.width = width_px
        self.height = height_px
        self.color = color
        self.body_ref = self.body

    def set_height(self, desired_world_height):
        texture = SpriteGL.textures_append[self.texture_path]
        ppu = texture.height / desired_world_height
        world_width = texture.width / ppu
        world_height = desired_world_height

        # Update sprite and fixture
        self.PPU = ppu
        self.set_size(world_width, world_height)
    
    def include_colliders(self, mask_tags):
        fixture = self.body.fixtures[0]
        f = b2Filter()
        f = fixture.filterData
        f.categoryBits = TagRegistry.get_category(self.tag)
        mask = 0
        for tag in mask_tags:
            if (tag in TagRegistry._tag_map):
                mask |= TagRegistry.get_category(tag)
            else:
                raise KeyError(f"**{tag}** doesn't exist in the tag (reminder: did you add the object with tag early ?)")
        f.maskBits = mask

        fixture.filterData = f
        fixture.Refilter()

    def exclude_colliders(self, mask_tags):
        fixture = self.body.fixtures[0]
        f = b2Filter()
        f = fixture.filterData
        f.categoryBits = TagRegistry.get_category(self.tag)
        mask = 0
        for tag in mask_tags:
            if (tag in TagRegistry._tag_map):
                mask |= TagRegistry.get_category(tag)
            else:
                raise KeyError(f"**{tag}** doesn't exist in the tag")
        f.maskBits = 0xFFFF & ~mask

        fixture.filterData = f
        fixture.Refilter()

    def set_desired_height(self, desired_world_height):
        """
        Resize the sprite and Box2D fixture to match a desired world height,
        keeping the original texture aspect ratio.
        """
        texture = SpriteGL.textures_append[self.texture_path]

        # Keep PPU fixed
        PPU = self.PPU

        # Calculate world width based on aspect ratio
        aspect_ratio = texture.width / texture.height
        world_height = desired_world_height
        world_width = world_height * aspect_ratio

        # Update Box2D fixture
        self.set_size(world_width, world_height)

        # Update sprite pixel size for rendering
        self.width = world_width * PPU
        self.height = world_height * PPU
        print(self.height)
        # Sync sprite position
        self.update_draw()



    @classmethod
    def create_with_desired_height(cls, world, camera, texture_name, desired_world_height,
                                position=(0, 0), bodyType=b2_dynamicBody, density=1.0, friction=0.3):
        """
        Automatically scale sprite based on texture height and desired world height.
        Uses the normal constructor so SpriteGL and textures are initialized correctly.
        """
        # Ensure texture is loaded (use same Texture constructor as SpriteGL.__init__)
        if texture_name not in SpriteGL.textures_append:
            surface = pygame.image.load("image/" + texture_name + ".png").convert_alpha()
            SpriteGL.textures_append[texture_name] = Texture(surface)

        texture = SpriteGL.textures_append[texture_name]
        texture_width_px = texture.width
        texture_height_px = texture.height

        # Calculate PPU to match desired world height
        ppu = texture_height_px / desired_world_height

        # Calculate world width to preserve aspect ratio
        world_width = texture_width_px / ppu
        world_height = desired_world_height

        # Create using the normal constructor so everything is properly initialized
        sprite = cls(
            world,
            camera,
            position=position,
            size=(world_width, world_height),
            density=density,
            friction=friction,
            texture_name=texture_name,
            bodyType=bodyType,
            ppu=ppu
        )

        # Ensure initial draw values are synced so renderer sees correct x/y/size
        try:
            sprite.update_draw()
        except Exception:
            sprite.update()

        return sprite



    def update(self):
        """Sync sprite with Box2D body every frame"""
        self.x = self.body.position[0]*self.PPU - self.width/2
        self.y = self.body.position[1]*self.PPU - self.height/2
        self.rotation = self.body.angle
    
    @staticmethod
    def get_fixture_size(fixture): # in case I need it
        shape = fixture.shape
        if hasattr(shape, 'box'):
            hx, hy = shape.box
            return hx * 2, hy * 2
        else:
            vertices = shape.vertices
            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)
            return width, height
    
    def set_size(self, new_width, new_height, density=None, friction=None):
        """
        Resize the Box2D fixture and update sprite size.
        new_width, new_height: in world units
        density, friction: optional, fallback to old values
        """
        # Store old fixture properties
        old_fixture = self.body.fixtures[0]  # assuming one main fixture
        old_density = old_fixture.density if density is None else density
        old_friction = old_fixture.friction if friction is None else friction

        # Destroy old fixture
        self.body.DestroyFixture(old_fixture)

        # Create new fixture
        self.body.CreatePolygonFixture(
            box=(new_width/2, new_height/2),
            density=old_density,
            friction=old_friction
        )

        # Update sprite size in pixels
        self.width = new_width * self.PPU
        self.height = new_height * self.PPU

    def update_draw(self):
        self.body = self.body_ref
        self.width = self.width
        self.height = self.height
        # center the sprite on the body
        self.x = self.body.position[0] * self.PPU - self.width / 2
        self.y = self.body.position[1] * self.PPU - self.height / 2
        self.rotation = self.body.angle  # rotate to match body

    # @classmethod
    # def UpdateAllDraw(cls):
    #     for sprite in cls.all_sprites:
    #         sprite.update_draw()

    def apply_linear(self, x, y):
        self.body.linearVelocity = (x, y)

    def apply_linear_Impulse(self, x, y):
        self.body.ApplyLinearImpulse((x,y),self.body.worldCenter, False)

    def apply_force(self, fx, fy):
        self.body.ApplyForceToCenter((fx, fy), True)

    def apply_impulse(self, ix, iy):
        self.body.ApplyLinearImpulse((ix, iy), self.body.worldCenter, True)


    # ---- Debug draw helpers (immediate-mode, easy to edit) ----
    @staticmethod
    def world_to_screen(x, y, camera, ppu=None):
        """Convert world units to screen pixels using PPU and camera (matches pythonPhysics.world_to_screen)."""
        ppu = ppu if ppu is not None else SpriteDynamicGL.PPU
        x_px = x * ppu
        y_px = y * ppu

        cam_cx = camera.width / 2
        cam_cy = camera.height / 2

        rel_x = x_px - camera.x
        rel_y = y_px - camera.y

        screen_x = cam_cx + (rel_x - cam_cx) * camera.zoom
        screen_y = cam_cy + (rel_y - cam_cy) * camera.zoom

        return screen_x, screen_y

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

        try:
            for sprite in SpriteGL.all_sprites:
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



