# Fortune Slip Printing Guide

## Problem Solved ✓

The fortune cookie messages were printing **horizontally** instead of **vertically (landscape/portrait mode)** because the bitmap image was not rotated. Thermal printers feed paper vertically, so images need to be in portrait orientation (tall, not wide).

## Solution

The fortune slip bitmap has been regenerated with a **90-degree rotation**, changing it from:
- **Before:** 384×120 pixels (landscape - wide and short)
- **After:** 120×384 pixels (portrait - narrow and tall)

Now the fortune will print vertically on the thermal printer paper as intended.

This project prints **pre-rendered bitmap slips** (no dynamic text rendering). The ESP32 chooses a random bitmap module listed in `config.FORTUNE_SLIP_MODULES`.

## Files Cleaned Up

Removed unnecessary example files:
- `examples/fortune_cookie.py` (duplicate functionality)
- `examples/thermal_printer_test.py` (not needed)
- `examples/blink.py` (basic example)
- `examples/wifi.py` (not used)
- `examples/sensors/` (not needed)

## New Tool: Preview Fortune Slip

Created `tools/preview_fortune_slip.py` to preview the fortune slip image **without loading it onto the ESP32**.

### Usage:
```bash
python3 tools/preview_fortune_slip.py
```

This will:
1. Load the bitmap from `src/fortune_slip_bitmap.py`
2. Convert it to a PNG image
3. Save it as `tools/fortune_slip_preview.png`
4. Open it in your default image viewer

## How to Update Fortune Messages

### 1. Generate a new fortune slip bitmap:
```bash
python3 tools/render_fortune_slip.py \
  --text "Your new fortune message here" \
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

**Important:** Always use `--rotate 90` for vertical printing!

### 2. Preview the result locally:
```bash
python3 tools/preview_fortune_slip.py
```

### 3. Deploy to ESP32:
```bash
mpremote connect auto fs cp src/fortune_slip_bitmap_006.py :fortune_slip_bitmap_006.py
mpremote connect auto reset
```

Then add it to the pool in `src/config.py`:

```py
FORTUNE_SLIP_MODULES = [
    "fortune_slip_bitmap",
    "fortune_slip_bitmap_001",
    "fortune_slip_bitmap_002",
    "fortune_slip_bitmap_003",
    "fortune_slip_bitmap_004",
    "fortune_slip_bitmap_005",
    "fortune_slip_bitmap_006",
]
```

### 4. Test on printer:
Press the boot button on the ESP32 to print a fortune cookie!

## Current Fortune Message

The current fortune slip contains:
> "You cannot shake hands with a clenched fist."

## Technical Details

- **Printer:** 58mm thermal printer (printer mechanism is typically 384 pixels wide)
- **Bitmap format:** 1-bit monochrome (black/white)
- **Portrait dimensions (known-good):** 360×648 pixels
- **Rotation:** 90 degrees for vertical printing

## Files Structure

```
src/
  ├── fortune_cookie.py          # Fortune printing logic
  ├── fortune_slip_bitmap*.py    # Generated bitmap slips (pre-rendered)
  └── thermal_printer.py         # Printer driver

tools/
  ├── render_fortune_slip.py     # Generate bitmap from text
  ├── preview_fortune_slip.py    # Preview bitmap locally
  ├── fortune_slip_preview.png   # Latest preview image
  └── README.md                  # Tools documentation
```

## Next Steps

1. Load the updated code onto your ESP32:
   ```bash
   mpremote connect auto fs cp src/fortune_slip_bitmap_001.py :fortune_slip_bitmap_001.py
   mpremote connect auto reset
   ```

2. Press the boot button to print a fortune cookie

3. The fortune should now print **vertically** (portrait mode) as intended!
