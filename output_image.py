"""Generate an image that summarizes encoding information for a character."""

import sys
import tomllib as tl
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import emoji
import unicodedata2 as ud
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from get_encoding import CharacterEncodingInfo, build_character_info, prompt_for_character

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "configuration.toml"


def load_config(config_path: Path) -> dict[str, Any]:
    """Load the TOML configuration file.

    Args:
        config_path: Absolute path to the configuration file.

    Returns:
        Parsed configuration dictionary.
    """
    with open(config_path, "rb") as file:
        return tl.load(file)


def load_font(font_dir: Path, file_name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font file from the configured font directory.

    Args:
        font_dir: Directory that contains font files.
        file_name: Target font file name.
        size: Requested font size.

    Returns:
        Loaded TrueType/OpenType font instance.
    """
    return ImageFont.truetype(font_dir / file_name, size)


def select_character_font(character: str, font_dir: Path) -> ImageFont.FreeTypeFont:
    """Choose a font capable of rendering the provided character.

    Args:
        character: Character that will be drawn.
        font_dir: Directory containing available font files.

    Returns:
        A font instance sized appropriately for the canvas.
    """
    if emoji.purely_emoji(character):
        return load_font(font_dir, "AppleColorEmoji.ttf", 137)

    fallback_fonts = [
        "SourceHanSerifSC-Bold.otf",
        "TH-Tshyn-P0.ttf",
        "TH-Tshyn-P1.ttf",
        "TH-Tshyn-P2.ttf",
    ]
    for font_name in fallback_fonts:
        font_path = font_dir / font_name
        font = TTFont(font_path)
        try:
            cmap = font.getBestCmap() or {}
            if ord(character) in cmap:
                return load_font(font_dir, font_name, 350)
        finally:
            font.close()
    return load_font(font_dir, "TH-Tshyn-P16.ttf", 350)


def resolve_unicode_name(character: str) -> str:
    """Return the Unicode name or a fallback label.

    Args:
        character: Character whose name should be resolved.

    Returns:
        Official Unicode character name or a fallback string.
    """
    try:
        return ud.name(character)
    except ValueError:
        return "Unknown Unicode Name"


def create_encoding_image(
    info: CharacterEncodingInfo,
    config: Mapping[str, Any],
) -> Image.Image:
    """Draw the encoding summary image using the provided configuration.

    Args:
        info: Aggregated encoding information for the character.
        config: Configuration dictionary controlling fonts, colors, and layout.

    Returns:
        Rendered Pillow image object.
    """
    colors = config["color"]
    font_dir = PROJECT_ROOT / config["input"]["font_folder"]

    image = Image.new("RGB", (1920, 1080), colors["background"])
    draw = ImageDraw.Draw(image)

    title_text = "字符编码查询"
    title_position = (150, 150)
    title_font = load_font(font_dir, "SourceHanSerifSC-Bold.otf", 85)
    title_bbox = list(title_font.getbbox(title_text))
    title_box_position = (
        title_bbox[0] + title_position[0] - 50,
        title_bbox[1] + title_position[1] - 50,
        title_bbox[2] + title_position[0] + 50,
        title_bbox[3] + title_position[1] + 50,
    )

    draw.rounded_rectangle(
        title_box_position,
        fill=colors["title_box"][0],
        radius=25,
        corners=(True, True, False, False),
    )
    title_box_position_2 = (
        title_box_position[0],
        title_box_position[3],
        title_box_position[2],
        title_box_position[3] + 600,
    )
    draw.rounded_rectangle(
        title_box_position_2,
        fill=colors["title_box"][1],
        radius=25,
        corners=(False, False, True, True),
    )
    draw.text(title_position, title_text, font=title_font, fill=colors["title"])

    text_size = 54
    text_font = load_font(font_dir, "SourceHanSerifSC-Regular.otf", text_size)
    text_font_small = load_font(font_dir, "SourceHanSerifSC-Regular.otf", text_size - 10)
    text_font_tiny = load_font(font_dir, "SourceHanSerifSC-Regular.otf", 28)
    text_font_bold = load_font(font_dir, "SourceHanSerifSC-Bold.otf", text_size)
    text_font_bold_small = load_font(font_dir, "SourceHanSerifSC-Bold.otf", text_size - 10)
    text_font_tc_bold_small = load_font(font_dir, "SourceHanSerifTC-Bold.otf", text_size - 10)

    character_font = select_character_font(info.character, font_dir)
    title_box_2_width = title_box_position_2[2] - title_box_position_2[0]
    title_box_2_height = title_box_position_2[3] - title_box_position_2[1]
    character_bbox = list(character_font.getbbox(info.character))
    character_width = character_bbox[2] - character_bbox[0]
    character_height = character_bbox[3] - character_bbox[1]
    character_box_position = (
        title_box_position_2[0] + title_box_2_width / 2 - character_width / 2,
        title_box_position_2[1] + title_box_2_height / 2 - character_height / 2,
        title_box_position_2[0] + title_box_2_width / 2 + character_width / 2,
        title_box_position_2[1] + title_box_2_height / 2 + character_height / 2,
    )
    draw.rectangle(
        character_box_position,
        outline=colors["character_outline"],
        width=5,
    )
    character_position = (
        character_box_position[0],
        character_box_position[1] - character_bbox[1],
    )
    draw.text(
        character_position,
        info.character,
        font=character_font,
        fill=colors["character"],
        embedded_color=emoji.purely_emoji(info.character),
    )

    unicode_name_position = (title_box_position[0], title_box_position[3] + 625)
    draw.text(
        unicode_name_position,
        resolve_unicode_name(info.character),
        font=text_font_tiny,
        fill=colors["unicode_name"],
    )

    encoding_list = "\n".join(
        [
            "ASCII",
            "Unicode",
            "GB/T 2312",
            "",
            "GB 18030",
            "",
            "大五码",
            "",
            "",
            "Shift JIS",
            "EUC-KR",
        ]
    )
    draw.text(
        (800, 150),
        encoding_list,
        font=text_font_bold,
        fill=colors["encoding_text"],
    )
    draw.text(
        (775, 150 + text_size * 6 + 20),
        "《通用规范汉字表》",
        font=text_font_bold_small,
        fill=colors["encoding_text"],
    )
    draw.text(
        (775, 150 + text_size * 8 + 45),
        "《常用國字標準字體表》",
        font=text_font_tc_bold_small,
        fill=colors["encoding_text"],
    )
    draw.text(
        (775, 150 + text_size * 9 + 60),
        "《次常用國字標準字體表》",
        font=text_font_tc_bold_small,
        fill=colors["encoding_text"],
    )

    big5_display = info.big5_hex if not info.big5_details else f"{info.big5_hex}{info.big5_details}"
    result_lines = "\n".join(
        [
            info.ascii_hex,
            info.unicode_label,
            info.gb2312_hex,
            "",
            info.gb18030_hex,
            info.lcuscc_result,
            big5_display,
            info.csfcnc_index,
            info.csfltcnc_index,
            info.shift_jis_hex,
            info.euc_kr_hex,
        ]
    )
    draw.text((1325, 150), result_lines, font=text_font, fill=colors["result_text"])
    draw.text(
        (1300, 150 + text_size * 3 - 5),
        info.gb2312_details,
        font=text_font_small,
        fill=colors["result_text"],
    )

    return image


def determine_output_path(config: Mapping[str, Any], character: str) -> Path:
    """Compute the output path for the rendered image.

    Args:
        config: Parsed configuration dictionary.
        character: Character that may be used for dynamic file names.

    Returns:
        Absolute path where the image should be written.
    """
    output_config = config["output"]
    output_dir = PROJECT_ROOT / output_config["folder"]
    output_dir.mkdir(exist_ok=True)

    file_name = output_config["file_name"]
    if output_config["input_char_file_name"]:
        if "." in file_name:
            suffix = file_name.split(".", maxsplit=1)[1]
            file_name = f"{character}.{suffix}"
        else:
            file_name = f"{character}_{file_name}"
    return output_dir / file_name


def main() -> None:
    """CLI entry point for generating the encoding summary image."""
    if not CONFIG_PATH.exists():
        print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
        sys.exit(1)

    config = load_config(CONFIG_PATH)
    character = prompt_for_character()
    info = build_character_info(character)
    image = create_encoding_image(info, config)
    output_path = determine_output_path(config, info.character)
    with open(output_path, "wb") as file:
        image.save(file)


if __name__ == "__main__":
    main()
