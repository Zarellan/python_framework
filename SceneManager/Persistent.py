from Libraries.GameObject import GameObject

class Persistent:
    # store GameObject instances (wrappers), not raw SpriteGL
    objects = []

    @classmethod
    def dont_destroy_on_load(cls, obj):
        """Add a GameObject to persistent storage."""
        if not isinstance(obj, GameObject):
            print("Persistent: ignoring non-GameObject:", obj)
            return

        if obj not in cls.objects:
            cls.objects.append(obj)


    @classmethod
    def get_all(cls):
        return cls.objects
