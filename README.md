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
