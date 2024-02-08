# -*- coding: UTF-8 -*-
"""生成字符编码信息图片工具"""

import sys
import tomllib as tl
from pathlib import Path
import unicodedata2 as ud
import emoji
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from get_encoding import (
    character,
    OUTPUT_ASCII,
    OUTPUT_UNICODE,
    OUTPUT_GB2312,
    OUTPUT_GB2312_2,
    output_gb18030,
    output_tygf,
    output_big5,
    changyong_num,
    cichangyong_num,
    output_shift_jis,
    output_euc_kr,
)

# 当前绝对路径
P = Path(__file__).resolve().parent
# 加载配置
CONFIG_DIR = P / "configuration.toml"
if not CONFIG_DIR.exists():
    print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
    sys.exit()
with open(CONFIG_DIR, "rb") as f:
    config = tl.load(f)

background_color = config["color"]["background"]  # 背景颜色
title_box_color = config["color"]["title_box"]  # 标题框颜色
title_color = config["color"]["title"]  # 标题颜色
character_color = config["color"]["character"]  # 查询字符的颜色
character_outline_color = config["color"]["character_outline"]  # 查询字符外框线的颜色
encoding_text_color = config["color"]["encoding_text"]  # 编码（表格第一列）文字颜色
result_text_color = config["color"]["result_text"]  # 查询结果（表格第二列）文字颜色
unicode_name_color = config["color"]["unicode_name"]  # 查询字符Unicode名的颜色

font_folder = config["input"]["font_folder"]  # 字体文件夹
table_folder = config["input"]["table_folder"]  # 编码表文件夹

file_name = config["output"]["file_name"]  # 输出文件名
output_folder = config["output"]["folder"]  # 输出文件夹

# 字体文件路径
FONT_DIR = P / font_folder


def load_font(file: str, size: int):
    """加载字体"""
    return ImageFont.truetype(FONT_DIR / file, size)


# 创建空白图片
image = Image.new("RGB", [1920, 1080], background_color)
draw = ImageDraw.Draw(image)

# 添加标题
TITLE = "字符编码查询"
title_position = [150, 150]
title_font = load_font("SourceHanSerifSC-Bold.otf", 85)
title_bbox = list(title_font.getbbox(TITLE))
title_box_position = [
    title_bbox[0] + title_position[0] - 50,
    title_bbox[1] + title_position[1] - 50,
    title_bbox[2] + title_position[0] + 50,
    title_bbox[3] + title_position[1] + 50,
]
draw.rounded_rectangle(
    title_box_position,
    fill=title_box_color[0],
    radius=25,
    corners=(True, True, False, False),
)
title_box_position_2 = [
    title_box_position[0],
    title_box_position[3],
    title_box_position[2],
    title_box_position[3] + 600,
]
draw.rounded_rectangle(
    title_box_position_2,
    fill=title_box_color[1],
    radius=25,
    corners=(False, False, True, True),
)
draw.text(title_position, TITLE, font=title_font, fill=title_color)

# 字体
TEXT_SIZE = 54
text_font = load_font("SourceHanSerifSC-Regular.otf", TEXT_SIZE)
text_font_small = load_font("SourceHanSerifSC-Regular.otf", TEXT_SIZE - 10)
text_font_tiny = load_font("SourceHanSerifSC-Regular.otf", 28)
text_font_bold = load_font("SourceHanSerifSC-Bold.otf", TEXT_SIZE)
text_font_bold_small = load_font("SourceHanSerifSC-Bold.otf", TEXT_SIZE - 10)
text_font_tc_bold_small = load_font("SourceHanSerifTC-Bold.otf", TEXT_SIZE - 10)


# 查询的字符
def valid(t, file):
    """字符在字体中是否有效"""
    return (
        ord(t)
        in TTFont(FONT_DIR / file)["cmap"]
        .tables[0]
        .ttFont.getBestCmap()
        .keys()
    )


if emoji.purely_emoji(character):
    character_font = load_font("AppleColorEmoji.ttf", 137)
elif valid(character, "SourceHanSerifSC-Bold.otf"):
    character_font = load_font("SourceHanSerifSC-Bold.otf", 350)
elif valid(character, "TH-Tshyn-P0.ttf"):
    character_font = load_font("TH-Tshyn-P0.ttf", 350)
elif valid(character, "TH-Tshyn-P1.ttf"):
    character_font = load_font("TH-Tshyn-P1.ttf", 350)
elif valid(character, "TH-Tshyn-P2.ttf"):
    character_font = load_font("TH-Tshyn-P2.ttf", 350)
else:
    character_font = load_font("TH-Tshyn-P16.ttf", 350)

# 字符位置
title_box_2_width = title_box_position_2[2] - title_box_position_2[0]
title_box_2_height = title_box_position_2[3] - title_box_position_2[1]
character_bbox = list(character_font.getbbox(character))
character_width = character_bbox[2] - character_bbox[0]
character_height = character_bbox[3] - character_bbox[1]
character_box_position = [
    title_box_position_2[0] + title_box_2_width / 2 - character_width / 2,
    title_box_position_2[1] + title_box_2_height / 2 - character_height / 2,
    title_box_position_2[0] + title_box_2_width / 2 + character_width / 2,
    title_box_position_2[1] + title_box_2_height / 2 + character_height / 2,
]
# 字符外框线
draw.rectangle(character_box_position, outline=character_outline_color, width=5)
# 字符
character_position = (
    character_box_position[0],
    character_box_position[1] - character_bbox[1],
)
draw.text(
    character_position,
    character,
    font=character_font,
    fill=character_color,
    embedded_color=emoji.purely_emoji(character),
)
# 字符的Unicode名
unicode_name_position = [title_box_position[0], title_box_position[3] + 625]
draw.text(
    unicode_name_position,
    ud.name(character),
    font=text_font_tiny,
    fill=unicode_name_color,
)

# 查询的结果
ENCODING_LIST = "\n".join(
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
draw.text((800, 150), ENCODING_LIST, font=text_font_bold, fill=encoding_text_color)
draw.text(
    (775, 150 + TEXT_SIZE * 6 + 20),
    "《通用规范汉字表》",
    font=text_font_bold_small,
    fill=encoding_text_color,
)
draw.text(
    (775, 150 + TEXT_SIZE * 8 + 45),
    "《常用國字標準字體表》",
    font=text_font_tc_bold_small,
    fill=encoding_text_color,
)
draw.text(
    (775, 150 + TEXT_SIZE * 9 + 60),
    "《次常用國字標準字體表》",
    font=text_font_tc_bold_small,
    fill=encoding_text_color,
)

OUTPUT_1 = "\n".join(
    [
        OUTPUT_ASCII,
        OUTPUT_UNICODE,
        OUTPUT_GB2312,
        "",
        output_gb18030,
        output_tygf,
        output_big5,
        changyong_num,
        cichangyong_num,
        output_shift_jis,
        output_euc_kr,
    ]
)
draw.text((1325, 150), OUTPUT_1, font=text_font, fill=result_text_color)
draw.text(
    (1300, 150 + TEXT_SIZE * 3 - 5),
    OUTPUT_GB2312_2,
    font=text_font_small,
    fill=result_text_color,
)

# 保存图片
OUTPUT_DIR = P / output_folder
OUTPUT_DIR.mkdir(exist_ok=True)  # 创建输出文件夹（若不存在）
with open(OUTPUT_DIR / file_name, "wb") as f:
    image.save(f)
