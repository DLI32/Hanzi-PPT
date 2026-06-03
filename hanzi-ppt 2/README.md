# hanzi-ppt

> 汉字笔画动画 GIF + PowerPoint 生成工具

---

## 从 GitHub 获取并使用

### 第一步：下载项目

**方式 A：有 Git（推荐）**
```bash
git clone https://github.com/你的用户名/hanzi-ppt.git
cd hanzi-ppt
```

**方式 B：没有 Git**
- 打开仓库页面 → 点绿色 **Code** 按钮 → **Download ZIP**
- 解压后进入文件夹

---

### 第二步：安装环境（只需做一次）

确认已安装 Python 和 Node.js：

```bash
python3 --version   # 需要 3.8+
node --version      # 需要 16+
```

没有的话：
- Python：https://python.org/downloads
- Node.js：https://nodejs.org

然后安装依赖：

```bash
# 在项目文件夹内运行
npm install          # 安装笔画数据和 PPT 库（约 30MB）
pip install pillow   # 安装图像处理库
```

---

### 第三步：生成你的汉字 GIF

```bash
python3 src/make_gifs.py "你想要的汉字" --output ./output
```

例如：
```bash
python3 src/make_gifs.py "学习汉字" --output ./output
```

运行后 `output/` 文件夹里会出现 `hanzi_学.gif`、`hanzi_习.gif` 等文件。

---

### 第四步：配置你的 PPT 内容

复制示例配置，按需修改：

```bash
cp examples/config_example.json my_config.json
```

用任意文本编辑器打开 `my_config.json`，修改汉字内容：

```json
{
  "title": "我的汉字课",
  "groups": [
    {
      "name": "本课生词",
      "color": "178451",
      "colorLight": "E8F5EE",
      "note": "本单元重点字",
      "chars": [
        { "ch": "学", "py": "xué", "strokes": 8, "words": ["学习", "学生", "学校"] },
        { "ch": "习", "py": "xí",  "strokes": 3, "words": ["习惯", "练习", "预习"] }
      ]
    }
  ]
}
```

---

### 第五步：生成 PPT

```bash
node src/make_pptx.js --config my_config.json --gif-dir ./output --out ./output/我的课件.pptx
```

---

### 第六步：修复 GIF 动画（必须）

```bash
python3 src/fix_gif_pptx.py output/我的课件.pptx output/我的课件_final.pptx
```

打开 `output/我的课件_final.pptx`，用 **PowerPoint 放映模式**即可看到笔画动画。

---

为汉字自动生成逐笔画动画 GIF，并打包成 PowerPoint 教学幻灯片。  
笔画数据来源：[hanzi-writer-data](https://github.com/chanind/hanzi-writer-data)，支持 9000+ 简繁体常用汉字。

---

## 效果预览

| GIF 动画 | PowerPoint 幻灯片 |
|:---:|:---:|
| 逐笔绘制，绿色笔画，带格线 | 左 GIF + 右大字/拼音/词组 |

每张幻灯片包含：
- 左侧：GIF 笔画动画（放映时自动循环播放）
- 右侧：大字、拼音、常用词组

---

## 环境要求

| 工具 | 版本 |
|---|---|
| Python | 3.8 + |
| Node.js | 16 + |
| Pillow | 任意 |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/hanzi-ppt.git
cd hanzi-ppt
```

### 2. 安装依赖

```bash
# Node 依赖（笔画数据 + PPT 生成）
npm install

# Python 依赖（GIF 渲染）
pip install pillow
```

### 3. 生成 GIF

```bash
python3 src/make_gifs.py "同内辆轻较辅" --output ./output
```

参数说明：

```
positional:
  chars             要生成的汉字字符串

optional:
  --output, -o      输出目录（默认 ./output）
  --size,   -s      图像尺寸 px（默认 300）
  --fps,    -f      帧率（默认 20）
  --speed           每笔时长秒（默认 0.6）
  --pause           字间停顿秒（默认 1.0）
  --prefix          文件名前缀（默认 hanzi_）
```

### 4. 编写配置文件

复制并修改示例配置：

```bash
cp examples/config_example.json my_config.json
```

配置格式：

```json
{
  "title": "汉字笔画动画",
  "groups": [
    {
      "name": "车字旁",
      "color": "B45309",
      "colorLight": "FEF3C7",
      "note": "与车辆、运输有关",
      "chars": [
        { "ch": "辆", "py": "liàng", "strokes": 11, "words": ["一辆","车辆","辆数"] },
        { "ch": "轻", "py": "qīng",  "strokes": 9,  "words": ["轻松","年轻","轻重"] }
      ]
    }
  ]
}
```

### 5. 生成 PPT

```bash
node src/make_pptx.js --config my_config.json --gif-dir ./output --out ./output/deck.pptx
```

### 6. 修复 GIF 动画播放（必须）

pptxgenjs 默认以静态图片嵌入 GIF，需要打补丁才能在 PowerPoint 放映时播放动画：

```bash
python3 src/fix_gif_pptx.py output/deck.pptx output/deck_final.pptx
```

---

## 一键运行示例

```bash
# 生成示例配置里的所有字
python3 src/make_gifs.py "辆轻较辅同内" --output ./output

# 生成 PPT
node src/make_pptx.js --config examples/config_example.json --out ./output/example.pptx

# 修复动画
python3 src/fix_gif_pptx.py output/example.pptx output/example_final.pptx
```

---

## 文件结构

```
hanzi-ppt/
├── src/
│   ├── make_gifs.py        # GIF 生成器
│   ├── make_pptx.js        # PPT 生成器
│   └── fix_gif_pptx.py     # GIF 动画修复工具
├── examples/
│   └── config_example.json # 示例配置
├── output/                 # 生成文件（git 忽略）
├── package.json
└── README.md
```

---

## PPT 播放说明

| 软件 | GIF 动画 |
|---|---|
| PowerPoint Microsoft 365 / Office 2016+ | ✅ 放映模式自动循环播放 |
| WPS | ❌ 显示为静图（不支持此 OOXML 扩展） |
| LibreOffice Impress | ❌ 显示为静图 |

> **提示**：如果 PowerPoint 动画仍不播放，请确认已运行 `fix_gif_pptx.py` 修复步骤。

---

## 自定义颜色

`color` 字段使用 6 位十六进制色值（不含 `#`）：

| 颜色 | 色值 | 适合场景 |
|---|---|---|
| 绿色 | `178451` | 默认笔画色 |
| 蓝色 | `1560BD` | 门字框 |
| 棕橙 | `B45309` | 车字旁 |
| 红色 | `C0392B` | 攵旁 |
| 深绿 | `1A6B3C` | 饣旁 |

---

## 数据来源与许可

- 笔画数据：[hanzi-writer-data](https://github.com/chanind/hanzi-writer-data)（Arphic Public License）
- 本项目代码：MIT License
