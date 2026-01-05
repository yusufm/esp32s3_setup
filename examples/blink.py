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
    
    try:
        # Example: RGB LED control
        np = neopixel.NeoPixel(Pin(config.LED_PIN), 1)
        colors = [(5, 0, 0), (0, 5, 0), (0, 0, 5)]
        
        while True:
            for color in colors:
                np[0] = color
                np.write()
                time.sleep(0.5)
                machine.idle()
    except Exception as e:
        print(f"LED error: {e}")


def get_free_memory():
    """Get free memory in bytes"""
    import gc
    gc.collect()
    return gc.mem_free()

if __name__ == "__main__":
    main()
