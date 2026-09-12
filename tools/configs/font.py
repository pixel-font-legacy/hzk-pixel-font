
class FontConfig:
    font_size: int
    ascent: int
    descent: int
    x_height: int
    cap_height: int
    source_names: list[str]

    def __init__(
            self,
            font_size: int,
            ascent: int,
            descent: int,
            x_height: int,
            cap_height: int,
            source_names: list[str],
    ) -> None:
        self.font_size = font_size
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height
        self.source_names = source_names
