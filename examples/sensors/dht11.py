"""
DHT11 Temperature and Humidity Sensor Example
Read temperature and humidity from DHT11 sensor
"""

from machine import Pin
import time

class DHT11:
    """DHT11 sensor driver"""
    
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_UP)
        self.temperature = 0
        self.humidity = 0
    
    def read(self):
        """Read temperature and humidity from sensor"""
        # Send start signal
        self.pin.value(1)
        time.sleep_ms(10)
        self.pin.value(0)
        time.sleep_ms(18)
        self.pin.value(1)
        time.sleep_us(40)
        
        # Switch to input mode
        self.pin.init(Pin.IN, Pin.PULL_UP)
        
        # Wait for sensor response
        timeout = 0
        while self.pin.value() == 1 and timeout < 100:
            time.sleep_us(1)
            timeout += 1
        
        if timeout >= 100:
            return False
        
        # Wait for sensor to pull low
        timeout = 0
        while self.pin.value() == 0 and timeout < 100:
            time.sleep_us(1)
            timeout += 1
        
        if timeout >= 100:
            return False
        
        # Read 40 bits of data
        data = []
        for _ in range(40):
            timeout = 0
            while self.pin.value() == 1 and timeout < 100:
                time.sleep_us(1)
                timeout += 1
            
            if timeout >= 100:
                return False
            
            # Measure bit length
            timeout = 0
            while self.pin.value() == 0 and timeout < 100:
                time.sleep_us(1)
                timeout += 1
            
            if timeout >= 100:
                return False
            
            # Count high time
            timeout = 0
            while self.pin.value() == 1 and timeout < 100:
                time.sleep_us(1)
                timeout += 1
            
            data.append(timeout > 40)  # Long pulse = 1, short pulse = 0
        
        # Convert bits to bytes
        humidity_int = 0
        humidity_dec = 0
        temp_int = 0
        temp_dec = 0
        checksum = 0
        
        for i in range(8):
            humidity_int = (humidity_int << 1) | data[i]
        for i in range(8, 16):
            humidity_dec = (humidity_dec << 1) | data[i]
        for i in range(16, 24):
            temp_int = (temp_int << 1) | data[i]
        for i in range(24, 32):
            temp_dec = (temp_dec << 1) | data[i]
        for i in range(32, 40):
            checksum = (checksum << 1) | data[i]
        
        # Verify checksum
        calc_checksum = humidity_int + humidity_dec + temp_int + temp_dec
        if calc_checksum & 0xFF != checksum:
            return False
        
        # Store values
        self.humidity = humidity_int + humidity_dec / 10
        self.temperature = temp_int + temp_dec / 10
        
        return True

def main():
    """Main DHT11 example"""
    # DHT11 data pin (connect to GPIO pin 4)
    dht_pin = 4
    
    dht = DHT11(dht_pin)
    
    print("DHT11 Temperature and Humidity Sensor")
    print("=" * 40)
    
    try:
        while True:
            if dht.read():
                print(f"Temperature: {dht.temperature:.1f}°C")
                print(f"Humidity: {dht.humidity:.1f}%")
                print()
            else:
                print("Failed to read from DHT11 sensor")
            
            time.sleep(2)  # DHT11 needs at least 2 seconds between reads
            
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()
