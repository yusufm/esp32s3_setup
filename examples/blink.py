"""
LED Blink Example
Simple example to blink an LED on the ESP32-S3
"""

from machine import Pin
import time

# Configuration
LED_PIN = 13  # Change to match your board's LED pin
BLINK_INTERVAL = 0.5  # seconds

def main():
    """Blink LED continuously"""
    led = Pin(LED_PIN, Pin.OUT)
    
    print(f"Blinking LED on pin {LED_PIN}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            led.on()
            time.sleep(BLINK_INTERVAL)
            led.off()
            time.sleep(BLINK_INTERVAL)
    except KeyboardInterrupt:
        print("Stopped by user")
        led.off()

if __name__ == "__main__":
    main()
