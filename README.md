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
- **Important**: Use the release that does **NOT** have "(Support for Octal-SPIRAM)" in the name
- Do **NOT** use `_PSRAM` firmware unless you are certain your board has PSRAM

---

## 3️⃣ Flash firmware
```bash
esptool erase-flash
esptool write-flash 0 ESP32_GENERIC_S3-*.bin
```

---

## 4️⃣ Upload project files
```bash
mpremote connect auto cp -r . :
mpremote reset
```

**Note:** If the board gets stuck in a boot loop, first remove main.py:
```bash
mpremote connect auto repl
>>> import os
>>> os.remove('main.py')
>>> os.remove('boot.py')
```
Then upload new files.

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
4. **Upload**: `mpremote connect auto cp -r . : && mpremote reset`
5. **Develop**: `mpremote connect auto repl`

---

## 📚 Development Tips

- Use `mpremote connect auto repl` for interactive development
- Test code in REPL before uploading
- Keep `main.py` minimal for faster boot times
- Use `config.py` for device-specific settings
- Store reusable code in the `lib/` directory
