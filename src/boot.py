"""
ESP32-S3 Boot Configuration
This file runs automatically when the device boots
"""

import config
import machine
from machine import Pin
import time

# Configure system clock and frequency
machine.freq(config.CPU_FREQUENCY * 1000000)  # Convert MHz to Hz

# Disable auto-deepsleep for better debugging
# machine.deepsleep() can be called manually when needed

# Initialize hardware components
def init_hardware():
    """Initialize hardware components"""
    # Configure pins
    if hasattr(config, 'INIT_PINS'):
        for pin_config in config.INIT_PINS:
            pin = Pin(pin_config['pin'], pin_config['mode'])
            if 'value' in pin_config:
                pin.value(pin_config['value'])
    
    # Initialize I2C if configured
    if hasattr(config, 'I2C_ENABLED') and config.I2C_ENABLED:
        from machine import I2C
        config.I2C = I2C(config.I2C_SCL, config.I2C_SDA)
    
    # Initialize SPI if configured
    if hasattr(config, 'SPI_ENABLED') and config.SPI_ENABLED:
        from machine import SPI
        config.SPI = SPI(config.SPI_ID, 
                         baudrate=config.SPI_BAUDRATE,
                         sck=config.SPI_SCK,
                         mosi=config.SPI_MOSI,
                         miso=config.SPI_MISO)

# Run hardware initialization
init_hardware()

# Print boot information
print(f"\n=== {config.DEVICE_NAME} Boot ===")
print(f"Version: {config.VERSION}")
print(f"CPU Frequency: {config.CPU_FREQUENCY} MHz")
print(f"Boot time: {time.ticks_ms()} ms")

# Safety hatch: when BOOT button is held during reset, skip running the main app.
# Note: MicroPython automatically runs main.py after boot.py, so boot.py must NOT
# import/run main itself (that can make the device hard to update over mpremote).
boot_pin = Pin(0, Pin.IN, Pin.PULL_UP)
config.SKIP_MAIN = (boot_pin.value() == 0)
if config.SKIP_MAIN:
    print("Boot mode detected - skipping main.py")
