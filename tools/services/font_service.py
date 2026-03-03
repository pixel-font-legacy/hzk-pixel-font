import math
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph, opentype
from pixel_font_knife import glyph_file_util
from pixel_font_knife.glyph_file_util import GlyphFile

from tools import configs
from tools.configs import FontConfig, options
from tools.configs import path_define


def collect_glyph_files(font_config: FontConfig) -> tuple[list[GlyphFile], dict[int, str]]:
    context = glyph_file_util.load_context(path_define.glyphs_dir.joinpath(str(font_config.font_size)))
    for source_name in font_config.source_names:
        context.update(glyph_file_util.load_context(path_define.dump_dir.joinpath(source_name)))

    glyph_sequence = glyph_file_util.get_glyph_sequence(context)
    character_mapping = glyph_file_util.get_character_mapping(context)
    return glyph_sequence, character_mapping


def _create_builder(font_config: FontConfig, glyph_sequence: list[GlyphFile], character_mapping: dict[int, str]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = font_config.font_size // 2
    builder.font_metric.vertical_layout.descent = -font_config.font_size // 2
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = configs.version
    builder.meta_info.created_time = datetime.fromisoformat(f'{configs.version_time}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'HZK Pixel {font_config.font_size}px'
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.MONOSPACED

    for glyph_file in glyph_sequence:
        horizontal_offset_y = (font_config.ascent + font_config.descent - glyph_file.height) // 2
        vertical_offset_x = -math.ceil(glyph_file.width / 2)
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=(0, horizontal_offset_y),
            advance_width=glyph_file.width,
            vertical_offset=(vertical_offset_x, 0),
            advance_height=font_config.font_size,
            bitmap=glyph_file.bitmap.data,
        ))

    builder.character_mapping.update(character_mapping)

    return builder


def make_fonts(font_config: FontConfig, glyph_sequence: list[GlyphFile], character_mapping: dict[int, str]):
    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)

    builder = _create_builder(font_config, glyph_sequence, character_mapping)
    for font_format in options.font_formats:
        file_path = path_define.outputs_dir.joinpath(f'hzk-pixel-{font_config.font_size}px.{font_format}')
        match font_format:
            case 'otf.woff':
                builder.save_otf(file_path, flavor=opentype.Flavor.WOFF)
            case 'otf.woff2':
                builder.save_otf(file_path, flavor=opentype.Flavor.WOFF2)
            case 'ttf.woff':
                builder.save_ttf(file_path, flavor=opentype.Flavor.WOFF)
            case 'ttf.woff2':
                builder.save_ttf(file_path, flavor=opentype.Flavor.WOFF2)
            case _:
                getattr(builder, f'save_{font_format}')(file_path)
        logger.info("Make font: '{}'", file_path)
