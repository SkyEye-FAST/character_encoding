# -*- coding: UTF-8 -*-

import os

P = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + os.path.sep
)  # 当前绝对路径


# 读取以文本文件存储的字符表
def load_table(file_path):
    with open(P + "table" + os.path.sep + file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


# 获取编码
get = lambda char, encoding: char.encode(encoding, errors="ignore").hex()

# 将16进制编码转为0xXXXX格式
to_hex = lambda n: f"0x{n.upper()}" if n else "未收录"

# 输入
while True:
    character = input("字符：")
    if len(character) == 1:
        break
    print("请输入单个字符。\n")

# ASCII编码
output_ascii = get(character, "ascii").upper() or "未收录"
print(f"\nASCII：{output_ascii}")
# Unicode编码
output_unicode = f"U+{format(ord(character), '04X')}"
print(f"Unicode: {output_unicode}\n")

gb2312 = get(character, "gb2312")  # 获取GB2312编码
output_gb2312 = to_hex(gb2312)
# GB2312分级
if len(gb2312) == 4:
    gb2312_row = int(gb2312[:2], 16) - 160
    if 16 <= gb2312_row <= 55:
        gb2312_level = "第一级汉字"
    elif 56 <= gb2312_row <= 87:
        gb2312_level = "第二级汉字"
    else:
        gb2312_level = "非汉字"
    output_gb2312_2 = f"\n（{gb2312_row}区{int(gb2312[2:], 16) - 160}位，{gb2312_level}）"
else:
    output_gb2312_2 = ""
print(f"GB/T 2312：{output_gb2312}{output_gb2312_2}")  # 输入GB2312编码
output_gb18030 = to_hex(get(character, "gb18030"))
print(f"GB 18030：{output_gb18030}")  # GB 18030编码

tygf = load_table("tongyong_guifan.txt")  # 读取《通用规范汉字表》
# 查找编号并分级
tygf_num = next((i + 1 for i, element in enumerate(tygf) if element == character), 0)
if tygf_num > 0:
    if tygf_num <= 3500:
        tygf_level = "（一级字）"
    elif tygf_num <= 6500:
        tygf_level = "（二级字）"
    elif tygf_num <= 8105:
        tygf_level = "（三级字）"
    tygf_num = str(tygf_num).zfill(4)
else:
    tygf_num = "未收录"
    tygf_level = ""
# 输出
output_tygf = tygf_num + tygf_level
print(f"《通用规范汉字表》: {output_tygf}\n")

big5 = get(character, "big5")  # 大五码
# 大五码分级
if big5:
    if 0xA440 <= int(big5, 16) <= 0xC67E:
        big5_level = "（常用汉字）"
    elif 0xC940 <= int(big5, 16) <= 0xF9D5:
        big5_level = "（次常用汉字）"
    else:
        big5_level = ""
else:
    big5 = "未收录"
    big5_level = ""
output_big5 = to_hex(get(character, "big5")) + big5_level
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
