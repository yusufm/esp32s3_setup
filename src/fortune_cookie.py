"""Fortune cookie fortune printing for the thermal printer."""

import random

from thermal_printer import ThermalPrinter

FORTUNES = [
    "You cannot shake hands with a clenched fist.",
    "Perhaps you will forget tomorrow the kind words you say today, but the recipient may cherish them over a lifetime.",
    "A surprise gift will be yours.",
    "Your hard work will pay off soon.",
    "Adventure awaits around the corner.",
    "Good things come to those who wait.",
]


def wrap_text(text, max_chars_per_line=28):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def print_fortune(printer=None, fortune=None):
    """Print a single authentic-style fortune slip.

    If printer is not provided, one will be created.
    """
    created_printer = False
    if printer is None:
        printer = ThermalPrinter()
        created_printer = True

    if fortune is None:
        fortune = random.choice(FORTUNES)

    try:
        import fortune_slip_bitmap
        print("fortune_cookie: using bitmap slip", fortune_slip_bitmap.WIDTH, fortune_slip_bitmap.HEIGHT)
        printer.print_bitmap(
            fortune_slip_bitmap.BITMAP,
            fortune_slip_bitmap.WIDTH,
            fortune_slip_bitmap.HEIGHT,
            mode='normal'
        )
        printer.feed(6)
    except Exception as e:
        print("fortune_cookie: bitmap slip unavailable, falling back to text. error=", repr(e))
        lines = wrap_text(fortune, max_chars_per_line=28)

        printer.feed(2)
        printer.print_corner_blocks(block_width_px=18, rows=2)
        printer.feed(1)

        printer.write(printer.FONT_SIZE_DOUBLE_HEIGHT)
        for line in lines:
            printer.print_line(line, "center")
        printer.write(printer.FONT_SIZE_NORMAL)

        printer.feed(1)
        printer.print_corner_blocks(block_width_px=18, rows=2)

        pad_lines = 18 - (len(lines) * 2)
        if pad_lines < 8:
            pad_lines = 8
        printer.feed(pad_lines)

    if created_printer:
        return fortune

    return fortune
