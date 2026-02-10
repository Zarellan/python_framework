import numpy as np
import pygame
import ctypes
from OpenGL.GL import *
from Libraries.Shader import Shader
from Libraries.spriteGL import SpriteGL

class SpriteRendererGL:
    def __init__(self, screen_width, screen_height):
        self.projection = self.ortho(0, screen_width, screen_height, 0)
        self.shader = self._create_shader()
        self.quad = self._create_quad()
        # Enable alpha blending for textures with alpha channel
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def draw(self, sprites):
        self.shader.use()
        self.shader.set_mat4("projection", self.projection)
        
        max_layer = max(SpriteGL.layers.keys(), default=-1)
        for i in range(max_layer + 1):
            for sprite in SpriteGL.layers[i]:
                sprite_rect = pygame.Rect(sprite.x, sprite.y, sprite.width, sprite.height)
                camera_rect = pygame.Rect(sprite.camera.x, sprite.camera.y, sprite.camera.width, sprite.camera.height)
                if camera_rect.colliderect(sprite_rect):
                    loc = glGetUniformLocation(self.shader.id, "global_alpha")
                    sprite_alpha = getattr(sprite, "alpha", 255.0)
                    camera_alpha = getattr(sprite.camera, "alpha", 255.0)
                    final_alpha = sprite_alpha * camera_alpha
                    glUniform1f(loc, max(0.0,min(1.0,final_alpha)))
                    self._draw_sprite(sprite, sprite.camera)



    @staticmethod
    def ortho(left, right, bottom, top, near=-1.0, far=1.0):
        return np.array([
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -2 / (far - near), -(far + near) / (far - near)],
            [0, 0, 0, 1],
        ], dtype="f4")

    def _create_quad(self):
        # Quad centered at origin (0,0)
        vertices = np.array([
            -0.5, -0.5, 0, 1,  # bottom-left
            0.5, -0.5, 1, 1,  # bottom-right
            0.5,  0.5, 1, 0,  # top-right
            -0.5, -0.5, 0, 1,  # bottom-left
            0.5,  0.5, 1, 0,  # top-right
            -0.5,  0.5, 0, 0,  # top-left
        ], dtype='f4')

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))

        # uv attribute
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return vertices

    

    def _draw_sprite(self, sprite, camera):
        # Apply camera zoom
        zoom = getattr(camera, "zoom", 1.0)
        
        # # cancelled since it zoom from left_top instead of center
        # tx = (sprite.x - camera.x + sprite.width / 2) * zoom  # move to sprite center
        # ty = (sprite.y - camera.y + sprite.height / 2) * zoom

        # Camera center position on screen
        cam_cx = camera.width / 2
        cam_cy = camera.height / 2

        # Position relative to camera center
        rel_x = sprite.x - camera.x + sprite.width / 2
        rel_y = sprite.y - camera.y + sprite.height / 2

        # Apply zoom around screen center
        tx = cam_cx + (rel_x - cam_cx) * zoom
        ty = cam_cy + (rel_y - cam_cy) * zoom

        r = getattr(sprite, "rotation", 0.0)
        c = np.cos(r)
        s = np.sin(r)

        # Scale also affected by zoom
        sx = sprite.width * getattr(sprite, "scale_x", 1.0) * zoom
        sy = sprite.height * getattr(sprite, "scale_y", 1.0) * zoom

        # TRS matrix
        model = np.array([
            [c * sx, -s * sy, 0.0, tx],
            [s * sx,  c * sy, 0.0, ty],
            [0.0,     0.0,    1.0, 0.0],
            [0.0,     0.0,    0.0, 1.0],
        ], dtype="f4")

        self.shader.set_mat4("model", model)

        glActiveTexture(GL_TEXTURE0)
        sprite.texture.bind()

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)




    def _create_shader(self):
        shader = Shader("Libraries/sprite.vert", "Libraries/sprite.frag")
        # ensure shader uses texture unit 0 for sprite_texture uniform
        shader.use()
        shader.set_mat4("projection", self.projection)

        loc = glGetUniformLocation(shader.id, "sprite_texture")
        if loc != -1:
            glUniform1i(loc, 0)
        return shader
    
    def cleanup(self):
        """Clean up all OpenGL resources"""
        if hasattr(self, 'VAO'):
            glDeleteVertexArrays(1, [self.VAO])
        if hasattr(self, 'VBO'):
            glDeleteBuffers(1, [self.VBO])
        if hasattr(self, 'shader'):
            glDeleteProgram(self.shader.id)


