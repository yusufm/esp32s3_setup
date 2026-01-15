import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def wrap_text(draw, text, font, max_width_px):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width_px:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def layout_text_for_width(text, font_path, font_size_min, font_size_max, max_width_px):
    img = Image.new("1", (max_width_px, 32), 1)
    draw = ImageDraw.Draw(img)

    best = None
    for size in range(font_size_min, font_size_max + 1):
        font = ImageFont.truetype(font_path, size)
        lines = wrap_text(draw, text, font, max_width_px)
        widths = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            widths.append(bbox[2])
        max_line_w = max(widths) if widths else 0

        if max_line_w > max_width_px:
            continue

        score = 0
        if max_width_px > 0:
            score = max_line_w / max_width_px

        candidate = (score, size, lines, font)
        if best is None or candidate[0] > best[0]:
            best = candidate

    if best is None:
        font = ImageFont.truetype(font_path, font_size_min)
        lines = wrap_text(draw, text, font, max_width_px)
        return font, lines

    return best[3], best[2]


def image_to_1bit_rows(img_1bit):
    w, h = img_1bit.size
    if w % 8 != 0:
        raise ValueError("Width must be multiple of 8")

    px = img_1bit.load()
    out = bytearray()

    for y in range(h):
        for x0 in range(0, w, 8):
            b = 0
            for i in range(8):
                x = x0 + i
                v = px[x, y]
                bit = 1 if v == 0 else 0
                b = (b << 1) | bit
            out.append(b)

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--font", required=True, help="Path to a .ttf font file")
    ap.add_argument("--size", type=int, default=28)
    ap.add_argument("--auto_size", action="store_true", help="Auto-scale font to better fill width")
    ap.add_argument("--size_min", type=int, default=18)
    ap.add_argument("--size_max", type=int, default=72)
    ap.add_argument("--width", type=int, default=384, help="Printer width in pixels (58mm is typically 384)")
    ap.add_argument("--height", type=int, default=120, help="Slip height in pixels before rotation")
    ap.add_argument("--auto_height", action="store_true", help="Auto-calculate height based on rendered text")
    ap.add_argument("--margin", type=float, default=0.06, help="Horizontal margin as fraction of width")
    ap.add_argument("--rotate", type=int, default=90, choices=[0, 90, 180, 270])
    ap.add_argument("--out", default="src/fortune_slip_bitmap.py")
    args = ap.parse_args()

    width = args.width
    if width % 8 != 0:
        width = width - (width % 8)

    margin_x = int(width * args.margin)
    max_text_width = width - 2 * margin_x

    if args.auto_size:
        font, lines = layout_text_for_width(
            args.text,
            args.font,
            args.size_min,
            args.size_max,
            max_text_width,
        )
    else:
        font = ImageFont.truetype(args.font, args.size)
        img_tmp = Image.new("1", (width, 32), 1)
        draw_tmp = ImageDraw.Draw(img_tmp)
        lines = wrap_text(draw_tmp, args.text, font, max_text_width)

    img_probe = Image.new("1", (width, 32), 1)
    draw_probe = ImageDraw.Draw(img_probe)
    line_h = draw_probe.textbbox((0, 0), "Ag", font=font)[3]
    total_h = len(lines) * (line_h + 2)

    block_w = 18
    block_h = 10
    pad_y = max(12, int(line_h * 0.6))

    if args.auto_height:
        base_h = total_h + (pad_y * 2) + (block_h * 2)
        height = max(base_h, 60)
    else:
        height = args.height

    img = Image.new("1", (width, height), 1)
    draw = ImageDraw.Draw(img)

    y = max(0, (height - total_h) // 2)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2]
        x = (width - tw) // 2
        draw.text((x, y), line, font=font, fill=0)
        y += line_h + 2

    draw.rectangle([0, 0, block_w, block_h], fill=0)
    draw.rectangle([width - block_w - 1, 0, width - 1, block_h], fill=0)
    draw.rectangle([0, height - block_h - 1, block_w, height - 1], fill=0)
    draw.rectangle([width - block_w - 1, height - block_h - 1, width - 1, height - 1], fill=0)

    if args.rotate:
        img = img.rotate(args.rotate, expand=True, fillcolor=1)

    w, h = img.size
    w = w - (w % 8)
    if w != img.size[0]:
        img = img.crop((0, 0, w, h))

    data = image_to_1bit_rows(img)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    py = []
    py.append(f"WIDTH = {w}\n")
    py.append(f"HEIGHT = {h}\n")
    py.append("BITMAP = bytes([\n")
    for i in range(0, len(data), 16):
        chunk = data[i : i + 16]
        py.append("    " + ", ".join(str(b) for b in chunk) + ",\n")
    py.append("])\n")

    out_path.write_text("".join(py))
    print(f"Wrote {out_path} (WIDTH={w}, HEIGHT={h}, bytes={len(data)})")


if __name__ == "__main__":
    main()
