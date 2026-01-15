# ESP32-S3 MicroPython Quickstart (Cookbook)

A minimal, repeatable setup for flashing and running MicroPython on a new ESP32-S3 board.

---

## 0️⃣ Plug in
- Use the USB port labeled **COM**

---

## 1️⃣ Install tools (once)
```bash
pip install --upgrade esptool mpremote
```

---

## 2️⃣ Download firmware
- Go to: https://micropython.org/download/ESP32_GENERIC_S3/
- Download the latest **.bin** file
- **Important**: Use the standard firmware version, NOT "Support for Octal-SPIRAM"
- For boards with 2MB PSRAM: Use the regular ESP32_GENERIC_S3 firmware

---

## 3️⃣ Flash firmware
```bash
esptool erase-flash
esptool write-flash 0 ESP32_GENERIC_S3-*.bin
```

---

## 4️⃣ Upload project files
```bash
mpremote connect auto fs cp src/boot.py :boot.py
mpremote connect auto fs cp src/main.py :main.py
mpremote connect auto fs cp src/config.py :config.py
mpremote connect auto fs cp src/thermal_printer.py :thermal_printer.py
mpremote connect auto fs cp src/fortune_cookie.py :fortune_cookie.py
mpremote connect auto fs cp src/fortune_slip_bitmap.py :fortune_slip_bitmap.py
mpremote connect auto fs cp src/fortune_slip_bitmap_001.py :fortune_slip_bitmap_001.py
mpremote connect auto fs cp src/fortune_slip_bitmap_002.py :fortune_slip_bitmap_002.py
mpremote connect auto fs cp src/fortune_slip_bitmap_003.py :fortune_slip_bitmap_003.py
mpremote connect auto fs cp src/fortune_slip_bitmap_004.py :fortune_slip_bitmap_004.py
mpremote connect auto fs cp src/fortune_slip_bitmap_005.py :fortune_slip_bitmap_005.py
mpremote connect auto reset
```

**Note:** If the board gets stuck in a boot loop, first remove main.py:
```bash
mpremote connect auto repl
>>> import os
>>> os.remove('main.py')
>>> os.remove('boot.py')
```
Then upload new files.

**Update mode:** If `mpremote` stops being able to copy files after you install `boot.py`/`main.py`, reset the board while holding the **BOOT** button. This skips starting the main application loop so you can reliably use `mpremote connect auto fs cp ...`.

---

## 5️⃣ Connect to REPL
```bash
mpremote connect auto repl
```

Exit REPL with: `Ctrl + ]` or `Ctrl + x` 

---

## ⚠️ Rules / Gotchas
- Always use the **COM** USB port
- Do not flash to any address other than `0` 
- Use non-PSRAM firmware unless PSRAM is confirmed
- Firmware updates erase all files on the board

---

## ✅ Known-Good Setup
- Board: ESP32-S3 (no PSRAM)
- Firmware: ESP32_GENERIC_S3
- Tools: esptool, mpremote
- Editor: Any editor + terminal

---

## 📌 Quick Recovery
```bash
esptool erase-flash
esptool write-flash 0 firmware.bin
mpremote connect auto repl
```

---

## 🚀 Project Structure

```
esp32s3_setup/
├── README.md                 # This file
├── requirements.txt           # Python dependencies
├── src/                      # MicroPython source files
│   ├── main.py              # Main application entry point
│   ├── boot.py              # Boot configuration
│   ├── config.py            # Device configuration
│   └── lib/                 # Custom libraries
│       └── __init__.py
├── examples/                 # Example code snippets
│   ├── blink.py             # LED blink example
│   ├── wifi.py              # WiFi connection example
│   └── sensors/             # Sensor examples
└── docs/                     # Additional documentation
    └── pinout.md            # Pin reference
```

---

## 🛠️ Usage

1. **Install**: `pip install --upgrade esptool mpremote`
2. **Download firmware**: Get .bin from https://micropython.org/download/ESP32_GENERIC_S3/
3. **Flash**: `esptool erase-flash && esptool write-flash 0 firmware.bin`
4. **Upload**: Use the commands in "4️⃣ Upload project files" above
5. **Develop**: `mpremote connect auto repl`

---

## 📚 Development Tips

- Use `mpremote connect auto repl` for interactive development
- Test code in REPL before uploading
- Keep `main.py` minimal for faster boot times
- Use `config.py` for device-specific settings
- Store reusable code in the `lib/` directory

---

## 🧾 Fortune Slip Bitmap (Known-Good)

This project prints **pre-rendered bitmap slips** (no dynamic text rendering). The ESP32 chooses a random bitmap module listed in `config.FORTUNE_SLIP_MODULES`.

To generate a fortune slip bitmap that prints correctly on this setup (confirmed-good parameters):

```bash
python3 tools/render_fortune_slip.py \
  --text "You cannot shake hands with a clenched fist." \
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

Preview locally:

```bash
python3 tools/preview_fortune_slip.py
```

Upload to the ESP32 and reboot:

```bash
mpremote connect auto fs cp src/fortune_slip_bitmap_006.py :fortune_slip_bitmap_006.py
mpremote connect auto reset
```

Add it to the pool in `src/config.py`:

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
