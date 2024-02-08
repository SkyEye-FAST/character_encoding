# 字符编码查询

[![Pylint](https://github.com/SkyEye-FAST/character_encoding/actions/workflows/pylint.yml/badge.svg)](https://github.com/SkyEye-FAST/character_encoding/actions/workflows/pylint.yml)

此项目用于查询某个字符的编码（或编号）。

## 需求

由于使用了标准库`tomllib`，所以需要**Python >= 3.11**。

``` shell
pip install -r requirements.txt
```

## 支持

目前支持的字符集和编码有：

- ASCII
- Unicode
- GB/T 2312《信息交换用汉字编码字符集　基本集》
- GB 18030《信息技术　中文编码字符集》
- 《通用规范汉字表》
- 大五码（Big5）
- 《常用國字標準字體表》
- 《次常用國字標準字體表》
- Shift JIS
- EUC-KR

## 脚本使用

### 命令行查询

`get_encoding.py`为基础脚本，在命令行中输出查询结果。

脚本运行后会提示输入单个字符，若不满足则需重新输入。

输出结果示例如下：

``` text
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

### 生成图片

`output_image.py`用于生成含有查询结果的图片，需要引入`get_encoding.py`来获取结果。

配置文件名为`configuration.toml`，位置与脚本同级。

输出图片位置默认为脚本同级目录下的`output`文件夹中。

图片使用字体为[思源宋体](https://github.com/adobe-fonts/source-han-serif)、[天珩全字库](http://cheonhyeong.com/Simplified/download.html)和[Apple Color Emoji for Linux](https://github.com/samuelngs/apple-emoji-linux)，需要存放在脚本同级目录下的`fonts`文件夹中。

生成图片样式如图所示：
![Sample](/sample/sample.png)
![Sample](/sample/sample.jpg)
![Sample](/sample/sample.webp)

## 反馈

遇到的问题和功能建议等可以提出议题（Issue）。

欢迎创建拉取请求（Pull request）。
