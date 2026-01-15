# Fortune Slip Tools

Tools for generating and previewing fortune slip bitmaps for thermal printing.

## Scripts

### `render_fortune_slip.py`
Generates a bitmap image from text for thermal printer output.

**Usage:**
```bash
python3 tools/render_fortune_slip.py \
  --text "Your fortune message here" \
  --font "/System/Library/Fonts/Helvetica.ttc" \
  --width 650 \
  --height 364 \
  --rotate 90 \
  --auto_size \
  --size_min 24 \
  --size_max 80 \
  --margin 0.04 \
  --out src/fortune_slip_bitmap.py
```

**Parameters:**
- `--text`: Fortune message to render (required)
- `--font`: Path to TTF font file (required)
- `--width`: Image width in pixels before rotation (default: 384)
- `--height`: Image height in pixels before rotation (default: 120)
- `--rotate`: Rotation angle - use 90 for portrait printing (default: 90)
- `--out`: Output Python file path (default: src/fortune_slip_bitmap.py)

**Important:** Always use `--rotate 90` to generate portrait-mode images that print vertically on the thermal printer.

### `preview_fortune_slip.py`
Preview the fortune slip bitmap without loading it onto the ESP32.

**Usage:**
```bash
python3 tools/preview_fortune_slip.py
```

This will:
1. Load the bitmap from `src/fortune_slip_bitmap.py`
2. Convert it to a PNG image
3. Save it as `tools/fortune_slip_preview.png`
4. Open it in your default image viewer

## Workflow

1. **Generate a new fortune slip:**
   ```bash
   python3 tools/render_fortune_slip.py \
     --text "Adventure awaits around the corner." \
     --font "/System/Library/Fonts/Helvetica.ttc" \
     --width 650 \
     --height 364 \
     --rotate 90 \
     --auto_size \
     --size_min 24 \
     --size_max 80 \
     --margin 0.04 \
     --out src/fortune_slip_bitmap_006.py
   ```

2. **Preview the result:**
   ```bash
   python3 tools/preview_fortune_slip.py
   ```

3. **Deploy to ESP32:**
   ```bash
   mpremote connect auto fs cp src/fortune_slip_bitmap_006.py :fortune_slip_bitmap_006.py
   mpremote connect auto reset
   ```

## Requirements

- Python 3.7+
- Pillow (PIL): `pip install Pillow`
