#!/usr/bin/env python3
"""
Preview Fortune Slip Image
Displays the fortune slip bitmap that will be printed on the thermal printer
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from PIL import Image

def preview_fortune_slip():
    """Load and display the fortune slip bitmap"""
    try:
        import fortune_slip_bitmap
        
        width = fortune_slip_bitmap.WIDTH
        height = fortune_slip_bitmap.HEIGHT
        bitmap_data = fortune_slip_bitmap.BITMAP
        
        print(f"Fortune Slip Dimensions: {width}x{height} pixels")
        print(f"Bitmap data size: {len(bitmap_data)} bytes")
        print(f"Expected size: {(width * height) // 8} bytes")
        
        # Create image from bitmap data
        img = Image.new('1', (width, height), 1)  # 1-bit image, white background
        pixels = img.load()
        
        # Convert bitmap bytes to pixels
        byte_idx = 0
        for y in range(height):
            for x in range(0, width, 8):
                if byte_idx >= len(bitmap_data):
                    break
                byte_val = bitmap_data[byte_idx]
                byte_idx += 1
                
                # Extract 8 pixels from this byte
                for bit in range(8):
                    if x + bit < width:
                        # Bit 7 is leftmost pixel
                        pixel_val = (byte_val >> (7 - bit)) & 1
                        # 1 = black, 0 = white in our bitmap
                        pixels[x + bit, y] = 0 if pixel_val else 1
        
        # Save preview image
        output_path = Path(__file__).parent / "fortune_slip_preview.png"
        img.save(output_path)
        print(f"\n✓ Preview saved to: {output_path}")
        
        # Display image
        try:
            img.show()
            print("✓ Image opened in default viewer")
        except Exception as e:
            print(f"Note: Could not auto-open image: {e}")
            print(f"Please open manually: {output_path}")
        
        return True
        
    except ImportError as e:
        print(f"Error: Could not import fortune_slip_bitmap: {e}")
        print("Make sure fortune_slip_bitmap.py exists in the src/ directory")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Fortune Slip Preview Tool ===\n")
    
    if preview_fortune_slip():
        print("\n✓ Success! The image above shows what will be printed.")
        print("  The fortune slip will print vertically (portrait mode)")
        print("  on the thermal printer.")
    else:
        print("\n✗ Failed to generate preview")
        sys.exit(1)

if __name__ == "__main__":
    main()
