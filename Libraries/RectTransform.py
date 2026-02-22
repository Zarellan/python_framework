class RectTransform:
    def __init__(self, x=0, y=0, width=100, height=100, rotation=0, scale=(1,1), pivot=(0.5, 0.5), anchor_min=(0,0), anchor_max=(1,1), parent=None):
        # Base transform properties
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale

        # Size and pivot (0,0=bottom-left, 1,1=top-right)
        self.width = width
        self.height = height
        self.pivot = pivot  # e.g., (0.5, 0.5) = center

        # Anchors (relative to parent rect)
        self.anchor_min = anchor_min
        self.anchor_max = anchor_max

        # Optional parent RectTransform
        self.parent = parent

    @property
    def position(self):
        """Absolute position (considering parent and pivot)"""
        px, py = (0,0)
        if self.parent:
            # Parent position + scaled offset
            px = self.parent.x
            py = self.parent.y
        # Position with pivot offset
        ox = self.width * self.pivot[0]
        oy = self.height * self.pivot[1]
        return (px + self.x - ox, py + self.y - oy)

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_pivot(self, pivot):
        self.pivot = pivot

    def set_parent(self, parent):
        self.parent = parent

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_scale(self, sx, sy):
        self.scale = (sx, sy)

    def get_relative_position(self):
        """Position relative to parent without pivot correction"""
        if self.parent:
            return (self.x - self.parent.x, self.y - self.parent.y)
        return (self.x, self.y)