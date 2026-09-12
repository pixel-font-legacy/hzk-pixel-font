import re
import shutil
from zipfile import ZipFile

from loguru import logger

from tools import configs
from tools.configs import path_define, options


def make_release_zips() -> None:
    path_define.RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    for font_format in options.FONT_FORMATS:
        file_path = path_define.RELEASES_DIR.joinpath(f'hzk-pixel-font-{font_format}-v{configs.VERSION}.zip')
        with ZipFile(file_path, 'w') as file:
            file.write(path_define.PROJECT_ROOT_DIR.joinpath('LICENSE-FONT.md'), 'README.md')
            for font_config in configs.FONT_CONFIGS:
                font_file_name = f'hzk-pixel-{font_config.font_size}px.{font_format}'
                file.write(path_define.OUTPUTS_DIR.joinpath(font_file_name), font_file_name)
        logger.info("Make release zip: '{}'", file_path)


def update_docs() -> None:
    path_define.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    regex_file_name = re.compile(r'^preview-.*px\.png$')
    for path_from in path_define.OUTPUTS_DIR.iterdir():
        if regex_file_name.match(path_from.name) is None:
            continue
        path_to = path_from.copy_into(path_define.DOCS_DIR)
        logger.info("Copy file: '{}' -> '{}'", path_from, path_to)


def update_www() -> None:
    if path_define.WWW_FONTS_DIR.exists():
        shutil.rmtree(path_define.WWW_FONTS_DIR)
    path_define.WWW_FONTS_DIR.mkdir(parents=True)

    for path_from in path_define.OUTPUTS_DIR.iterdir():
        if not path_from.name.endswith('.otf.woff2'):
            continue
        path_to = path_from.copy_into(path_define.WWW_FONTS_DIR)
        logger.info("Copy file: '{}' -> '{}'", path_from, path_to)
