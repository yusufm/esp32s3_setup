"""Fortune cookie fortune printing for the thermal printer."""

import random

import config
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

    slip_modules = getattr(config, "FORTUNE_SLIP_MODULES", None)
    if not slip_modules:
        slip_modules = ["fortune_slip_bitmap"]

    module_name = random.choice(slip_modules)
    slip = __import__(module_name)
    print("fortune_cookie: using bitmap slip", module_name, slip.WIDTH, slip.HEIGHT)
    printer.print_bitmap(
        slip.BITMAP,
        slip.WIDTH,
        slip.HEIGHT,
        mode='normal'
    )
    printer.feed(6)

    if created_printer:
        return fortune

    return fortune
