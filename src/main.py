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
    
    # Initialize NeoPixel and lid switch
    np = neopixel.NeoPixel(Pin(config.LED_PIN), 1)
    lid_pin = Pin(config.LID_SWITCH_PIN, Pin.IN, Pin.PULL_UP)
    
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

    last_lid_state = lid_pin.value()
    last_lid_event_time = 0
    last_print_time = 0
    lid_ready_for_open = (last_lid_state == 0)
    lid_closed_since = None
    last_led_state = None
    
    try:
        while True:
            current_time = time.ticks_ms()

            lid_state = lid_pin.value()
            if lid_state == 1:  # Lid open
                lid_closed_since = None
                if last_led_state != 1:
                    np[0] = (0, 26, 0)
                    np.write()
                    last_led_state = 1

                if (
                    lid_ready_for_open
                    and last_lid_state == 0
                    and time.ticks_diff(current_time, last_lid_event_time) > config.LID_SWITCH_DEBOUNCE_MS
                ):
                    last_lid_event_time = current_time
                    lid_ready_for_open = False

                    if time.ticks_diff(current_time, last_print_time) >= config.LID_MIN_PRINT_INTERVAL_MS:
                        last_print_time = current_time
                        print("Lid opened")

                        if printer:
                            print("Printing fortune cookie...")
                            try:
                                fortune_cookie.print_fortune(printer=printer)
                            except Exception as e:
                                print(f"Fortune cookie print failed: {e}")
                        else:
                            print("Thermal printer not available")
                    else:
                        print("Lid opened (cooldown active - not printing)")
            else:
                # Normal cycling when button released
                if last_led_state != 0:
                    np[0] = (0, 0, 26)
                    np.write()
                    last_led_state = 0

                if not lid_ready_for_open:
                    if lid_closed_since is None:
                        if last_lid_state == 1 and time.ticks_diff(current_time, last_lid_event_time) > config.LID_SWITCH_DEBOUNCE_MS:
                            last_lid_event_time = current_time
                            lid_closed_since = current_time
                            print("Lid closed")
                    else:
                        if time.ticks_diff(current_time, lid_closed_since) >= getattr(config, "LID_CLOSED_STABLE_MS", 1000):
                            lid_ready_for_open = True

            last_lid_state = lid_state
            
            time.sleep(0.1)  # Small delay to prevent overwhelming
            
    except Exception as e:
        print(f"LED error: {e}")


def get_free_memory():
    """Get free memory in bytes"""
    import gc
    gc.collect()
    return gc.mem_free()

if __name__ == "__main__":
    if getattr(config, "SKIP_MAIN", False):
        print("main.py: SKIP_MAIN is set - not starting main loop")
    else:
        main()
