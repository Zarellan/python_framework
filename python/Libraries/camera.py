# class Camera:
#     def __init__(self, width, height, screen_height):
#         """
#         width, height: viewport size
#         screen_height: the Pygame display height, used for flipping y
#         """
#         self.x = 0
#         self.y = 0
#         self.width = width
#         self.height = height
#         self.screen_height = screen_height  # needed for y flip

#     # def follow(self, target):
#     #     """
#     #     Center the camera on the target (usually the player)
#     #     """
#     #     self.x = target.x - self.width // 2
#     #     self.y = self.y_correction(target.y) - self.height // 2

#     def follow(self, target, lerp=1):
#         self.x += (target.x - self.width // 2 - self.x) * lerp
#         self.y += (self.y_correction(target.y + 50) - self.height // 2 - self.y) * lerp

#     def apply(self, sprite):
#         """
#         Convert sprite's world coordinates into screen coordinates
#         with proper y-axis flip
#         """
#         # Flip y and offset by camera
#         screen_x = sprite.x - self.x
#         screen_y = self.y_correction(sprite.y) - self.y - sprite.height
#         return screen_x, screen_y
    
#     def y_correction(self,y):
#         return self.screen_height - y

#     @property
#     def pos(self):
#         # OpenGL typically uses bottom-left origin, so we flip y
#         return (self.x, self.y)



class Camera:
    def __init__(self, width, height, screen_height, is_ui=False, alpha=255, zoom=1.0):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.screen_height = screen_height
        self.is_ui = is_ui        # If True, this camera is for UI, no movement
        self.alpha = alpha        # 0 = fully transparent, 255 = fully opaque
        self.zoom = zoom          # 1.0 = normal, >1 = zoom in, <1 = zoom out

    def follow(self, target, dt, lerp=4):
        if self.is_ui:
            return  # UI camera never moves
        try:
            target_cx = target.rect.centerx
            target_cy = target.rect.centery
        except Exception:
            target_cx = getattr(target, 'x', 0)
            target_cy = getattr(target, 'y', 0)

        self.x += (target_cx - self.width / 2 - self.x) * lerp * dt
        self.y += (target_cy - self.height / 2 - self.y) * lerp * dt

    def apply(self, sprite):
        cam_cx = self.width / 2
        cam_cy = self.height / 2

        if self.is_ui or not getattr(sprite, "on_world", True):
            rel_x = sprite.x
            rel_y = self.screen_height - sprite.y - sprite.height
        else:
            rel_x = sprite.x - self.x
            rel_y = (self.screen_height - sprite.y - sprite.height) - self.y

        # Zoom relative to center
        screen_x = cam_cx + (rel_x - cam_cx) * self.zoom
        screen_y = cam_cy + (rel_y - cam_cy) * self.zoom

        return screen_x, screen_y






    def set_alpha(self, value):
        """Clamp and set alpha (0-255)"""
        self.alpha = max(0, min(255, value))

    def set_zoom(self, value):
        """Clamp zoom to positive numbers (avoid negative or zero)"""
        self.zoom = max(0.01, value)

    @property
    def pos(self):
        return (self.x, self.y)
