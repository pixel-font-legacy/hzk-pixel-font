from typing import Literal

type FontType = Literal['asc', 'hzk']


class DumpConfig:
    font_name: str
    font_type: FontType
    font_size: int

    def __init__(
            self,
            font_name: str,
            font_type: FontType,
            font_size: int,
    ) -> None:
        self.font_name = font_name
        self.font_type = font_type
        self.font_size = font_size
