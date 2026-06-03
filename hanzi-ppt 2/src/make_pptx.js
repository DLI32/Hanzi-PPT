#!/usr/bin/env node
/**
 * hanzi-ppt · PPT 生成器
 * ========================
 * 读取配置文件，将汉字 GIF 生成为 PowerPoint 幻灯片。
 *
 * 用法
 * ----
 *   node src/make_pptx.js --config my_config.json
 *   node src/make_pptx.js --config my_config.json --gif-dir ./output --out ./output/deck.pptx
 *
 * 配置文件格式（JSON）
 * --------------------
 * {
 *   "title": "汉字笔画动画",
 *   "groups": [
 *     {
 *       "name": "车字旁",
 *       "color": "B45309",
 *       "colorLight": "FEF3C7",
 *       "note": "与车辆、运输相关",
 *       "chars": [
 *         { "ch": "辆", "py": "liàng", "strokes": 11, "words": ["一辆","车辆","辆数"] }
 *       ]
 *     }
 *   ]
 * }
 */

"use strict";

const pptxgen = require("pptxgenjs");
const fs      = require("fs");
const path    = require("path");

// ── 默认配色 ─────────────────────────────────────────────────────────────────
const BASE = {
  dark:   "1C1C2E",
  white:  "FFFFFF",
  gray:   "6B7280",
  border: "E5E7EB",
  bg:     "F8F9FA",
};

// ── 字符幻灯片 ────────────────────────────────────────────────────────────────
function addCharSlide(pres, item, groupName, color, colorLight, gifDir) {
  const gifPath = path.join(gifDir, `hanzi_${item.ch}.gif`);
  if (!fs.existsSync(gifPath)) {
    console.warn(`  ⚠  GIF 不存在: ${gifPath}`);
    return;
  }

  const slide = pres.addSlide();
  slide.background = { color: BASE.bg };

  // 左：白面板 + 偏旁标签 + GIF + 笔画数
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:4.3, h:5.625,
    fill:{ color:BASE.white }, line:{ color:BASE.border, width:0 },
  });
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x:0.28, y:0.26, w:1.6, h:0.36,
    fill:{ color }, line:{ color }, rectRadius:0.05,
  });
  slide.addText(groupName, {
    x:0.28, y:0.26, w:1.6, h:0.36,
    fontSize:12, color:BASE.white, bold:true,
    fontFace:"Microsoft YaHei", align:"center", valign:"middle", margin:0,
  });
  slide.addImage({ path:gifPath, x:0.32, y:0.75, w:3.65, h:3.65 });
  slide.addText(`${item.strokes} 画`, {
    x:0.32, y:4.48, w:3.65, h:0.38,
    fontSize:13, color:BASE.gray, fontFace:"Microsoft YaHei", align:"center",
  });

  // 右：大字 + 拼音 + 词组
  slide.addText(item.ch, {
    x:4.5, y:0.25, w:2.9, h:2.55,
    fontSize:138, bold:true, color:BASE.dark,
    fontFace:"Microsoft YaHei", align:"center", valign:"middle",
  });
  slide.addText(item.py, {
    x:4.5, y:2.88, w:2.9, h:0.55,
    fontSize:26, color, bold:true, fontFace:"Microsoft YaHei", align:"center",
  });
  slide.addShape(pres.shapes.LINE, {
    x:4.5, y:3.58, w:5.15, h:0, line:{ color:BASE.border, width:1 },
  });
  slide.addText("常用词组", {
    x:4.5, y:3.72, w:5.15, h:0.28,
    fontSize:11, color:BASE.gray, fontFace:"Microsoft YaHei",
  });
  (item.words || []).forEach((w, wi) => {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:4.5+wi*1.75, y:4.1, w:1.58, h:0.5,
      fill:{ color:colorLight }, line:{ color:colorLight }, rectRadius:0.06,
    });
    slide.addText(w, {
      x:4.5+wi*1.75, y:4.1, w:1.58, h:0.5,
      fontSize:17, color, bold:true,
      fontFace:"Microsoft YaHei", align:"center", valign:"middle", margin:0,
    });
  });
  // 装饰数字
  slide.addText(String(item.strokes), {
    x:8.5, y:4.72, w:1.3, h:0.78,
    fontSize:50, color:BASE.border, bold:true,
    fontFace:"Microsoft YaHei", align:"right",
  });
  console.log(`  ✓  ${item.ch}（${item.py}）${item.strokes} 画`);
}

// ── 分组标题幻灯片 ────────────────────────────────────────────────────────────
function addGroupSlide(pres, group) {
  const s = pres.addSlide();
  s.background = { color: group.color };
  s.addText(group.name, {
    x:0.5, y:1.5, w:9, h:1.5,
    fontSize:72, bold:true, color:BASE.white,
    fontFace:"Microsoft YaHei", align:"center",
  });
  s.addText(group.note || "", {
    x:0.5, y:3.2, w:9, h:0.5,
    fontSize:20, color:BASE.white, fontFace:"Microsoft YaHei", align:"center",
  });
  s.addText((group.chars || []).map(c => c.ch).join("  "), {
    x:0.5, y:3.85, w:9, h:0.55,
    fontSize:26, bold:true, color:BASE.white,
    fontFace:"Microsoft YaHei", align:"center",
  });
}

// ── 封面幻灯片 ────────────────────────────────────────────────────────────────
function addCoverSlide(pres, config) {
  const s = pres.addSlide();
  s.background = { color: BASE.dark };
  s.addText(config.title || "汉字笔画动画", {
    x:0.5, y:1.1, w:9, h:1.2,
    fontSize:52, bold:true, color:BASE.white,
    fontFace:"Microsoft YaHei", align:"center",
  });
  const groupNames = (config.groups || []).map(g => g.name).join("  ·  ");
  s.addText(groupNames, {
    x:0.5, y:2.55, w:9, h:0.65,
    fontSize:24, color:"A0AEC0", fontFace:"Microsoft YaHei", align:"center",
  });
  const allChars = (config.groups || []).flatMap(g => (g.chars||[]).map(c => c.ch)).join(" · ");
  s.addText(allChars, {
    x:0.5, y:3.3, w:9, h:0.45,
    fontSize:16, color:"4A5568", fontFace:"Microsoft YaHei", align:"center",
  });
  s.addText("逐笔动画  ·  常用词组", {
    x:0.5, y:3.85, w:9, h:0.35,
    fontSize:13, color:"4A5568", fontFace:"Microsoft YaHei", align:"center",
  });
  // 分组色条
  const groups = config.groups || [];
  const bw = 10 / Math.max(groups.length, 1);
  groups.forEach((g, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:i*bw, y:5.1, w:bw, h:0.25,
      fill:{ color:g.color }, line:{ color:g.color },
    });
    s.addText(`${g.name}  ${(g.chars||[]).map(c=>c.ch).join(" ")}`, {
      x:i*bw, y:4.72, w:bw, h:0.35,
      fontSize:11, color:"718096", fontFace:"Microsoft YaHei", align:"center",
    });
  });
}

// ── 总结幻灯片 ────────────────────────────────────────────────────────────────
function addSummarySlide(pres, config) {
  const groups = config.groups || [];
  if (groups.length === 0) return;
  const s = pres.addSlide();
  s.background = { color: BASE.dark };
  s.addText("偏旁总结", {
    x:0.5, y:0.3, w:9, h:0.7,
    fontSize:30, bold:true, color:BASE.white,
    fontFace:"Microsoft YaHei", align:"center",
  });
  const cardW = Math.min(4.4, 9.2 / groups.length);
  const gap   = (10 - cardW * groups.length) / (groups.length + 1);
  groups.forEach((g, i) => {
    const x = gap + i * (cardW + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y:1.1, w:cardW, h:4.2,
      fill:{ color:"000000" }, line:{ color:g.color, width:2 }, rectRadius:0.1,
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y:1.1, w:cardW, h:0.6,
      fill:{ color:g.color }, line:{ color:g.color }, rectRadius:0.1,
    });
    s.addText(g.name, {
      x, y:1.1, w:cardW, h:0.6,
      fontSize:16, bold:true, color:BASE.white,
      fontFace:"Microsoft YaHei", align:"center", valign:"middle", margin:0,
    });
    s.addText((g.chars||[]).map(c=>c.ch).join("  "), {
      x, y:1.82, w:cardW, h:0.65,
      fontSize:22, bold:true, color:BASE.white,
      fontFace:"Microsoft YaHei", align:"center",
    });
    if (g.note) {
      s.addText(g.note, {
        x:x+0.15, y:2.6, w:cardW-0.3, h:0.5,
        fontSize:12, color:"94A3B8", fontFace:"Microsoft YaHei",
      });
    }
  });
}

// ── 主函数 ────────────────────────────────────────────────────────────────────
async function main() {
  const args  = process.argv.slice(2);
  const get   = (flag, def) => { const i = args.indexOf(flag); return i >= 0 ? args[i+1] : def; };

  const configPath = get("--config", null);
  const gifDir     = get("--gif-dir", "./output");
  const outFile    = get("--out", "./output/汉字笔画.pptx");

  if (!configPath) {
    console.error("用法: node src/make_pptx.js --config <config.json> [--gif-dir ./output] [--out ./output/deck.pptx]");
    console.error("示例配置文件见 examples/config_example.json");
    process.exit(1);
  }

  if (!fs.existsSync(configPath)) {
    console.error(`配置文件不存在: ${configPath}`); process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  fs.mkdirSync(path.dirname(path.resolve(outFile)), { recursive: true });

  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title  = config.title || "汉字笔画动画";

  addCoverSlide(pres, config);

  for (const group of (config.groups || [])) {
    addGroupSlide(pres, group);
    for (const item of (group.chars || [])) {
      addCharSlide(pres, item, group.name, group.color, group.colorLight || "F0F0F0", gifDir);
    }
  }

  addSummarySlide(pres, config);

  await pres.writeFile({ fileName: outFile });
  console.log(`\n✅  PPT 已保存 → ${outFile}`);
  console.log(`\n⚠️  还需执行修复步骤让 GIF 动画在 PowerPoint 中播放：`);
  console.log(`   python3 src/fix_gif_pptx.py "${outFile}" "${outFile.replace('.pptx','_final.pptx')}"`);
}

main().catch(e => { console.error(e); process.exit(1); });
