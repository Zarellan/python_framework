from Libraries.Deltatime import Deltatime

class Tween:

    all_tweens = []
    
    #easings
    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def ease_in_quad(t):
        return t * t

    @staticmethod
    def ease_out_quad(t):
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t):
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    # You can add more: cubic, sine, bounce, etc.

    def __init__(self, start_value, end_value, duration, on_complete=None, setter=None, ease=linear):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.timer = 0.0
        self.on_complete = on_complete
        self.setter = setter
        self.ease = ease  # easing function
        self.value = start_value
        Tween.all_tweens.append(self)


    # Class method to tween sprite.x
    @classmethod
    def x(cls, sprite, end_value, duration, on_complete=None, ease=linear):
        return cls(
            start_value=sprite.x,
            end_value=end_value,
            duration=duration,
            on_complete=on_complete,
            ease = ease,
            setter=lambda val: setattr(sprite, "x", val)
        )

    # Class method to tween sprite.y
    @classmethod
    def y(cls, sprite, end_value, duration, on_complete=None):
        return cls(
            start_value=sprite.y,
            end_value=end_value,
            duration=duration,
            on_complete=on_complete,
            setter=lambda val: setattr(sprite, "y", val)
        )

    # Can also add scale, rotation, etc.
    @classmethod
    def scale_x(cls, sprite, end_value, duration, on_complete=None):
        return cls(
            start_value=sprite.scale_x,
            end_value=end_value,
            duration=duration,
            on_complete=on_complete,
            setter=lambda val: setattr(sprite, "scale_x", val)
        )

    @classmethod
    def alpha(cls, sprite, end_value, duration, on_complete=None, ease=linear):
        return cls(
            start_value=sprite.alpha,
            end_value=end_value,
            duration=duration,
            on_complete=on_complete,
            ease = ease,
            setter=lambda val: setattr(sprite, "alpha", val)
        )
    
    @classmethod
    def camera_zoom(cls, camera, end_value, duration, on_complete=None, ease=linear):
        return cls(
            start_value=camera.zoom,
            end_value=end_value,
            duration=duration,
            on_complete=on_complete,
            ease = ease,
            setter=lambda val: setattr(camera, "zoom", val)
        )


    def update(self):
        self.timer += Deltatime.dt
        t = min(self.timer / self.duration, 1.0)
        
        # Apply easing
        t_eased = self.ease(t)

        # Interpolate
        self.value = self.start_value + (self.end_value - self.start_value) * t_eased

        if self.setter:
            self.setter(self.value)

        if t >= 1.0:
            if self.on_complete:
                self.on_complete()
            Tween.all_tweens.remove(self)


    def stop(self):
        if self in Tween.all_tweens:
            Tween.all_tweens.remove(self)

    @classmethod
    def UpdateAllTweens(cls):
        for tween in cls.all_tweens[:]:
            tween.update()

