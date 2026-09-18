from collections.abc import Mapping, Sequence
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph
from pixel_font_knife.cmap.context import CmapContext
from pixel_font_knife.glyph.file import GlyphFile
from pixel_font_knife.named.file import NamedGlyphFile

from tools import configs
from tools.configs import FontConfig, options
from tools.configs import path_define


def collect_glyph_files(font_config: FontConfig) -> tuple[Sequence[GlyphFile], Mapping[int, str]]:
    notdef_glyph_file = NamedGlyphFile.load_notdef(path_define.GLYPHS_DIR.joinpath(str(font_config.font_size), 'notdef.png'))

    context = CmapContext()
    for source_name in font_config.source_names:
        context = context.merge_by_code_point(
            CmapContext.load(path_define.DUMP_DIR.joinpath(source_name)),
            conflict='replace',
        )

    glyph_sequence = [notdef_glyph_file] + context.get_glyph_sequence()
    character_mapping = context.get_character_mapping()
    return glyph_sequence, character_mapping


def _create_builder(font_config: FontConfig, glyph_sequence: Sequence[GlyphFile], character_mapping: Mapping[int, str]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = font_config.font_size // 2
    builder.font_metric.vertical_layout.descent = -font_config.font_size // 2
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = configs.VERSION
    builder.meta_info.created_time = datetime.fromisoformat(f'{configs.VERSION_TIME}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'HZK Pixel {font_config.font_size}px'
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.MONOSPACED

    for glyph_file in glyph_sequence:
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=glyph_file.canvas.horizontal_offset_for_trimmed(font_config.font_size, font_config.baseline),
            advance_width=glyph_file.canvas.advance_width(),
            vertical_offset=glyph_file.canvas.vertical_offset_for_trimmed(font_config.font_size),
            advance_height=glyph_file.canvas.advance_height(font_config.font_size),
            bitmap=glyph_file.canvas.trimmed_bitmap.data,
        ))

    builder.character_mapping.update(character_mapping)

    return builder


def make_fonts(font_config: FontConfig, glyph_sequence: Sequence[GlyphFile], character_mapping: Mapping[int, str]) -> None:
    path_define.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    builder = _create_builder(font_config, glyph_sequence, character_mapping)
    for font_format in options.FONT_FORMATS:
        file_path = path_define.OUTPUTS_DIR.joinpath(f'hzk-pixel-{font_config.font_size}px.{font_format}')
        getattr(builder, f'save_{font_format.replace('.', '_')}')(file_path)
        logger.info("Make font: '{}'", file_path)
