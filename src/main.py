"""
ESP32-S3 Main Application
Entry point for the MicroPython application
"""

import config
from machine import Pin
import time
import neopixel
import machine

def main():
    """Main application loop"""
    print(f"Starting {config.DEVICE_NAME}...")
    print(f"Version: {config.VERSION}")
    print(f"Free memory: {get_free_memory()} bytes")
    
    # Initialize NeoPixel and boot button
    np = neopixel.NeoPixel(Pin(config.LED_PIN), 1)
    boot_pin = Pin(0, Pin.IN, Pin.PULL_UP)
    
    try:
        while True:
            if boot_pin.value() == 0:  # Boot button pressed
                # Light up NeoPixel when button held
                np[0] = (255, 255, 255)  # White
                np.write()
                print("Boot button pressed - LED ON")
            else:
                # Normal cycling when button released
                colors = [(5, 5, 5), (0, 5, 0), (0, 0, 5)]
                for color in colors:
                    if boot_pin.value() == 0:  # Check button during cycle
                        break
                    np[0] = color
                    np.write()
                    time.sleep(0.5)
                    machine.idle()
            
            time.sleep(0.1)  # Small delay to prevent overwhelming
            
    except Exception as e:
        print(f"LED error: {e}")


def get_free_memory():
    """Get free memory in bytes"""
    import gc
    gc.collect()
    return gc.mem_free()

if __name__ == "__main__":
    main()
