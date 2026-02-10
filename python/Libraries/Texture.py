import pygame
import numpy as np
from OpenGL.GL import *

class Texture:
    def __init__(self, surface):
        self.id = glGenTextures(1)
        self.surface = surface
        glBindTexture(GL_TEXTURE_2D, self.id)

        # Upload surface pixels to GPU
        image_data = pygame.image.tostring(surface, "RGBA", True)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.width = surface.get_width()
        self.height = surface.get_height()

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)

    def delete(self):
        if self.id:
            glDeleteTextures([self.id])
            self.id = None
