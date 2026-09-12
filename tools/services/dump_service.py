import math

from character_encoding_utils import gb2312
from character_encoding_utils.gb2312 import GB2312Exception
from loguru import logger
from pixel_font_knife.mono_bitmap import MonoBitmap

from tools.configs import DumpConfig, path_define


def _parse_bitmap(bitmap_bytes: bytes, row_bytes_size: int, width: int, height: int) -> MonoBitmap:
    bitmap = MonoBitmap()
    bitmap.width = width
    bitmap.height = height
    for row_index in range(height):
        bitmap_row = []
        for col_index in range(row_bytes_size):
            b = bitmap_bytes[row_index * row_bytes_size + col_index]
            row_string = f'{b:08b}'
            bitmap_row.extend(int(c) for c in row_string)
        bitmap.append(bitmap_row[:width])
    return bitmap


def dump_font(dump_config: DumpConfig) -> None:
    dump_dir = path_define.DUMP_DIR.joinpath(dump_config.font_name)
    dump_dir.mkdir(parents=True, exist_ok=True)

    with path_define.FONTS_DIR.joinpath(dump_config.font_name).open('rb') as file:
        if dump_config.font_type == 'asc':
            row_bytes_size = math.ceil(dump_config.font_size / 2 / 8)
            bitmap_bytes_size = row_bytes_size * dump_config.font_size
            for code_point in range(0, 255 + 1):
                file.seek(code_point * bitmap_bytes_size)
                bitmap_bytes = file.read(bitmap_bytes_size)
                if len(bitmap_bytes) == 0:
                    break
                bitmap = _parse_bitmap(bitmap_bytes, row_bytes_size, dump_config.font_size // 2, dump_config.font_size)
                bitmap.save_png(dump_dir.joinpath(f'{code_point:04X}.png'))
        else:
            assert dump_config.font_type == 'hzk'
            row_bytes_size = math.ceil(dump_config.font_size / 8)
            bitmap_bytes_size = row_bytes_size * dump_config.font_size
            for row in range(1, 94 + 1):
                for col in range(1, 94 + 1):
                    try:
                        c = gb2312.query_chr(row, col)
                    except GB2312Exception:
                        continue
                    file.seek(((row - 1) * 94 + (col - 1)) * bitmap_bytes_size)
                    bitmap_bytes = file.read(bitmap_bytes_size)
                    bitmap = _parse_bitmap(bitmap_bytes, row_bytes_size, dump_config.font_size, dump_config.font_size)
                    bitmap.save_png(dump_dir.joinpath(f'{ord(c):04X}.png'))

    logger.info('Dump font: {}', dump_config.font_name)
