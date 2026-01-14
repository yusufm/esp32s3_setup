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
    ap.add_argument("--width", type=int, default=384, help="Printer width in pixels (58mm is typically 384)")
    ap.add_argument("--height", type=int, default=120, help="Slip height in pixels before rotation")
    ap.add_argument("--rotate", type=int, default=90, choices=[0, 90, 180, 270])
    ap.add_argument("--out", default="src/fortune_slip_bitmap.py")
    args = ap.parse_args()

    width = args.width
    if width % 8 != 0:
        width = width - (width % 8)

    img = Image.new("1", (width, args.height), 1)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(args.font, args.size)

    margin_x = int(width * 0.10)
    max_text_width = width - 2 * margin_x

    lines = wrap_text(draw, args.text, font, max_text_width)

    line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
    total_h = len(lines) * (line_h + 2)
    y = max(0, (args.height - total_h) // 2)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2]
        x = (width - tw) // 2
        draw.text((x, y), line, font=font, fill=0)
        y += line_h + 2

    block_w = 18
    block_h = 10
    draw.rectangle([0, 0, block_w, block_h], fill=0)
    draw.rectangle([width - block_w - 1, 0, width - 1, block_h], fill=0)
    draw.rectangle([0, args.height - block_h - 1, block_w, args.height - 1], fill=0)
    draw.rectangle([width - block_w - 1, args.height - block_h - 1, width - 1, args.height - 1], fill=0)

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
