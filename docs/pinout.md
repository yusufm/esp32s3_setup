# ESP32-S3 Pin Reference

## GPIO Pins

The ESP32-S3 provides up to 45 GPIO pins, but availability depends on the specific board configuration.

### Common Pin Functions

| Pin | Function | Notes |
|-----|----------|-------|
| 0-21 | GPIO | General purpose I/O |
| 22-29 | GPIO | General purpose I/O |
| 30-37 | GPIO | General purpose I/O |
| 38-48 | GPIO | General purpose I/O |

### Special Pins

| Pin | Special Function | Usage |
|-----|------------------|-------|
| 0 | GPIO0 | Boot mode selection, pull-up |
| 1 | GPIO1 | TXD0 (UART0) |
| 2 | GPIO2 | Boot mode selection |
| 3 | GPIO3 | RXD0 (UART0) |
| 21 | GPIO21 | Default I2C SDA |
| 22 | GPIO22 | Default I2C SCL |
| 13 | GPIO13 | Common LED pin |

### I2C Pins

| Function | Default Pin | Alternative |
|----------|-------------|-------------|
| SCL | 22 | Any GPIO |
| SDA | 21 | Any GPIO |

### SPI Pins

| Function | Default Pin | Alternative |
|----------|-------------|-------------|
| MOSI | 13 | Any GPIO |
| MISO | 12 | Any GPIO |
| SCK | 14 | Any GPIO |
| CS | 15 | Any GPIO |

### ADC Pins

The ESP32-S3 has ADC capabilities on specific pins:

| ADC Channel | GPIO Pin | Notes |
|-------------|----------|-------|
| ADC1_CH0 | GPIO1 | |
| ADC1_CH1 | GPIO2 | |
| ADC1_CH2 | GPIO3 | |
| ADC1_CH3 | GPIO4 | |
| ADC1_CH4 | GPIO5 | |
| ADC1_CH5 | GPIO6 | |
| ADC1_CH6 | GPIO7 | |
| ADC1_CH7 | GPIO8 | |
| ADC1_CH8 | GPIO9 | |
| ADC1_CH9 | GPIO10 | |

### DAC Pins

| DAC Channel | GPIO Pin | Notes |
|-------------|----------|-------|
| DAC1 | GPIO17 | 8-bit DAC |
| DAC2 | GPIO18 | 8-bit DAC |

### Touch Sensor Pins

| Touch Channel | GPIO Pin | Notes |
|----------------|----------|-------|
| T0 | GPIO1 | |
| T1 | GPIO2 | |
| T2 | GPIO3 | |
| T3 | GPIO4 | |
| T4 | GPIO5 | |
| T5 | GPIO6 | |
| T6 | GPIO7 | |
| T7 | GPIO8 | |
| T8 | GPIO9 | |
| T9 | GPIO10 | |

## UART Pins

### UART0
- TX: GPIO1
- RX: GPIO3

### UART1
- TX: GPIO17
- RX: GPIO16

### UART2
- TX: GPIO15
- RX: GPIO13

## USB Pins

The ESP32-S3 has native USB support:
- USB_D+: GPIO19
- USB_D-: GPIO20

## Strapping Pins

These pins affect boot behavior:
- GPIO0: Pull high for normal boot, low for flash download
- GPIO2: Pull high for normal boot
- GPIO5: Pull high for normal boot

## Power Pins

- 3V3: 3.3V power output
- GND: Ground
- VIN: Input voltage (5V recommended)

## Board-Specific Notes

Different ESP32-S3 boards may have different pin configurations:

### DevKit Boards
- Built-in LED usually on GPIO13
- Boot button on GPIO0
- EN pin for reset

### Compact Boards
- May have limited GPIO access
- Check board documentation for specific pin assignments

## Usage Tips

1. **Always check board documentation** for specific pin assignments
2. **Avoid using strapping pins** for general I/O when possible
3. **Consider pin limitations** - some pins have special behaviors
4. **Use pull-up/pull-down resistors** for input pins as needed
5. **Check voltage levels** - ESP32-S3 is 3.3V logic

## Example Pin Usage

```python
from machine import Pin, I2C, SPI

# LED blink
led = Pin(13, Pin.OUT)

# I2C setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# SPI setup
spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

# Button input
button = Pin(0, Pin.IN, Pin.PULL_UP)
```
