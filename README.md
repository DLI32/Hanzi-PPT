# Hanzi-PPT
Hanzi-PPT 汉字笔画 PPT 生成器

Generate animated Chinese stroke-order PowerPoint decks in seconds — built for language teachers and learners.

What is Hanzi-PPT?
Hanzi-PPT takes a list of Chinese characters or vocabulary words and produces a ready-to-use PowerPoint presentation (.pptx) where each character is accompanied by its stroke-order animation GIF. No design skills required — just paste your word list and get a classroom-ready deck.
Designed by a Chinese language teacher, for Chinese language teachers.

✨ Features

Stroke animation GIFs — powered by hanzi-writer data, covering 9,000+ simplified and traditional characters
Auto-generated PPTX — one slide per character, with animation embedded and ready to present
Desktop GUI — clean Electron-based interface, no command line needed for everyday use
CLI support — scriptable via command line for batch generation and automation workflows
Cross-platform builds — Windows, macOS, and Linux via GitHub Actions
Offline-first — no internet required after installation; all stroke data is bundled locally


📸 Screenshots

(Screenshots coming soon — contributions welcome!)

GUI ModeGenerated Slide ExampleShow ImageShow Image

🚀 Quick Start
Option A: Download the Desktop App (Recommended)

Go to Releases
Download the installer for your platform (.exe for Windows)
Run the installer and launch Hanzi-PPT
Enter your character list → click Generate → save your .pptx

Option B: Run from Source
Prerequisites: Node.js ≥ 18, Python ≥ 3.9
bash# Clone the repository
git clone https://github.com/DLI32/Hanzi-PPT.git
cd Hanzi-PPT/hanzi-ppt\ 2

# Install dependencies
npm install
pip install -r requirements.txt

# Launch the GUI
npm start

# Or use the CLI
python cli.py --chars "你好世界" --output my_deck.pptx

🖥️ CLI Usage
python cli.py [OPTIONS]

Options:
  --chars TEXT        Characters or words to include (e.g. "你好世界")
  --wordlist FILE     Path to a .txt file with one character/word per line
  --output FILE       Output .pptx filename (default: hanzi_output.pptx)
  --title TEXT        Presentation title shown on the cover slide
  --help              Show this message and exit

Examples:
  python cli.py --chars "学生老师汉字"
  python cli.py --wordlist vocab.txt --output lesson3.pptx --title "第三课生词"

🛠️ Tech Stack
LayerTechnologyDesktop GUIElectronStroke data & animationhanzi-writerGIF generationPython (Pillow / imageio)PPTX generationpptxgenjsCI/CDGitHub Actions (cross-platform matrix build)RuntimeNode.js + Python

📁 Project Structure
Hanzi-PPT/
└── hanzi-ppt 2/
    ├── main.js          # Electron main process
    ├── renderer/        # Electron renderer (UI)
    ├── cli.py           # Command-line entry point
    ├── gif_gen.py       # Stroke GIF generation (Python)
    ├── ppt_builder.js   # PPTX assembly (pptxgenjs)
    └── data/            # Bundled hanzi-writer stroke data

🗺️ Roadmap

 macOS and Linux GUI installers
 Pinyin annotation on slides
 Word meaning / English gloss support
 Custom slide themes and color schemes
 Bulk import from CSV / Anki deck format
 Web-based version (no install required)


🤝 Contributing
Contributions are welcome! Here's how to get started:

Fork the repo and create a feature branch
Make your changes and test locally
Submit a pull request with a clear description

If you find a bug or have a feature request, please open an issue.

📄 License
This project is open source. See LICENSE for details.

🙏 Acknowledgements

hanzi-writer by David Chanin — stroke order data and animation engine
pptxgenjs by Brent Ely — PowerPoint generation library
Built with ❤️ for Chinese language classrooms


Made by a language teacher who got tired of making stroke-order slides by hand.

# Hanzi-PPT 汉字笔画 PPT 生成器

> 输入词表，一键生成带笔画动画的汉字 PPT 课件 —— 专为汉语教师和学习者打造。

## 这是什么？

**Hanzi-PPT** 接收一组汉字或词语，自动生成一份 PowerPoint 演示文稿（.pptx），每个汉字独占一张幻灯片，并内嵌笔顺动画 GIF，打开即可课堂使用。

由汉语教师亲手开发，为汉语教师量身设计。


## ✨ 功能特性

- **笔顺动画 GIF** — 基于 [hanzi-writer](https://hanziwriter.org/) 笔画数据，覆盖 9000+ 简繁体常用汉字
- **自动生成 PPTX** — 每字一页，动画 GIF 直接嵌入，开箱即用
- **桌面 GUI 界面** — 基于 Electron 的图形界面，普通用户无需接触命令行
- **CLI 命令行支持** — 支持脚本化调用，方便批量生成与自动化工作流
- **跨平台构建** — 通过 GitHub Actions 支持 Windows、macOS、Linux
- **完全离线运行** — 安装后无需联网，笔画数据全部本地打包

---

## 📸 截图预览

> *(截图即将上线，欢迎贡献！)*

| GUI 界面 | 生成的幻灯片示例 |
|---|---|
| ![GUI 截图占位](docs/screenshots/gui-placeholder.png) | ![幻灯片示例占位](docs/screenshots/slide-placeholder.png) |

---

## 🚀 快速开始

### 方式一：下载桌面客户端（推荐）

1. 前往 [Releases 页面](https://github.com/DLI32/Hanzi-PPT/releases)
2. 下载对应平台的安装包（Windows 用 `.exe`）
3. 安装并启动 **Hanzi-PPT**
4. 输入汉字列表 → 点击**生成** → 保存 `.pptx` 文件

### 方式二：从源码运行

**环境要求：** Node.js ≥ 18，Python ≥ 3.9

```bash
# 克隆仓库
git clone https://github.com/DLI32/Hanzi-PPT.git
cd "Hanzi-PPT/hanzi-ppt 2"

# 安装依赖
npm install
pip install -r requirements.txt

# 启动 GUI
npm start

# 或使用命令行
python cli.py --chars "你好世界" --output 我的课件.pptx
```

---

## 🖥️ 命令行用法

```
python cli.py [选项]

选项：
  --chars TEXT        要处理的汉字或词语（如 "你好世界"）
  --wordlist FILE     词表文件路径，每行一个字/词（.txt 格式）
  --output FILE       输出文件名（默认：hanzi_output.pptx）
  --title TEXT        封面页标题
  --help              显示帮助信息

示例：
  python cli.py --chars "学生老师汉字"
  python cli.py --wordlist 词表.txt --output 第三课.pptx --title "第三课生词"
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|---|---|
| 桌面 GUI | [Electron](https://www.electronjs.org/) |
| 笔画数据与动画 | [hanzi-writer](https://hanziwriter.org/) |
| GIF 生成 | Python（Pillow / imageio） |
| PPTX 生成 | [pptxgenjs](https://gitbrent.github.io/PptxGenJS/) |
| CI/CD | GitHub Actions（跨平台矩阵构建） |
| 运行环境 | Node.js + Python |

---

## 📁 项目结构

```
Hanzi-PPT/
└── hanzi-ppt 2/
    ├── main.js          # Electron 主进程
    ├── renderer/        # Electron 渲染层（UI）
    ├── cli.py           # 命令行入口
    ├── gif_gen.py       # 笔画 GIF 生成（Python）
    ├── ppt_builder.js   # PPTX 组装（pptxgenjs）
    └── data/            # 本地笔画数据（hanzi-writer）
```

---

## 🗺️ 开发计划

- [ ] macOS 和 Linux GUI 安装包
- [ ] 幻灯片上显示拼音标注
- [ ] 支持词义 / 英文释义
- [ ] 自定义幻灯片主题与配色
- [ ] 支持 CSV / Anki 格式批量导入
- [ ] 网页版（无需安装）

---

## 🤝 参与贡献

欢迎提交 PR 或 Issue！

1. Fork 本仓库，创建功能分支
2. 完成修改并在本地测试
3. 提交 Pull Request，附上清晰的改动说明

有 Bug 或功能建议？请[提交 Issue](https://github.com/DLI32/Hanzi-PPT/issues)。

---

## 📄 开源协议

本项目为开源软件，详见 [LICENSE](LICENSE)。

---

## 🙏 致谢

- [hanzi-writer](https://hanziwriter.org/)（David Chanin）— 笔画数据与动画引擎
- [pptxgenjs](https://gitbrent.github.io/PptxGenJS/)（Brent Ely）— PowerPoint 生成库
- 用 ❤️ 为汉语课堂而造

---

*因为厌倦了手动做笔顺课件，所以写了这个工具。*
