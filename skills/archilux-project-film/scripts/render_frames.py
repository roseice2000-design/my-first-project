#!/usr/bin/env python3
"""把分镜表(storyboard.json)里的每个镜头，渲染成带文字排版的 4K 静帧。

用法: python3 render_frames.py projects/<项目>/storyboard.json
输出: projects/<项目>/build/frames/NN.png  (3840x2160，留给视频推拉镜头的余量)
"""
import json, sys, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 3840, 2160
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]

def font(size):
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def cover(img, w, h):
    r = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def paper(style):
    c = tuple(style.get("paper", [244, 239, 230]))
    return Image.new("RGB", (W, H), c)

def draw_text_block(d, lines, x, y, style, align="left", max_w=None):
    ink = tuple(style.get("ink", [60, 48, 40]))
    accent = tuple(style.get("accent", [139, 26, 26]))
    for ln in lines:
        kind = ln.get("kind", "body")
        size = {"eyebrow": 54, "title": 150, "subtitle": 84, "body": 72, "caption": 46}[kind]
        f = font(size)
        color = accent if kind == "eyebrow" else ink
        text = ln["text"]
        tw = d.textlength(text, font=f)
        tx = x - tw if align == "right" else (x - tw / 2 if align == "center" else x)
        d.text((tx, y), text, font=f, fill=color)
        y += int(size * 1.55)
    return y

def render(shot, base_dir, style):
    layout = shot.get("layout", "full")
    img = None
    if shot.get("image"):
        p = (base_dir / shot["image"]).resolve()
        if p.exists():
            img = Image.open(p).convert("RGB")
        else:
            print(f"  ! 缺图 {p}，先用纸色底占位")
    canvas = paper(style)
    d = ImageDraw.Draw(canvas)
    lines = shot.get("text", [])
    if layout == "full" and img:
        canvas = cover(img, W, H)
        # 底部渐变压暗，保证字可读
        grad = Image.new("L", (1, H))
        for yy in range(H):
            grad.putpixel((0, yy), int(200 * max(0, (yy - H * 0.45) / (H * 0.55))))
        shade = Image.new("RGB", (W, H), (20, 16, 12))
        canvas = Image.composite(shade, canvas, grad.resize((W, H)))
        d = ImageDraw.Draw(canvas)
        st = dict(style, ink=[245, 240, 232], accent=[230, 200, 160])
        draw_text_block(d, lines, 220, H - 240 - 130 * len(lines), st)
    elif layout == "split" and img:
        canvas.paste(cover(img, int(W * 0.58), H), (0, 0))
        draw_text_block(d, lines, int(W * 0.63), 520, style)
    elif layout == "plan" and img:
        # 图纸完整显示（不裁切），上方标题
        y = draw_text_block(d, lines, 220, 160, style)
        im = img.copy(); im.thumbnail((W - 440, H - y - 200), Image.LANCZOS)
        from PIL import ImageChops  # 白底与纸色相乘，图纸“印”在纸上
        im = ImageChops.multiply(im, Image.new("RGB", im.size, tuple(style.get("paper", [244, 239, 230]))))
        canvas.paste(im, ((W - im.width) // 2, y + 60))
    else:  # "card": 纯文字卡，纸色底
        if img:
            canvas = cover(img, W, H).filter(ImageFilter.GaussianBlur(30))
            canvas = Image.blend(canvas, paper(style), 0.82)
            d = ImageDraw.Draw(canvas)
        total = sum(int({"eyebrow":54,"title":150,"subtitle":84,"body":72,"caption":46}[l.get("kind","body")]*1.55) for l in lines)
        draw_text_block(d, lines, W // 2, (H - total) // 2, style, align="center")
    cap = shot.get("caption")
    if cap:
        d.text((W - 220 - d.textlength(cap, font=font(40)), H - 120), cap, font=font(40),
               fill=(200, 195, 185) if layout == "full" else (140, 130, 120))
    return canvas

def main():
    sb_path = Path(sys.argv[1]).resolve()
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    base = sb_path.parent
    out = base / "build" / "frames"
    out.mkdir(parents=True, exist_ok=True)
    style = sb.get("style", {})
    for i, shot in enumerate(sb["shots"], 1):
        render(shot, base, style).save(out / f"{i:02d}.png")
        print(f"  ✓ {i:02d} {shot.get('node','')}")
    print(f"静帧已生成: {out}")

if __name__ == "__main__":
    main()
