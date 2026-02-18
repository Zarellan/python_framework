from Libraries.spriteGL import SpriteGL
from Libraries.TagRegistry import TagRegistry

class GameObject:
    all_objects = []
    all_tags = []
    def __init__(self, tag):
        self.sprite = None
        self.tag = tag
        self.__class__.all_objects.append(self)

        if self.tag not in GameObject.all_tags:
            TagRegistry.ensure_tag(self.tag)
            GameObject.all_tags.append(self.tag)



    def create_sprite(self,imagePath,x,y,camera):
        self.sprite = SpriteGL(imagePath,x,y,camera)
    def destroy(self):
        """Destroy this GameObject and its sprite."""
        # Destroy sprite safely
        if self.sprite:
            self.sprite.destroy()
            self.sprite = None

        if self in self.__class__.all_objects:
            self.__class__.all_objects.remove(self)

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

    # ✅ Class method to get all sprites by tag
    @classmethod
    def get_all_by_tag(cls, tag_name):
        return [obj for obj in cls.all_objects if obj.tag == tag_name]
    
    # Class method to draw all sprites
    @classmethod
    def UpdateAllDraw(cls, display, camera):
        for i in range(max(4)):
            for obj in cls.all_objects:
                if (obj.sprite.layer_index == i):
                    obj.sprite.update_draw(display, camera)

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