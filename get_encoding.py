# -*- coding: UTF-8 -*-
"""字符编码获取工具"""

import os

# 当前绝对路径
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")


def load_table(file_path):
    """读取以文本文件存储的字符表"""
    with open(os.path.join(P, "table", file_path), "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def get(char: str, encoding: str):
    """获取编码"""
    return char.encode(encoding, errors="ignore").hex()


def to_hex(n:str):
    """将16进制编码转为0xXXXX格式"""
    return f"0x{n.upper()}" if n else "未收录"


# 输入
while True:
    character = input("字符：")
    if len(character) == 1:
        break
    print("请输入单个字符。\n")

# ASCII编码
OUTPUT_ASCII = get(character, "ascii").upper() or "未收录"
print(f"\nASCII：{OUTPUT_ASCII}")
# Unicode编码
OUTPUT_UNICODE = f"U+{format(ord(character), '04X')}"
print(f"Unicode: {OUTPUT_UNICODE}\n")

gb2312 = get(character, "gb2312")  # 获取GB2312编码
OUTPUT_GB2312 = to_hex(gb2312)
# GB2312分级
if len(gb2312) == 4:
    gb2312_row = int(gb2312[:2], 16) - 160
    if 16 <= gb2312_row <= 55:
        GB2312_LEVEL = "第一级汉字"
    elif 56 <= gb2312_row <= 87:
        GB2312_LEVEL = "第二级汉字"
    else:
        GB2312_LEVEL = "非汉字"
    OUTPUT_GB2312_2 = f"\n（{gb2312_row}区{int(gb2312[2:], 16) - 160}位，{GB2312_LEVEL}）"
else:
    OUTPUT_GB2312_2 = ""
print(f"GB/T 2312：{OUTPUT_GB2312}{OUTPUT_GB2312_2}")  # 输入GB2312编码
output_gb18030 = to_hex(get(character, "gb18030"))
print(f"GB 18030：{output_gb18030}")  # GB 18030编码

tygf = load_table("tongyong_guifan.txt")  # 读取《通用规范汉字表》
# 查找编号并分级
TYGF_NUM = next((i + 1 for i, element in enumerate(tygf) if element == character), 0)
if TYGF_NUM > 0:
    if TYGF_NUM <= 3500:
        TYGF_LEVEL = "（一级字）"
    elif TYGF_NUM <= 6500:
        TYGF_LEVEL = "（二级字）"
    elif TYGF_NUM <= 8105:
        TYGF_LEVEL = "（三级字）"
    TYGF_NUM = str(TYGF_NUM).zfill(4)
else:
    TYGF_NUM = "未收录"
    TYGF_LEVEL = ""
# 输出
output_tygf = TYGF_NUM + TYGF_LEVEL
print(f"《通用规范汉字表》: {output_tygf}\n")

BIG5 = get(character, "big5")  # 大五码
# 大五码分级
if BIG5:
    if 0xA440 <= int(BIG5, 16) <= 0xC67E:
        BIG5_LEVEL = "（常用汉字）"
    elif 0xC940 <= int(BIG5, 16) <= 0xF9D5:
        BIG5_LEVEL = "（次常用汉字）"
    else:
        BIG5_LEVEL = ""
else:
    BIG5 = "未收录"
    BIG5_LEVEL = ""
output_big5 = to_hex(get(character, "big5")) + BIG5_LEVEL
print(f"Big5：{output_big5}")  # 输出
changyong = load_table("changyong_guozi.txt")  # 读取《常用國字標準字體表》
changyong_num = next(
    (
        str(i + 1).zfill(5)
        for i, element in enumerate(changyong)
        if element == character
    ),
    "未收录",
)  # 查找编号
print(f"《常用國字標準字體表》: {changyong_num}")  # 输出
cichangyong = load_table("cichangyong_guozi.txt")  # 读取《次常用國字標準字體表》
cichangyong_num = next(
    (str(i + 1) for i, element in enumerate(cichangyong) if element == character),
    "未收录",
)  # 查找编号
print(f"《次常用國字標準字體表》: {cichangyong_num}\n")  # 输出

# Shift JIS
output_shift_jis = to_hex(get(character, "shift_jis"))
print(f"Shift JIS：{output_shift_jis}\n")

# EUC-KR
output_euc_kr = to_hex(get(character, "euc_kr"))
print(f"EUC-KR：{output_euc_kr}")
