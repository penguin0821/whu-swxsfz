# 字体：思源宋体子集

站点正文用 **思源宋体（Source Han Serif CN）** 的两个字重：Regular 与 SemiBold。为避免把十几 MB 的完整字体内联进单文件页面，这里只保留**站内实际用到的汉字子集**（各约 150 KB），由构建脚本 `reinject6.py` 自动维护。

## 目录里的文件

| 文件 | 说明 |
|------|------|
| `SHS-Regular.woff2` | Regular 字重子集（构建产物，可重新生成）。 |
| `SHS-SemiBold.woff2` | SemiBold 字重子集。 |
| `v5_font_reg.b64.txt` | Regular 子集的 base64，注入模板用（构建时自动重写）。 |
| `v5_font_sb.b64.txt` | SemiBold 子集的 base64。 |
| `charset_live.txt` | 全站当前用到的汉字清单（**单调递增**，构建时自动并入新字）。 |
| `charset.txt` / `charset2.txt` / `charset3.txt` | 历史字符集快照，留档对照。 |

## OTF 源文件不入库

完整 OTF 每个约 11.6 MB，为保持仓库轻量**不提交**。只有在**新增汉字、需要重新切子集**时才用得到它。

日常改文案（复用已有汉字）无需 OTF——`reinject6.py` 会直接复用现有 woff2 构建。一旦模板引入了子集里没有的新汉字（比如新成员名字、新论文标题里的生僻字），脚本会 WARNING 提示，此时需放入 OTF 重新构建，否则那个字会回退成系统字体、基线错位。

## 下载 OTF

思源宋体是 Adobe 的开源字体，遵循 SIL Open Font License 1.1。从官方 release 下载：

    https://github.com/adobe-fonts/source-han-serif/releases

选 **简体中文** 包（`09_SourceHanSerifCN.zip`），解压出 Regular 与 SemiBold 两个 OTF，放到本目录并**严格命名**为：

    fonts/SourceHanSerifCN-Regular.otf
    fonts/SourceHanSerifCN-SemiBold.otf

放好后 `python3 reinject6.py` 会自动重新子集化，并恢复硬断言式的字形守卫。这两个 OTF 已在 `.gitignore` 中忽略，不会被误提交。

## 手动重新子集化（排查用）

正常情况下不用手动执行，`reinject6.py` 会做。等价命令：

```bash
python3 -m fontTools.subset fonts/SourceHanSerifCN-Regular.otf \
  --text-file=fonts/charset_live.txt --flavor=woff2 --no-hinting \
  --output-file=fonts/SHS-Regular.woff2
# SemiBold 同理，换成 SourceHanSerifCN-SemiBold.otf / SHS-SemiBold.woff2
```

依赖：`pip install fonttools brotli`。

## 验收字体是否生效

headless 浏览器在 base64 内联字体下不可靠，必须用**真实 Chrome**，控制台执行：

```js
document.fonts.check('400 16px "Source Han Serif CN"', '某字')   // Regular
document.fonts.check('600 16px "Source Han Serif CN"', '某字')   // SemiBold
```

对新增/关键汉字逐一确认为 `true`。
