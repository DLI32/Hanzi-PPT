#!/usr/bin/env python3
"""
hanzi-ppt · GIF 生成器
=======================
为汉字生成逐笔画动画 GIF。
数据来源：hanzi-writer-data（本地 npm 包优先，自动回退 CDN）

用法
----
  python3 src/make_gifs.py 学
  python3 src/make_gifs.py "同内辆轻较辅" --output ./output
  python3 src/make_gifs.py "汉字" --size 300 --fps 20 --speed 0.6 --pause 1.0
"""

import argparse
import json
import math
import os
import re
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

# ── 数据加载 ────────────────────────────────────────────────────────────────

# 本地 npm 包搜索路径（优先级从高到低）
_DATA_DIRS = [
    Path(__file__).parent.parent / "node_modules" / "hanzi-writer-data",
    Path.cwd() / "node_modules" / "hanzi-writer-data",
    Path.home() / "node_modules" / "hanzi-writer-data",
]

_CDN = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{char}.json"


def load_char_data(ch: str) -> dict:
    """加载汉字笔画数据（本地 → CDN 自动回退）"""
    for d in _DATA_DIRS:
        p = d / f"{ch}.json"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    url = _CDN.format(char=ch)
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        raise FileNotFoundError(
            f"'{ch}' 无笔画数据（本地 node_modules 未找到，CDN 请求失败: {e}）\n"
            "请先运行 npm install 安装 hanzi-writer-data"
        )


# ── SVG Path 解析 ───────────────────────────────────────────────────────────

def _parse_path(d: str) -> list:
    tokens = re.findall(r"[MmCcQqLlZz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", d)
    cmds, i = [], 0
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd, i, args = t, i + 1, []
            while i < len(tokens) and not tokens[i].isalpha():
                args.append(float(tokens[i]))
                i += 1
            cmds.append((cmd, args))
        else:
            i += 1
    return cmds


def _path_to_poly(d: str, steps: int = 50) -> list:
    pts, cx, cy, sx, sy = [], 0.0, 0.0, 0.0, 0.0
    for cmd, a in _parse_path(d):
        if cmd == "M":
            cx, cy = a[0], a[1]; sx, sy = cx, cy; pts.append((cx, cy))
        elif cmd == "m":
            cx += a[0]; cy += a[1]; sx, sy = cx, cy; pts.append((cx, cy))
        elif cmd == "L":
            cx, cy = a[0], a[1]; pts.append((cx, cy))
        elif cmd == "l":
            cx += a[0]; cy += a[1]; pts.append((cx, cy))
        elif cmd in ("Q", "q"):
            x1, y1, x2, y2 = (a[0], a[1], a[2], a[3]) if cmd == "Q" else (cx+a[0], cy+a[1], cx+a[2], cy+a[3])
            for t in range(1, steps + 1):
                tt = t / steps
                pts.append(((1-tt)**2*cx + 2*(1-tt)*tt*x1 + tt**2*x2,
                             (1-tt)**2*cy + 2*(1-tt)*tt*y1 + tt**2*y2))
            cx, cy = x2, y2
        elif cmd in ("C", "c"):
            x1,y1,x2,y2,x3,y3 = (a[0],a[1],a[2],a[3],a[4],a[5]) if cmd=="C" else (cx+a[0],cy+a[1],cx+a[2],cy+a[3],cx+a[4],cy+a[5])
            for t in range(1, steps + 1):
                tt = t / steps
                pts.append(((1-tt)**3*cx+3*(1-tt)**2*tt*x1+3*(1-tt)*tt**2*x2+tt**3*x3,
                             (1-tt)**3*cy+3*(1-tt)**2*tt*y1+3*(1-tt)*tt**2*y2+tt**3*y3))
            cx, cy = x3, y3
        elif cmd in ("Z", "z"):
            pts.append((sx, sy))
    return pts


def _transform(pts: list, size: int, pad: int = 18) -> list:
    sc = (size - 2 * pad) / 1024
    return [(pad + x * sc, size - pad - y * sc) for x, y in pts]


# ── 帧渲染 ──────────────────────────────────────────────────────────────────

_STROKE_COLOR  = (23, 132, 81)
_OUTLINE_COLOR = (225, 225, 225)
_GRID_COLOR    = (210, 210, 210)
_BG_COLOR      = (255, 255, 255)


def render_frame(data: dict, stroke_progress: float, size: int = 300) -> Image.Image:
    img = Image.new("RGB", (size, size), _BG_COLOR)
    draw = ImageDraw.Draw(img)
    h = size // 2
    draw.line([(h, 4), (h, size - 4)], fill=_GRID_COLOR, width=1)
    draw.line([(4, h), (size - 4, h)], fill=_GRID_COLOR, width=1)
    draw.rectangle([3, 3, size - 4, size - 4], outline=_GRID_COLOR, width=1)

    strokes  = data["strokes"]
    medians  = data["medians"]
    n        = len(strokes)
    done     = int(stroke_progress)
    partial  = stroke_progress - done

    for s in strokes:
        tpts = _transform(_path_to_poly(s), size)
        if len(tpts) >= 3:
            draw.polygon(tpts, fill=_OUTLINE_COLOR)

    for i in range(min(done, n)):
        tpts = _transform(_path_to_poly(strokes[i]), size)
        if len(tpts) >= 3:
            draw.polygon(tpts, fill=_STROKE_COLOR)

    if done < n and partial > 0.01:
        med = medians[done]
        if med and len(med) >= 2:
            tmed = _transform(med, size)
            end  = max(1, int(math.ceil(partial * (len(tmed) - 1))))
            seg  = tmed[: end + 1]
            if len(seg) >= 2:
                draw.line(seg, fill=_STROKE_COLOR, width=max(6, size // 30), joint="curve")
    return img


# ── GIF 生成 ────────────────────────────────────────────────────────────────

def make_gif(
    ch: str,
    output_path: str,
    size: int = 300,
    fps: int = 20,
    stroke_duration: float = 0.6,
    inter_stroke: float = 0.25,
    char_pause: float = 1.0,
) -> int:
    """生成单字 GIF，返回笔画数。"""
    data   = load_char_data(ch)
    n      = len(data["strokes"])
    fms    = int(1000 / fps)
    sf     = max(1, int(stroke_duration * fps))
    pf     = max(1, int(inter_stroke * fps))
    cpf    = max(1, int(char_pause * fps))
    frames, durations = [], []

    for si in range(n):
        for f in range(sf):
            frames.append(render_frame(data, si + (f + 1) / sf, size))
            durations.append(fms)
        if si < n - 1:
            for _ in range(pf):
                frames.append(render_frame(data, si + 1.0, size))
                durations.append(fms)
    for _ in range(cpf):
        frames.append(render_frame(data, float(n), size))
        durations.append(fms)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    pf_list = [f.convert("P", palette=Image.ADAPTIVE, colors=64) for f in frames]
    pf_list[0].save(
        output_path, format="GIF",
        append_images=pf_list[1:],
        save_all=True, duration=durations,
        loop=0, optimize=True,
    )
    return n


# ── CLI ─────────────────────────────────────────────────────────────────────

def _is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or 0xF900 <= cp <= 0xFAFF


def main():
    parser = argparse.ArgumentParser(
        description="生成汉字笔画动画 GIF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("chars",             help="要生成的汉字，如 '同内辆轻'")
    parser.add_argument("--output", "-o",    default="./output",  help="输出目录（默认 ./output）")
    parser.add_argument("--size",   "-s",    type=int,   default=300,  help="图像尺寸 px（默认 300）")
    parser.add_argument("--fps",    "-f",    type=int,   default=20,   help="帧率（默认 20）")
    parser.add_argument("--speed",           type=float, default=0.6,  help="每笔时长秒（默认 0.6）")
    parser.add_argument("--pause",           type=float, default=1.0,  help="字间停顿秒（默认 1.0）")
    parser.add_argument("--prefix",          default="hanzi_",         help="文件名前缀（默认 hanzi_）")
    args = parser.parse_args()

    char_list = [c for c in args.chars if _is_cjk(c)]
    if not char_list:
        print("错误：输入中没有有效的 CJK 汉字"); sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    ok = fail = 0
    for ch in char_list:
        out = os.path.join(args.output, f"{args.prefix}{ch}.gif")
        try:
            n = make_gif(ch, out, size=args.size, fps=args.fps,
                         stroke_duration=args.speed, char_pause=args.pause)
            print(f"  ✓  {ch}  {n} 画  →  {out}")
            ok += 1
        except Exception as e:
            print(f"  ✗  {ch}  失败：{e}")
            fail += 1

    print(f"\n完成：{ok} 成功，{fail} 失败")


if __name__ == "__main__":
    main()
