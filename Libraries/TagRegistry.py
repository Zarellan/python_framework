class TagRegistry:
    """
    Assigns unique Box2D category bits to string tags.
    Ensures no collisions and stable mapping.
    """
    _next_bit = 0x0001  # start at bit 0
    _tag_map = {}       # string -> categoryBits
    _max_bits = 16      # Box2D only supports 16 bits

    @classmethod
    def ensure_tag(cls, tag: str):
        """
        Ensure the tag exists in the registry. If not, add it.
        Does not return anything by default.
        """
        if tag not in cls._tag_map:
            if cls._next_bit > (1 << (cls._max_bits - 1)):
                raise RuntimeError("Exceeded maximum number of Box2D category bits (16).")
            cls._tag_map[tag] = cls._next_bit
            cls._next_bit <<= 1  # move to the next bit

    @classmethod
    def get_category(cls, tag: str) -> int:
        """
        Get the Box2D categoryBits for a tag.
        Raises KeyError if tag not registered.
        """
        return cls._tag_map[tag]

    @classmethod
    def debug_all(cls):
        """Print all registered tags and their bits (binary for clarity)"""
        for t, b in cls._tag_map.items():
            print(f"{t}: {b:016b}")
