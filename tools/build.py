import shutil

from tools import configs
from tools.configs import path_define
from tools.services import dump_service, font_service, image_service, publish_service


def main() -> None:
    if path_define.BUILD_DIR.exists():
        shutil.rmtree(path_define.BUILD_DIR)

    for dump_config in configs.DUMP_CONFIGS:
        dump_service.dump_font(dump_config)

    for font_config in configs.FONT_CONFIGS:
        glyph_sequence, character_mapping = font_service.collect_glyph_files(font_config)
        font_service.make_fonts(font_config, glyph_sequence, character_mapping)
        image_service.make_preview_image(font_config)

    publish_service.make_release_zips()
    publish_service.update_docs()
    publish_service.update_www()


if __name__ == '__main__':
    main()
