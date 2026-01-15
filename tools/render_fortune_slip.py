import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def wrap_text(draw, text, font, max_width_px):
    # Split by newlines first, then wrap each line
    paragraphs = text.split('\n')
    all_lines = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():  # Empty line
            all_lines.append('')
            continue
            
        words = paragraph.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] <= max_width_px:
                cur = test
            else:
                if cur:
                    all_lines.append(cur)
                cur = w
        if cur:
            all_lines.append(cur)
    
    return all_lines


def render_text_with_different_sizes(draw, text, font_path, font_size, max_width_px, max_height_px):
    """Render text with smaller font for lucky numbers line."""
    # Split the text into fortune and lucky numbers parts
    parts = text.split('\n\nLucky numbers: ')
    fortune_text = parts[0]
    lucky_numbers_text = 'Lucky numbers: ' + parts[1] if len(parts) > 1 else ''
    
    # Font for fortune text
    fortune_font = ImageFont.truetype(font_path, font_size)
    
    # Smaller font for lucky numbers (about 60% of main font size)
    lucky_font_size = max(12, int(font_size * 0.6))
    lucky_font = ImageFont.truetype(font_path, lucky_font_size)
    
    # Wrap fortune text
    fortune_lines = wrap_text(draw, fortune_text, fortune_font, max_width_px)
    
    # Wrap lucky numbers text if it exists
    lucky_lines = []
    if lucky_numbers_text:
        lucky_lines = wrap_text(draw, lucky_numbers_text, lucky_font, max_width_px)
    
    # Calculate total height needed
    line_height_fortune = draw.textbbox((0, 0), "Ag", font=fortune_font)[3]
    line_height_lucky = draw.textbbox((0, 0), "Ag", font=lucky_font)[3]
    
    # Add spacing between fortune and lucky numbers
    spacing = max(8, int(line_height_fortune * 0.5))
    
    total_height = (len(fortune_lines) * (line_height_fortune + 2)) + spacing
    if lucky_lines:
        total_height += (len(lucky_lines) * (line_height_lucky + 2))

    return fortune_lines, lucky_lines, fortune_font, lucky_font, line_height_fortune, line_height_lucky, spacing, total_height


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
        # Use the chosen auto-sized font's size for rendering
        chosen_size = getattr(font, "size", args.size_max)

        img_tmp = Image.new("1", (width, 32), 1)
        draw_tmp = ImageDraw.Draw(img_tmp)
        fortune_lines, lucky_lines, fortune_font, lucky_font, line_h_fortune, line_h_lucky, spacing, total_h = render_text_with_different_sizes(
            draw_tmp,
            args.text,
            args.font,
            chosen_size,
            max_text_width,
            args.height,
        )
    else:
        # Use the new function to handle different font sizes
        img_tmp = Image.new("1", (width, 32), 1)
        draw_tmp = ImageDraw.Draw(img_tmp)
        fortune_lines, lucky_lines, fortune_font, lucky_font, line_h_fortune, line_h_lucky, spacing, total_h = render_text_with_different_sizes(
            draw_tmp,
            args.text,
            args.font,
            args.size,
            max_text_width,
            args.height
        )
        font = fortune_font

    block_w = 18
    block_h = 10
    pad_y = max(12, int(line_h_fortune * 0.6))

    if args.auto_height:
        base_h = total_h + (pad_y * 2) + (block_h * 2)
        height = max(base_h, 60)
    else:
        height = args.height

    img = Image.new("1", (width, height), 1)
    draw = ImageDraw.Draw(img)

    y = max(0, (height - total_h) // 2)

    # Draw fortune text with main font
    for line in fortune_lines:
        bbox = draw.textbbox((0, 0), line, font=fortune_font)
        tw = bbox[2]
        x = (width - tw) // 2
        draw.text((x, y), line, font=fortune_font, fill=0)
        y += line_h_fortune + 2
    
    # Add spacing
    y += spacing
    
    # Draw lucky numbers with smaller font
    for line in lucky_lines:
        bbox = draw.textbbox((0, 0), line, font=lucky_font)
        tw = bbox[2]
        x = (width - tw) // 2
        draw.text((x, y), line, font=lucky_font, fill=0)
        y += line_h_lucky + 2

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
