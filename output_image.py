# -*- coding: UTF-8 -*-

import os
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from get_encoding import (
    character,
    output_ascii,
    output_unicode,
    output_gb2312,
    output_gb2312_2,
    output_gb18030,
    output_tygf,
    output_big5,
    changyong_num,
    cichangyong_num,
    output_shift_jis,
    output_euc_kr,
)

# 当前绝对路径
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")

# 字体文件路径
FONT_PATH = os.path.join(P, "fonts")

# 创建空白图片
image = Image.new("RGB", (1920, 1080), (249, 242, 224))
draw = ImageDraw.Draw(image)

# 添加标题
title = "字符编码查询"
title_position = (150, 165)
title_font = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"), 85
)
title_bbox = list(title_font.getbbox(title))
title_box_position = [
    title_bbox[0] + title_position[0] - 50,
    title_bbox[1] + title_position[1] - 50,
    title_bbox[2] + title_position[0] + 50,
    title_bbox[3] + title_position[1] + 50,
]
draw.rounded_rectangle(
    title_box_position,
    fill="#2bae85",
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
    fill="#b9dec9",
    radius=25,
    corners=(False, False, True, True),
)
draw.text(title_position, title, font=title_font, fill="white")

# 字体
text_size = 54
text_font = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifSC-Regular.otf"), text_size
)
text_font_small = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifSC-Regular.otf"), text_size - 10
)
text_font_bold = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"), text_size
)
text_font_bold_small = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"), text_size - 10
)
text_font_tc_bold_small = ImageFont.truetype(
    os.path.join(FONT_PATH, "SourceHanSerifTC-Bold.otf"), text_size - 10
)

# 查询的字符
font = TTFont(os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"))
unicode_map = font["cmap"].tables[0].ttFont.getBestCmap()
if "CJK" in unicodedata.name(character):
    if ord(character) in unicode_map.keys():
        character_font = ImageFont.truetype(
            os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"), 350
        )
    else:
        character_font = ImageFont.truetype(
            os.path.join(FONT_PATH, "BabelStoneHan.ttf"), 350
        )
else:
    character_font = ImageFont.truetype(
        os.path.join(FONT_PATH, "SourceHanSerifSC-Bold.otf"), 350
    )

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
draw.rectangle(character_box_position, outline="#2376b7", width=5)
# 字符
character_position = (character_box_position[0], character_box_position[1] - character_bbox[1])
draw.text(character_position, character, font=character_font, fill="black")

# 查询的结果
encoding_list_1 = "\n".join(
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
draw.text((800, 150), encoding_list_1, font=text_font_bold, fill="black")
draw.text(
    (775, 150 + text_size * 6 + 20),
    "《通用规范汉字表》",
    font=text_font_bold_small,
    fill="black",
)
draw.text(
    (775, 150 + text_size * 8 + 45),
    "《常用國字標準字體表》",
    font=text_font_tc_bold_small,
    fill="black",
)
draw.text(
    (775, 150 + text_size * 9 + 60),
    "《次常用國字標準字體表》",
    font=text_font_tc_bold_small,
    fill="black",
)

output_1 = "\n".join(
    [
        output_ascii,
        output_unicode,
        output_gb2312,
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
output_2 = output_gb2312_2
draw.text((1325, 150), output_1, font=text_font, fill="black")
draw.text((1300, 150 + text_size * 3 - 5), output_2, font=text_font_small, fill="black")

# 保存图片
with open(os.path.join(P, "output.png"), "wb") as f:
    image.save(f)
