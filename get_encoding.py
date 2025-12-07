"""Utilities for gathering encoding information for a single character."""

import unicodedata as ud
from dataclasses import dataclass
from functools import cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
UNRECORDED_LABEL = "未收录"


@dataclass(frozen=True)
class CharacterEncodingInfo:
    """Structured collection of encoding-related metadata.

    Attributes:
        character: The queried character.
        ascii_hex: The ASCII hex representation or "未收录" if unavailable.
        unicode_label: The Unicode code point label, e.g., "U+0041".
        unicode_name: Official Unicode character name or a fallback label.
        gb2312_hex: The GB/T 2312 encoding in prefixed hex format.
        gb2312_details: Human-readable GB/T 2312 block description.
        gb18030_hex: The GB 18030 encoding in prefixed hex format.
        lcuscc_result: Entry number and level in the List of Commonly Used Standard Chinese
            Characters (通用规范汉字表).
        big5_hex: The Big5 encoding in prefixed hex format.
        big5_details: Big5 usage level annotation, if available.
        csfcnc_index: Entry in Chart of Standard Forms of Common National Characters
            (常用國字標準字體表).
        csfltcnc_index: Entry in Chart of Standard Forms of Less-Than-Common National
            Characters (次常用國字標準字體表).
        shift_jis_hex: The Shift JIS encoding in prefixed hex format.
        euc_kr_hex: The EUC-KR encoding in prefixed hex format.
    """

    character: str
    ascii_hex: str
    unicode_label: str
    unicode_name: str
    gb2312_hex: str
    gb2312_details: str
    gb18030_hex: str
    lcuscc_result: str
    big5_hex: str
    big5_details: str
    csfcnc_index: str
    csfltcnc_index: str
    shift_jis_hex: str
    euc_kr_hex: str


def prompt_for_character(prompt: str = "字符：") -> str:
    """Prompt the user until a single character is provided.

    Args:
        prompt: Input prompt shown to the user.

    Returns:
        A single-character string entered by the user.
    """
    while True:
        user_input = input(prompt).strip()
        if len(user_input) == 1:
            return user_input
        print("请输入单个字符。\n")


@cache
def load_table(file_name: str) -> tuple[str, ...]:
    """Load a newline-separated character table from the data directory.

    Args:
        file_name: Name of the file relative to the data folder.

    Returns:
        Tuple containing each stripped line from the file.
    """
    with open(DATA_DIR / file_name, encoding="utf-8") as file:
        return tuple(line.strip() for line in file)


def build_character_info(character: str) -> CharacterEncodingInfo:
    """Aggregate every table lookup and encoding for the provided character.

    Args:
        character: Character to analyze.

    Returns:
        Populated `CharacterEncodingInfo` instance.
    """
    ascii_hex_value = character.encode("ascii", errors="ignore").hex().upper()
    ascii_hex = ascii_hex_value or UNRECORDED_LABEL
    unicode_label = f"U+{ord(character):04X}"

    gb2312_raw = character.encode("gb2312", errors="ignore").hex()
    gb2312_hex = f"0x{gb2312_raw.upper()}" if gb2312_raw else UNRECORDED_LABEL
    if len(gb2312_raw) == 4:
        row = int(gb2312_raw[:2], 16) - 160
        column = int(gb2312_raw[2:], 16) - 160
        if 16 <= row <= 55:
            gb2312_level = "第一级汉字"
        elif 56 <= row <= 87:
            gb2312_level = "第二级汉字"
        else:
            gb2312_level = "非汉字"
        gb2312_details = f"\n（{row}区{column}位，{gb2312_level}）"
    else:
        gb2312_details = ""

    gb18030_raw = character.encode("gb18030", errors="ignore").hex()
    unicode_name = ud.name(character, "未知的Unicode名称")
    gb18030_hex = f"0x{gb18030_raw.upper()}" if gb18030_raw else UNRECORDED_LABEL

    big5_raw = character.encode("big5", errors="ignore").hex()
    big5_hex = f"0x{big5_raw.upper()}" if big5_raw else UNRECORDED_LABEL
    if big5_raw:
        big5_code_point = int(big5_raw, 16)
        if 0xA440 <= big5_code_point <= 0xC67E:
            big5_details = "（常用汉字）"
        elif 0xC940 <= big5_code_point <= 0xF9D5:
            big5_details = "（次常用汉字）"
        else:
            big5_details = ""
    else:
        big5_details = ""

    lcuscc_table = load_table("List of Commonly Used Standard Chinese Characters.txt")
    try:
        lcuscc_index = lcuscc_table.index(character) + 1
    except ValueError:
        lcuscc_result = UNRECORDED_LABEL
    else:
        if lcuscc_index <= 3500:
            lcuscc_level = "（一级字）"
        elif lcuscc_index <= 6500:
            lcuscc_level = "（二级字）"
        elif lcuscc_index <= 8105:
            lcuscc_level = "（三级字）"
        else:
            lcuscc_level = ""
        lcuscc_result = f"{str(lcuscc_index).zfill(4)}{lcuscc_level}"

    csfcnc_table = load_table("Chart of Standard Forms of Common National Characters.txt")
    csfcnc_index = next(
        (str(i + 1).zfill(5) for i, entry in enumerate(csfcnc_table) if entry == character),
        UNRECORDED_LABEL,
    )

    csfltcnc_table = load_table(
        "Chart of Standard Forms of Less-Than-Common National Characters.txt"
    )
    csfltcnc_index = next(
        (str(i + 1) for i, entry in enumerate(csfltcnc_table) if entry == character),
        UNRECORDED_LABEL,
    )

    shift_jis_raw = character.encode("shift_jis", errors="ignore").hex()
    shift_jis_hex = f"0x{shift_jis_raw.upper()}" if shift_jis_raw else UNRECORDED_LABEL

    euc_kr_raw = character.encode("euc_kr", errors="ignore").hex()
    euc_kr_hex = f"0x{euc_kr_raw.upper()}" if euc_kr_raw else UNRECORDED_LABEL

    return CharacterEncodingInfo(
        character,
        ascii_hex,
        unicode_label,
        unicode_name,
        gb2312_hex,
        gb2312_details,
        gb18030_hex,
        lcuscc_result,
        big5_hex,
        big5_details,
        csfcnc_index,
        csfltcnc_index,
        shift_jis_hex,
        euc_kr_hex,
    )


def display_report(info: CharacterEncodingInfo) -> None:
    """Print a human-readable encoding summary to stdout.

    Args:
        info: Aggregated encoding information to show.
    """
    print(f"\nASCII：{info.ascii_hex}")
    print(f"Unicode: {info.unicode_label}")
    print(f"{info.unicode_name}\n")
    print(f"GB/T 2312：{info.gb2312_hex}{info.gb2312_details}")
    print(f"GB 18030：{info.gb18030_hex}")
    print(f"《通用规范汉字表》: {info.lcuscc_result}\n")
    print(f"Big5：{info.big5_hex}{info.big5_details}")
    print(f"《常用國字標準字體表》: {info.csfcnc_index}")
    print(f"《次常用國字標準字體表》: {info.csfltcnc_index}\n")
    print(f"Shift JIS：{info.shift_jis_hex}\n")
    print(f"EUC-KR：{info.euc_kr_hex}")


def main() -> None:
    """Entry point for interactive CLI usage."""
    character = prompt_for_character()
    info = build_character_info(character)
    display_report(info)


if __name__ == "__main__":
    main()
