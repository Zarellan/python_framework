import pygame
import math
import numpy as np
from Libraries.utils import get_mouse_ui_pos
from Libraries.Texture import Texture
from collections import defaultdict
from Libraries.Deltatime import Deltatime
from OpenGL.GL import *
from Libraries.TagRegistry import TagRegistry

class SpriteGL:

    textures_append = {}
    sprite = ""
    tag_name = ""
    texture_path = ""
    layers = defaultdict(list)
    origin_centered: bool = True
    camera = None

    animation_frames = []
    animation_index = 0
    animation_timer = 0
    animation_speed = 1.0
    animation_loop = False
    animation_finished = False
    animation_finished_VA = False
    x = 0
    y = 0
    def __init__(self, image_path, camera, tag="none", layer_index = 0,is_world = True, origin_center = False, is_pixel = False):
        # Load image with pygame
        if (image_path not in SpriteGL.textures_append):
            surface = pygame.image.load("image/" + image_path + ".png").convert_alpha()
            SpriteGL.textures_append[image_path] = Texture(surface, GL_NEAREST if is_pixel else GL_LINEAR)
        
        self.layer_index = max(layer_index,0)
        SpriteGL.layers[self.layer_index].append(self)
        self.x = 0
        self.y = 0
        self.tag = tag
        self.origin_centered = origin_center
        self.camera = camera
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0.0
        self.alpha = 1.0
        self.is_world = is_world
        
        self.texture_path= image_path
        # Upload to OpenGL
        self.texture = SpriteGL.textures_append[image_path]
        self.width = self.texture.width
        self.height = self.texture.height
        
        self.original_width = self.width
        self.original_height = self.height

        self.origin_x = self.width / 2
        self.origin_y = self.height / 2
        
        # Cached rect to avoid recalculating every frame
        self._cached_rect = None
        self._cached_scale_x = None
        self._cached_scale_y = None
        self._cached_x = None
        self._cached_y = None

        # register sprite in global list
        # self.all_sprites.append(self)

        # if self.tag not in SpriteGL.all_tags:
        #     TagRegistry.ensure_tag(self.tag)
        #     SpriteGL.all_tags.append(self.tag)



    # def change_animation(self):
    #     self.play_animation()

    def set_animation(self, frames, speed = 1.0, isLoop = False):
        self.animation_frames = frames
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = speed
        self.animation_loop = isLoop
        self.animation_finished = False
        self.animation_finished_VA = False
        self.change_animation()

    def change_animation(self):
        frame_path = self.animation_frames[self.animation_index]
        if frame_path not in SpriteGL.textures_append:
            surface = pygame.image.load("image/" + frame_path + ".png").convert_alpha()
            SpriteGL.textures_append[frame_path] = Texture(surface)
        
        self.texture = SpriteGL.textures_append[frame_path]

        self.animation_index += 1
        if (self.animation_finished):
            self.animation_finished_VA = True
        if (self.animation_index > len(self.animation_frames) - 1):
            self.animation_index = 0
            if (not self.animation_loop):
                self.animation_finished = True
            
    def update_draw(self): # for SpriteDynamicInheritance
        pass

    def play_animation(self):
        
        self.animation_timer += Deltatime.dt
        if (self.animation_timer > self.animation_speed):
            self.animation_timer = 0
            if (not self.animation_finished_VA):
                self.change_animation()

    def change_image(self, image_path):
        if (image_path not in SpriteGL.textures_append):
            surface = pygame.image.load("image/" + image_path + ".png").convert_alpha()
            SpriteGL.textures_append[image_path] = Texture(surface)

        self.texture = SpriteGL.textures_append[image_path]
    
    def get_model_matrix(self):
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)

        sx = self.scale_x
        sy = self.scale_y

        tx = self.x
        ty = self.y

        ox = self.origin_x
        oy = self.origin_y

        return np.array([
            [ cos_r * sx, -sin_r * sy, 0, tx - ox * cos_r * sx + oy * sin_r * sy],
            [ sin_r * sx,  cos_r * sy, 0, ty - ox * sin_r * sx - oy * cos_r * sy],
            [ 0,           0,          1, 0],
            [ 0,           0,          0, 1],
        ], dtype=np.float32)


    @property
    def rect(self):
        # Use scaled width/height
        w = self.width * self.scale_x
        h = self.height * self.scale_y

        # Centered origin → rect top-left
        if self.origin_centered:
            x = self.x - w / 2
            y = self.y - h / 2
        else:
            x = self.x
            y = self.y

        return pygame.Rect(x, y, w, h)

    def set_layer(self, new_layer):
        if self in SpriteGL.layers[self.layer_index]:
            SpriteGL.layers[self.layer_index].remove(self)
        # Add to new layer
        self.layer_index = max(new_layer,0)
        SpriteGL.layers[self.layer_index].append(self)
    
    # # ✅ Class method to get all sprites by tag
    # @classmethod
    # def get_all_by_tag(cls, tag_name):
    #     return [sprite for sprite in cls.all_sprites if sprite.tag == tag_name]
    # # Class method to draw all sprites
    # @classmethod
    # def UpdateAllDraw(cls, display, camera):
    #     for i in range(max(4)):
    #         for sprite in cls.all_sprites:
    #             if (sprite.layer_index == i):
    #                 sprite.update_draw(display, camera)

    # @classmethod
    # def UpdateAllAnimation(cls):
    #     for sprite in cls.all_sprites:
    #         if (sprite.animation_frames):
    #             sprite.play_animation()

    # Optional: remove a sprite from the central list
    def destroy(self):
        """
        Destroy this sprite without deleting the GPU texture.
        Removes references from parent GameObject and rendering layers.
        """
        # Remove references from parent GameObject if any
        if hasattr(self, "parent_object"):
            self.parent_object.sprite = None

        # Remove sprite from its rendering layer so it won't be drawn
        try:
            if hasattr(self, 'layer_index') and self in SpriteGL.layers.get(self.layer_index, []):
                SpriteGL.layers[self.layer_index].remove(self)
        except Exception:
            pass

        # Do NOT delete self.texture — keep it in GPU memory
        self.texture = None


    # def destroy(self):
    # """
    # Destroy this sprite and safely free GPU memory,
    # without relying on global all_sprites.
    # """
    # # Remove references from parent GameObject if any
    # if hasattr(self, "parent_object"):
    #     try:
    #         self.parent_object.sprite = None
    #     except Exception:
    #         pass

    # # Remove sprite from its layer so renderer won't try to draw it
    # try:
    #     if hasattr(self, 'layer_index') and self in SpriteGL.layers.get(self.layer_index, []):
    #         SpriteGL.layers[self.layer_index].remove(self)
    # except Exception:
    #     pass

    # # Delete texture only if no other sprite references it
    # if hasattr(self, "texture") and self.texture is not None:
    #     tex = self.texture
    #     other_uses = False
    #     for lst in SpriteGL.layers.values():
    #         for spr in lst:
    #             if spr is self:
    #                 continue
    #             if getattr(spr, 'texture', None) is tex:
    #                 other_uses = True
    #                 break
    #         if other_uses:
    #             break

    #     if other_uses:
    #         # Another sprite still uses this texture; do not delete GPU resource
    #         try:
    #             # just clear our reference
    #             self.texture = None
    #         except Exception:
    #             self.texture = None
    #     else:
    #         try:
    #             tex.delete()
    #         except Exception:
    #             pass
    #         self.texture = None


    # @classmethod
    # def destroy_all(cls, skip=None):
    #     """
    #     Destroy all sprites and free GPU memory.
    #     skip: list of sprites to keep (persistent)
    #     """
    #     if skip is None:
    #         skip = []

    #     # Determine textures that must be preserved because skip sprites use them
    #     textures_to_keep = set()
    #     for s in skip:
    #         if hasattr(s, "texture") and s.texture is not None:
    #             textures_to_keep.add(s.texture)

    #     for sprite in cls.all_sprites:
    #         if sprite in skip:
    #             continue
    #         if hasattr(sprite, "texture") and sprite.texture is not None:
    #             # Only delete texture if it's not used by a persistent sprite
    #             if sprite.texture not in textures_to_keep:
    #                 try:
    #                     sprite.texture.delete()
    #                 except Exception:
    #                     pass
    #             sprite.texture = None

    #     # Only keep the persistent sprites in the global list
    #     cls.all_sprites = [s for s in cls.all_sprites if s in skip]


    def MouseIsOverlap(self, ui_camera):
        mouse_x, mouse_y = get_mouse_ui_pos(ui_camera)

        ui_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


        if ui_rect.collidepoint(mouse_x, mouse_y):
            return 1
