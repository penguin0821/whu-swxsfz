# 涉外刑事风险治理与合规中心 · 官网源码

武汉大学涉外法治学院 **涉外刑事风险治理与合规中心**（Center for Foreign-Related Criminal Risk Governance and Compliance）单页官网的完整源码、构建脚本、素材与开发文档。

在线预览：https://penguin0821.github.io/whu-swxsfz/

## 这是一个什么样的项目

一个**零依赖、单文件**的静态网站。整站最终产物就是一个 `index.html`（约 1.35 MB），所有图片、字体、脚本都以 base64 内联其中，不依赖任何外部 CSS/JS/CDN，双击即可离线打开，也能直接丢到任意静态托管上。

技术栈是原生 HTML + CSS + JavaScript，首屏的镂空地球用 Canvas 2D 逐帧绘制，没有前端框架、没有打包器。唯一的"构建"是一个 Python 脚本，负责把字体和二进制素材注入模板。

## 快速开始

```bash
# 1. 安装构建依赖（仅重新子集化字体时需要；纯改文案可跳过）
pip install fonttools brotli

# 2. 改内容：只编辑模板，不要直接改 index.html
#    文案 / 成员 / 成果 / 新闻都在 demo6_template.html 的数据区
vim demo6_template.html

# 3. 构建：生成根目录 index.html（会自动同步字体子集并做字形守卫）
python3 reinject6.py

# 4. 本地预览
open index.html            # macOS
# 或起个本地服务器：python3 -m http.server 8000 然后访问 http://localhost:8000
```

构建完成后，把 `index.html` 部署到 GitHub Pages 即可（见 `deploy/`）。

## 仓库结构

| 路径 | 用途 |
|------|------|
| `index.html` | **构建产物 / 线上文件**，GitHub Pages 从仓库根目录读取它。不要手改。 |
| `demo6_template.html` | **唯一真源**。所有文案、数据、样式、脚本都在这里，含 `{{...}}` 资源占位符。 |
| `reinject6.py` | 构建脚本：字体自同步 + 资源注入 + 字形守卫，输出 `index.html`。 |
| `assets/` | base64 素材（logo、浮岛、枝干、地球陆地掩膜、导师照片）与源图。 |
| `fonts/` | 思源宋体子集 woff2、字符集清单、字体 base64。OTF 源文件不入库，见 `fonts/README.md`。 |
| `docs/` | 开发使用手册、CMS 与演进路线、成果清单（含来源核实）。 |
| `deploy/` | GitHub Pages 部署脚本与说明。 |
| `tools/` | 一次性的素材生成 / 审计脚本，保留备查。 |
| `legacy/` | 冻结的 v1–v5 历史模板与构建脚本，仅作演进记录，勿用于生产。 |
| `audit/` | 排版走查脚本 `audit.js`。 |

## 改内容去哪里改

全部在 `demo6_template.html` 的 `/* ---------- data ---------- */` 区块：

- `UI = { zh:{...}, en:{...} }` — 全站双语文案（导航、标题、按钮、提示）。
- `DIRS` — 研究方向卡片。
- `SUP` — 导师（敬力嘉）档案，含简介、荣誉、代表成果。
- `MEM` — 中心成员名单（博士生 / 硕士生 / 校友，按入学年份分组）。
- `PUBS` — 研究成果（`papers` / `projects` / `forums` / `books`）。
- `NEWS` — 新闻动态（可选 `url` 字段渲染"原文链接"胶囊）。

改完必须重新 `python3 reinject6.py`，否则 `index.html` 不会更新。**切勿直接编辑 `index.html`**——它是产物，下次构建会被覆盖。

## 字体

站点正文用思源宋体（Source Han Serif CN）的两个字重子集，只包含站内实际用到的汉字，base64 内联。完整 OTF 源文件（约 23 MB）不入库；需要新增生僻字时按 `fonts/README.md` 下载后重新子集化。思源宋体遵循 SIL Open Font License 1.1。

## 许可

网站代码与内容 © 武汉大学涉外法治学院 涉外刑事风险治理与合规中心。内联字体思源宋体遵循 [SIL OFL 1.1](https://openfontlicense.org/)。
