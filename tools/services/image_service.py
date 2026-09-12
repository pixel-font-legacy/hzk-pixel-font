from PIL import Image, ImageFont, ImageDraw
from loguru import logger

from tools.configs import FontConfig
from tools.configs import path_define


def make_preview_image(font_config: FontConfig) -> None:
    font = ImageFont.truetype(path_define.OUTPUTS_DIR.joinpath(f'hzk-pixel-{font_config.font_size}px.otf.woff2'), font_config.font_size)
    text_color = (0, 0, 0, 255)

    image = Image.new('RGBA', (font_config.font_size * 27, font_config.font_size * 11), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((font_config.font_size, font_config.font_size), '汉字库像素字体 / HZK Pixel Font', fill=text_color, font=font)
    draw.text((font_config.font_size, font_config.font_size * 3), '我们度过的每个平凡的日常，也许就是连续发生的奇迹。', fill=text_color, font=font)
    draw.text((font_config.font_size, font_config.font_size * 5), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', fill=text_color, font=font)
    draw.text((font_config.font_size, font_config.font_size * 7), 'the quick brown fox jumps over a lazy dog.', fill=text_color, font=font)
    draw.text((font_config.font_size, font_config.font_size * 9), '0123456789', fill=text_color, font=font)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = path_define.OUTPUTS_DIR.joinpath(f'preview-{font_config.font_size}px.png')
    image.save(file_path)
    logger.info("Make preview image: '{}'", file_path)
