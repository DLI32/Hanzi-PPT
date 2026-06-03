#!/usr/bin/env python3
"""
hanzi-ppt · PPTX GIF 动画修复工具
====================================
pptxgenjs 将 GIF 以静态 image 关系嵌入 PPTX。
PowerPoint 要求同时存在 video 关系 + <a:videoFile> 标签才能播放 GIF 动画。
本工具通过纯字符串替换修补 OOXML，不改变原有 namespace。

用法
----
  python3 src/fix_gif_pptx.py input.pptx output_final.pptx

要求
----
  Python 3.6+，仅用标准库，无需额外安装
"""

import os
import re
import shutil
import sys
import zipfile

REL_VIDEO = "http://schemas.microsoft.com/office/2007/relationships/video"


def fix_gif_animation(src: str, dst: str) -> int:
    """
    修补 PPTX 中 GIF 的动画关系。
    返回成功修补的 GIF 数量。
    """
    tmp = src + "_fix_tmp"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    shutil.unpack_archive(src, tmp, "zip")

    slides_dir = os.path.join(tmp, "ppt", "slides")
    rels_dir   = os.path.join(tmp, "ppt", "slides", "_rels")
    fixed = 0

    if not os.path.exists(slides_dir):
        raise ValueError(f"不是有效的 PPTX 文件：找不到 ppt/slides/ 目录")

    for slide_fn in sorted(os.listdir(slides_dir)):
        if not slide_fn.endswith(".xml"):
            continue
        rels_path  = os.path.join(rels_dir, slide_fn + ".rels")
        slide_path = os.path.join(slides_dir, slide_fn)
        if not os.path.exists(rels_path):
            continue

        rels_text  = open(rels_path,  encoding="utf-8").read()
        slide_text = open(slide_path, encoding="utf-8").read()

        gif_rels = re.findall(
            r'<Relationship Id="([^"]+)" Type="[^"]+/relationships/image" Target="([^"]+\.gif)"',
            rels_text,
        )
        if not gif_rels:
            continue

        for img_rid, target in gif_rels:
            vid_rid   = f"{img_rid}v"
            video_rel = f'<Relationship Id="{vid_rid}" Type="{REL_VIDEO}" Target="{target}"/>'
            rels_text = rels_text.replace("</Relationships>", video_rel + "</Relationships>")

            parts = re.split(r"(<p:pic>)", slide_text)
            new_parts = []
            for i, part in enumerate(parts):
                if i > 0 and parts[i - 1] == "<p:pic>" and f'r:embed="{img_rid}"' in part:
                    if "<p:nvPr/>" in part:
                        part = part.replace(
                            "<p:nvPr/>",
                            f'<p:nvPr><a:videoFile r:link="{vid_rid}"/></p:nvPr>',
                        )
                        fixed += 1
                    elif "<p:nvPr>" in part:
                        part = part.replace(
                            "<p:nvPr>",
                            f'<p:nvPr><a:videoFile r:link="{vid_rid}"/>',
                        )
                        fixed += 1
                new_parts.append(part)
            slide_text = "".join(new_parts)

        open(rels_path,  "w", encoding="utf-8").write(rels_text)
        open(slide_path, "w", encoding="utf-8").write(slide_text)

    if os.path.exists(dst):
        os.remove(dst)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(tmp):
            for file in files:
                fp = os.path.join(root, file)
                zout.write(fp, os.path.relpath(fp, tmp))
    shutil.rmtree(tmp)
    return fixed


def main():
    if len(sys.argv) < 3:
        print("用法: python3 src/fix_gif_pptx.py <输入.pptx> <输出_final.pptx>")
        print("示例: python3 src/fix_gif_pptx.py output/deck.pptx output/deck_final.pptx")
        sys.exit(1)

    src, dst = sys.argv[1], sys.argv[2]
    if not os.path.exists(src):
        print(f"错误：文件不存在 → {src}"); sys.exit(1)

    print(f"修复 GIF 动画：{src}")
    n = fix_gif_animation(src, dst)
    print(f"✅  修补了 {n} 个 GIF → {dst}")
    print()
    print("播放说明：")
    print("  • PowerPoint（Microsoft 365 / Office 2016+）：放映模式下 GIF 自动循环播放")
    print("  • WPS：不支持此 OOXML 扩展，GIF 显示为静图")


if __name__ == "__main__":
    main()
