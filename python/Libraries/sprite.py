import pygame

from Libraries.utils import y_correction

class Sprite:

    all_sprites = []
    sprite = ""
    tag_name = ""

    x = 0
    y = 0
    def __init__(self,image,x, y, tag = "none"):
        self.sprite = pygame.image.load("image/" + image + ".png")
        self.x = x
        self.y = y_correction(y)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.all_sprites.append(self)
        self.tag = tag
        pass

    def update_draw(self, display, camera):
        display.blit(self.sprite, camera.apply(self))

    @property
    def rect(self):
    # Use flipped y for drawing, but rect uses logical coordinates
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # ✅ Class method to get all sprites by tag
    @classmethod
    def get_all_by_tag(cls, tag_name):
        return [sprite for sprite in cls.all_sprites if sprite.tag == tag_name]
    # Class method to draw all sprites
    @classmethod
    def UpdateAllDraw(cls, display, camera):
        for sprite in cls.all_sprites:
            sprite.update_draw(display, camera)

    # Optional: remove a sprite from the central list
    def destroy(self):
        if self in Sprite.all_sprites:
            Sprite.all_sprites.remove(self)
