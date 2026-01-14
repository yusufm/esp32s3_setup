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
  --size 28 \
  --width 384 \
  --height 120 \
  --rotate 90 \
  --out src/fortune_slip_bitmap.py
```

**Parameters:**
- `--text`: Fortune message to render (required)
- `--font`: Path to TTF font file (required)
- `--size`: Font size in points (default: 28)
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
     --size 28 \
     --rotate 90
   ```

2. **Preview the result:**
   ```bash
   python3 tools/preview_fortune_slip.py
   ```

3. **Deploy to ESP32:**
   ```bash
   mpremote connect auto cp src/fortune_slip_bitmap.py :fortune_slip_bitmap.py
   mpremote connect auto reset
   ```

## Requirements

- Python 3.7+
- Pillow (PIL): `pip install Pillow`
