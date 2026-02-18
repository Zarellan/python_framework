import pygame
import numpy as np
from OpenGL.GL import *

class Texture:
    def __init__(self, surface, format = GL_LINEAR):
        self.id = glGenTextures(1)
        self.surface = surface
        glBindTexture(GL_TEXTURE_2D, self.id)

        # Upload surface pixels to GPU
        image_data = pygame.image.tostring(surface, "RGBA", True)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, format)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, format)

        self.width = surface.get_width()
        self.height = surface.get_height()

    def bind(self):
        # If texture was deleted `self.id` can be None — skip binding then.
        if getattr(self, 'id', None) is None:
            return
        glBindTexture(GL_TEXTURE_2D, self.id)

    def delete(self):
        if getattr(self, 'id', None):
            try:
                glDeleteTextures([self.id])
            except Exception:
                pass
            self.id = None
