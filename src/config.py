"""
ESP32-S3 Device Configuration
Central configuration for hardware and application settings
"""

# Device information
DEVICE_NAME = "ESP32-S3"
VERSION = "1.0.0"

# System configuration
CPU_FREQUENCY = 240  # MHz (max for ESP32-S3)

# Pin configuration
LED_PIN = 48  # NeoPixel RGB LED pin

# Lid reed switch configuration
LID_SWITCH_PIN = 4
LID_SWITCH_DEBOUNCE_MS = 75
LID_MIN_PRINT_INTERVAL_MS = 5000
LID_CLOSED_STABLE_MS = 1000

# GPIO pin definitions
GPIO_PINS = {
    'D0': 0,
    'D1': 1,
    'D2': 2,
    'D3': 3,
    'D4': 4,
    'D5': 5,
    'D6': 6,
    'D7': 7,
    'D8': 8,
    'D9': 9,
    'D10': 10,
    'D11': 11,
    'D12': 12,
    'D13': 13,
    'D14': 14,
    'D15': 15,
    'D16': 16,
    'D17': 17,
    'D18': 18,
    'D19': 19,
    'D20': 20,
    'D21': 21,
}

# I2C configuration (set I2C_ENABLED = True to enable)
I2C_ENABLED = False
I2C_SCL = 22  # I2C clock pin
I2C_SDA = 21  # I2C data pin

# SPI configuration (set SPI_ENABLED = True to enable)
SPI_ENABLED = False
SPI_ID = 1
SPI_BAUDRATE = 1000000  # 1 MHz
SPI_SCK = 14
SPI_MOSI = 13
SPI_MISO = 12

# WiFi configuration
WIFI_ENABLED = True
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Application settings
DEBUG = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Timing settings
LOOP_DELAY = 0.1  # seconds
WATCHDOG_TIMEOUT = 30000  # milliseconds

# Power management
DEEP_SLEEP_ENABLED = False
DEEP_SLEEP_DURATION = 60000  # milliseconds

# Sensor configuration
SENSOR_ENABLED = False
SENSOR_READ_INTERVAL = 5000  # milliseconds

# Network configuration
NTP_ENABLED = False
NTP_SERVER = "pool.ntp.org"
TIMEZONE_OFFSET = 0  # hours from UTC

# File system settings
ENABLE_WEBREPL = False
WEBREPL_PASSWORD = "password"

# UART configuration for thermal printer
UART_ENABLED = True
UART_ID = 1  # UART1 for thermal printer
UART_TX_PIN = 17  # ESP32 TX -> Printer RX
UART_RX_PIN = 16  # ESP32 RX -> Printer TX  
UART_BAUDRATE = 9600  # Common baudrate for thermal printers
UART_TIMEOUT = 1000  # milliseconds

# Thermal printer configuration
THERMAL_PRINTER_ENABLED = True
THERMAL_PRINTER_WIDTH = 58  # mm (58mm paper width)
THERMAL_PRINTER_CHARS_PER_LINE = 32  # Approximate characters per line

# Fortune slip bitmap modules (pre-rendered). Each module must export WIDTH, HEIGHT, BITMAP.
# Example: ["fortune_slip_bitmap", "fortune_slip_bitmap_002"]
FORTUNE_SLIP_MODULES = [
    "fortune_slip_bitmap",
] + [f"fortune_slip_bitmap_{i:03d}" for i in range(1, 33)]

# Development settings
AUTO_RELOAD = True
REPL_ON_BOOT = False
