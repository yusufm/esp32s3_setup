"""
Thermal Printer Driver for ESP32-S3
Supports GOOJPRT QR203 and similar 58mm thermal printers
"""

import config
from machine import UART, Pin
import time

class ThermalPrinter:
    """Thermal printer driver class"""
    
    # Printer control commands
    ESC = b'\x1b'
    GS = b'\x1d'
    
    # Text formatting commands
    JUSTIFY_LEFT = ESC + b'a' + bytes([0])
    JUSTIFY_CENTER = ESC + b'a' + bytes([1])
    JUSTIFY_RIGHT = ESC + b'a' + bytes([2])
    
    FONT_SIZE_NORMAL = ESC + b'!' + bytes([0])
    FONT_SIZE_DOUBLE_HEIGHT = ESC + b'!' + bytes([16])
    FONT_SIZE_DOUBLE_WIDTH = ESC + b'!' + bytes([32])
    FONT_SIZE_DOUBLE_BOTH = ESC + b'!' + bytes([48])
    
    BOLD_ON = ESC + b'E' + bytes([1])
    BOLD_OFF = ESC + b'E' + bytes([0])
    
    UNDERLINE_ON = ESC + b'-' + bytes([1])
    UNDERLINE_OFF = ESC + b'-' + bytes([0])
    
    # Line spacing
    LINE_SPACING_DEFAULT = ESC + b'2'
    LINE_SPACING_24 = ESC + b'3' + bytes([24])
    
    # Feed and cut commands
    FEED_1_LINE = ESC + b'd' + bytes([1])
    FEED_3_LINES = ESC + b'd' + bytes([3])
    FEED_N_LINES = ESC + b'd'  # + n
    
    def __init__(self, uart_id=None, tx_pin=None, rx_pin=None, baudrate=None):
        """Initialize thermal printer"""
        if not config.THERMAL_PRINTER_ENABLED:
            raise RuntimeError("Thermal printer is disabled in config")
            
        self.uart_id = uart_id or config.UART_ID
        self.tx_pin = tx_pin or config.UART_TX_PIN
        self.rx_pin = rx_pin or config.UART_RX_PIN
        self.baudrate = baudrate or config.UART_BAUDRATE
        
        try:
            self.uart = UART(
                self.uart_id,
                baudrate=self.baudrate,
                tx=self.tx_pin,
                rx=self.rx_pin,
                timeout=config.UART_TIMEOUT
            )
            self.init_printer()
            print(f"Thermal printer initialized on UART{self.uart_id}")
        except Exception as e:
            print(f"Failed to initialize thermal printer: {e}")
            raise
    
    def init_printer(self):
        """Initialize printer with default settings"""
        self.write(self.LINE_SPACING_DEFAULT)
        self.write(self.JUSTIFY_LEFT)
        self.write(self.FONT_SIZE_NORMAL)
        self.write(self.BOLD_OFF)
        self.write(self.UNDERLINE_OFF)
        time.sleep(0.1)
    
    def write(self, data):
        """Write data to printer"""
        if isinstance(data, str):
            data = data.encode('ascii')
        self.uart.write(data)
        time.sleep(0.01)  # Small delay for printer processing

    def set_absolute_position(self, dots):
        if dots < 0:
            dots = 0
        nL = dots & 0xFF
        nH = (dots >> 8) & 0xFF
        self.write(self.ESC + b'$' + bytes([nL, nH]))

    def bit_image_row(self, row_bytes, mode=0):
        if isinstance(row_bytes, list):
            row_bytes = bytes(row_bytes)
        n = len(row_bytes)
        nL = n & 0xFF
        nH = (n >> 8) & 0xFF
        self.write(self.ESC + b'*' + bytes([mode, nL, nH]) + row_bytes)

    def print_corner_blocks(self, block_width_px=16, rows=3, left_margin_dots=0, right_margin_dots=0):
        bytes_per_row = (block_width_px + 7) // 8
        row_bytes = bytes([0xFF] * bytes_per_row)
        right_pos = 384 - right_margin_dots - block_width_px
        if right_pos < 0:
            right_pos = 0
        for _ in range(rows):
            self.set_absolute_position(left_margin_dots)
            self.bit_image_row(row_bytes, mode=0)
            self.set_absolute_position(right_pos)
            self.bit_image_row(row_bytes, mode=0)
            self.write(b'\n')
    
    def print_text(self, text):
        """Print text line"""
        self.write(text + '\n')
    
    def print_line(self, text="", align="left"):
        """Print text with alignment"""
        if align == "center":
            self.write(self.JUSTIFY_CENTER)
        elif align == "right":
            self.write(self.JUSTIFY_RIGHT)
        else:
            self.write(self.JUSTIFY_LEFT)
        
        self.print_text(text)
        self.write(self.JUSTIFY_LEFT)  # Reset to left alignment
    
    def print_bold(self, text):
        """Print bold text"""
        self.write(self.BOLD_ON)
        self.print_text(text)
        self.write(self.BOLD_OFF)
    
    def print_double_height(self, text):
        """Print double height text"""
        self.write(self.FONT_SIZE_DOUBLE_HEIGHT)
        self.print_text(text)
        self.write(self.FONT_SIZE_NORMAL)
    
    def print_double_width(self, text):
        """Print double width text"""
        self.write(self.FONT_SIZE_DOUBLE_WIDTH)
        self.print_text(text)
        self.write(self.FONT_SIZE_NORMAL)
    
    def print_large(self, text):
        """Print double height and width text"""
        self.write(self.FONT_SIZE_DOUBLE_BOTH)
        self.print_text(text)
        self.write(self.FONT_SIZE_NORMAL)
    
    def print_underline(self, text):
        """Print underlined text"""
        self.write(self.UNDERLINE_ON)
        self.print_text(text)
        self.write(self.UNDERLINE_OFF)
    
    def print_separator(self, char='-', length=32):
        """Print separator line"""
        self.print_text(char * length)
    
    def feed(self, lines=1):
        """Feed paper lines"""
        if lines == 1:
            self.write(self.FEED_1_LINE)
        elif lines == 3:
            self.write(self.FEED_3_LINES)
        else:
            self.write(self.FEED_N_LINES + bytes([lines & 0xFF]))
    
    def test_print(self):
        """Print test pattern"""
        self.print_separator('=', 32)
        self.print_line("THERMAL PRINTER TEST", "center")
        self.print_separator('=', 32)
        self.feed(1)
        
        self.print_bold("ESP32-S3 Thermal Printer")
        self.print_text("GOOJPRT QR203 Compatible")
        self.feed(1)
        
        self.print_text("Font Size Tests:")
        self.print_text("Normal text")
        self.print_double_height("Double Height")
        self.print_double_width("Double Width")
        self.print_large("Double Both")
        self.print_underline("Underlined Text")
        self.feed(1)
        
        self.print_text("Alignment Tests:")
        self.print_line("Left aligned", "left")
        self.print_line("Center aligned", "center")
        self.print_line("Right aligned", "right")
        self.feed(1)
        
        self.print_separator('-', 32)
        self.print_text("Characters: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.print_text("          abcdefghijklmnopqrstuvwxyz")
        self.print_text("          0123456789 !@#$%^&*()")
        self.print_separator('-', 32)
        self.feed(3)
    
    def print_receipt(self, items, total, title="RECEIPT"):
        """Print simple receipt"""
        self.print_separator('=', 32)
        self.print_large(title)
        self.print_separator('=', 32)
        self.feed(1)
        
        for item in items:
            name = item.get('name', 'Unknown')
            price = item.get('price', 0.00)
            qty = item.get('qty', 1)
            line_total = price * qty
            
            # Format: Item name (right aligned price)
            item_text = f"{name}"
            price_text = f"${line_total:.2f}"
            
            # Simple formatting - print name then price on next line
            self.print_text(item_text)
            self.print_line(price_text, "right")
        
        self.print_separator('-', 32)
        self.print_bold(f"TOTAL: ${total:.2f}")
        self.print_separator('=', 32)
        self.feed(3)
    
    def clear_buffer(self):
        """Clear printer buffer (if supported)"""
        self.write(ESC + b'@')
        time.sleep(0.1)
    
    def print_bitmap(self, bitmap_data, width, height, mode='normal'):
        """
        Print a bitmap image
        bitmap_data: list of bytes representing the image (1 bit per pixel)
        width: image width in pixels (must be multiple of 8)
        height: image height in pixels
        mode: 'normal', 'double_height', 'double_width', or 'double_both'
        """
        # Validate dimensions
        if width % 8 != 0:
            raise ValueError("Width must be multiple of 8")
        
        # Set print mode
        if mode == 'double_height':
            self.write(ESC + b'!' + bytes([16]))
        elif mode == 'double_width':
            self.write(ESC + b'!' + bytes([32]))
        elif mode == 'double_both':
            self.write(ESC + b'!' + bytes([48]))
        else:
            self.write(ESC + b'!' + bytes([0]))
        
        # Send bitmap data line by line
        bytes_per_line = width // 8
        
        for y in range(height):
            # Extract line data
            line_start = y * bytes_per_line
            line_end = line_start + bytes_per_line
            line_data = bitmap_data[line_start:line_end]
            
            # Send line command
            nL = bytes_per_line & 0xFF
            nH = (bytes_per_line >> 8) & 0xFF
            self.write(ESC + b'*' + bytes([0, nL, nH]) + bytes(line_data))
            
            # Feed to next line
            self.write(b'\n')
            time.sleep(0.01)
        
        # Reset to normal mode
        self.write(ESC + b'!' + bytes([0]))
    
    def print_simple_image(self, image_type='heart'):
        """Print a simple predefined image"""
        if image_type == 'heart':
            # Simple 8x8 heart bitmap (8 bytes)
            heart_bitmap = [
                0x66,  # 01100110
                0xFF,  # 11111111
                0xFF,  # 11111111
                0xFF,  # 11111111
                0x7E,  # 01111110
                0x3C,  # 00111100
                0x18,  # 00011000
                0x00   # 00000000
            ]
            self.print_bitmap(heart_bitmap, 8, 8, 'double_both')
            
        elif image_type == 'smiley':
            # Simple 16x16 smiley face (32 bytes)
            smiley_bitmap = [
                0x3C, 0x00,  #     ****     
                0x42, 0x00,  #    *    *    
                0x81, 0x80,  #   *      *   
                0x81, 0x80,  #   *      *   
                0x81, 0x80,  #   *      *   
                0x42, 0x00,  #    *    *    
                0x3C, 0x00,  #     ****     
                0x00, 0x00,  #              
                0x18, 0x00,  #    **        
                0x24, 0x00,  #   *  *       
                0x42, 0x00,  #  *    *      
                0x81, 0x80,  # *      *     
                0x81, 0x80,  # *      *     
                0x81, 0x80,  # *      *     
                0x42, 0x00,  #  *    *      
                0x3C, 0x00   #   ****       
            ]
            self.print_bitmap(smiley_bitmap, 16, 16, 'normal')
            
        elif image_type == 'qr':
            # Simple 8x8 QR-like pattern
            qr_bitmap = [
                0xFF,  # 11111111
                0x81,  # 10000001
                0xBD,  # 10111101
                0xA5,  # 10100101
                0xA5,  # 10100101
                0xBD,  # 10111101
                0x81,  # 10000001
                0xFF   # 11111111
            ]
            self.print_bitmap(qr_bitmap, 8, 8, 'double_width')
        
        else:
            raise ValueError(f"Unknown image type: {image_type}")
    
    def print_text_with_image(self, text, image_type='heart'):
        """Print text with a small image beside it"""
        self.print_text(text)
        self.print_simple_image(image_type)
        self.feed(1)
