class ScreenScaler:
    """
    Implements Unity-like Canvas Scaler for UI.
    Scales RectTransforms based on reference resolution.
    """
    def __init__(self, reference_width=1920, reference_height=1080):
        self.reference_width = reference_width
        self.reference_height = reference_height

    def get_scale_factor(self, screen_width, screen_height):
        scale_x = screen_width / self.reference_width
        scale_y = screen_height / self.reference_height
        # Uniform scale: use min or max to preserve aspect ratio
        return min(scale_x, scale_y)