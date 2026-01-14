"""
ESP32-S3 Main Application
Entry point for the MicroPython application
"""

import config
from machine import Pin
import time
import neopixel
import machine

# Import thermal printer if enabled
if config.THERMAL_PRINTER_ENABLED:
    try:
        from thermal_printer import ThermalPrinter
        import fortune_cookie
        THERMAL_PRINTER_AVAILABLE = True
    except ImportError as e:
        print(f"Warning: Thermal printer module not available: {e}")
        THERMAL_PRINTER_AVAILABLE = False
else:
    THERMAL_PRINTER_AVAILABLE = False

def main():
    """Main application loop"""
    print(f"Starting {config.DEVICE_NAME}...")
    print(f"Version: {config.VERSION}")
    print(f"Free memory: {get_free_memory()} bytes")
    
    # Initialize NeoPixel and boot button
    np = neopixel.NeoPixel(Pin(config.LED_PIN), 1)
    boot_pin = Pin(0, Pin.IN, Pin.PULL_UP)
    
    # Initialize thermal printer if available
    printer = None
    if THERMAL_PRINTER_AVAILABLE:
        try:
            printer = ThermalPrinter()
            print("Thermal printer initialized successfully")
        except Exception as e:
            print(f"Failed to initialize thermal printer: {e}")
            printer = None
    
    # # Print startup message if printer available
    # if printer:
    #     try:
    #         printer.print_separator('=', 32)
    #         printer.print_large("ESP32-S3 STARTUP")
    #         printer.print_separator('=', 32)
    #         printer.print_text(f"Device: {config.DEVICE_NAME}")
    #         printer.print_text(f"Version: {config.VERSION}")
    #         printer.print_text(f"Memory: {get_free_memory()} bytes")
    #         printer.print_text("Ready for operation!")
    #         printer.feed(3)
    #     except Exception as e:
    #         print(f"Failed to print startup message: {e}")

    last_boot_state = boot_pin.value()
    last_boot_press_time = 0
    
    try:
        while True:
            current_time = time.ticks_ms()

            boot_state = boot_pin.value()
            if boot_state == 0:  # Boot button pressed
                np[0] = (255, 255, 255)  # White
                np.write()

                if last_boot_state == 1 and time.ticks_diff(current_time, last_boot_press_time) > 500:
                    last_boot_press_time = current_time
                    print("Boot button pressed")

                    if printer:
                        print("Printing fortune cookie...")
                        try:
                            fortune_cookie.print_fortune(printer=printer)
                        except Exception as e:
                            print(f"Fortune cookie print failed: {e}")
                    else:
                        print("Thermal printer not available")
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

            last_boot_state = boot_state
            
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
