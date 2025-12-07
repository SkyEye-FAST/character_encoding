# Character Encoding Lookup

This project queries the encodings (or catalog numbers) associated with a single character.

## Supported Encodings

The tool currently reports data for the following character sets and encodings:

- ASCII
- Unicode
- GB/T 2312 *Code of Chinese graphic character set for information interchange - Primary set* (信息交换用汉字编码字符集 基本集)
- GB 18030 *Information technology — Chinese coded character set* (信息技术 中文编码字符集)
- *List of Commonly Used Standard Chinese Characters* (通用规范汉字表)
- Big5
- *Chart of Standard Forms of Common National Characters* (常用國字標準字體表)
- *Chart of Standard Forms of Less-Than-Common National Characters* (次常用國字標準字體表)
- Shift JIS
- EUC-KR

## Installation

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv)

### Setup

1. **Clone the repository:**

    ``` bash
    git clone https://github.com/SkyEye-FAST/character_encoding.git
    cd mcbe-chinese-patch
    ```

2. **Create a virtual environment and install dependencies:**

    ``` bash
    uv venv
    uv sync
    ```

    This will create a virtual environment in the `.venv` directory and install the required packages listed in `pyproject.toml`.

3. **Activate the virtual environment:**

    - **Windows (PowerShell):**

        ``` powershell
        .venv\Scripts\Activate.ps1
        ```

    - **macOS/Linux:**

        ``` bash
        source .venv/bin/activate
        ```

## Usage

### Command-Line Query

`get_encoding.py` is the base script that prints the query result to the terminal.

When you run the script it prompts for a single character; provide exactly one glyph to continue.

**Example output:**

```text
ASCII：未收录
Unicode: U+9AD1

GB/T 2312：0xF7C7
（87区39位，第二级汉字）
GB 18030：0xF7C7
《通用规范汉字表》: 6472（二级字）

Big5：0xC5EA（常用汉字）
《常用國字標準字體表》: 未收录
《次常用國字標準字體表》: 5880

Shift JIS：0xE991

EUC-KR：未收录
```

### Image Generation

`output_image.py` renders the query result as an image and imports `get_encoding.py` to reuse the core logic.

Images are saved to the `output` folder located next to the scripts by default.

> [!IMPORTANT]
> Place the configuration file `configuration.toml` beside the scripts.
>
> Store the font files under the `fonts` directory next to the scripts.

The layout uses fonts from [Source Han Serif](https://github.com/adobe-fonts/source-han-serif), [TH-Tshyn](http://cheonhyeong.com/Simplified/download.html), and [Apple Color Emoji for Linux](https://github.com/samuelngs/apple-emoji-linux).

**Example output:**

![Sample](/sample/sample.png)
![Sample](/sample/sample.jpg)
![Sample](/sample/sample.webp)

## License

Source Han Serif and Apple Color Emoji for Linux are licensed under the SIL Open Font License, version 1.1.

The project is released under the [Apache 2.0 license](LICENSE).

``` text
  Copyright 2023-2025 SkyEye_FAST

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
```

## Feedback

Please feel free to raise issues for any problems encountered or feature suggestions.

Pull requests are welcome.
