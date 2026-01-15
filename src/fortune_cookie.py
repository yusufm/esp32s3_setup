"""Fortune cookie fortune printing for the thermal printer."""

import random

import config
from thermal_printer import ThermalPrinter

FORTUNES = [
    "You will commit a very small crime against productivity.",
    "Today's plan is mostly 'we'll see.'",
    "Something silly works suspiciously well.",
    "You are running on confidence and snacks.",
    "A bad idea shows up wearing a fun hat.",
    "You will laugh at the wrong moment. It improves the moment.",
    "Mischief checks your calendar and moves in.",
    "You pretend this was the plan the whole time.",
    "A tiny chaos goblin applauds your choices.",
    "You accidentally start a joke that lasts all day.",
    "Today has strong 'oops, fun' energy.",
    "You are doing bits. Everyone notices.",
    "A shortcut leads somewhere unexpected but delightful.",
    "You break nothing important. Probably.",
    "Your seriousness takes the day off.",
    "You will say 'watch this' and survive.",
    "Something dumb becomes your favorite part.",
    "The vibes are doing the steering now.",
    "You win by being lightly ridiculous.",
    "This fortune is giggling and refuses to explain.",
    "A silly detour improves the plot.",
    "You misjudge something—in a funny way.",
    "Today's energy is 'confident shrug.'",
    "You trip over nothing and land in a good mood.",
    "A joke you don't tell is still funny.",
    "You are accidentally the fun one today.",
    "A harmless rule looks the other way.",
    "You will clap for yourself internally.",
    "Something minor becomes extremely amusing.",
    "You get away with it because no one's mad.",
    "You are doing just enough. Miraculous.",
    "Today is powered by mild chaos.",
    "A tiny win demands a tiny celebration.",
    "You smile first and figure it out later.",
    "A nonsense idea improves morale.",
    "You are underqualified but enthusiastic. Perfect.",
    "Someone laughs because of you. Success.",
    "You misunderstand something and it helps.",
    "The moment is funnier than expected.",
    "This was not on the agenda. Nice.",
    "You will make a sound effect for no reason.",
    "A dramatic pause goes unanswered. Still satisfying.",
    "You choose the fun option. Again.",
    "Today's confidence is mostly pretend. It works.",
    "A joke lands sideways and that's better.",
    "You nod like you meant that.",
    "Something works despite your involvement.",
    "You survive a 'why did I do that?' moment.",
    "A small chaos sparkles briefly.",
    "You laugh, then pretend you didn't.",
    "You are lightly unserious on purpose.",
    "A plan changes hats mid-sentence.",
    "You take a risk the size of a peanut.",
    "Today's logic is on vacation.",
    "You confuse enthusiasm with competence. Still fine.",
    "A silly choice ages well.",
    "You almost behave. Almost.",
    "Something funny sneaks past you.",
    "You improvise confidently and exit.",
    "The mood improves for unclear reasons.",
    "You are accidentally charming.",
    "A non-problem becomes a joke.",
    "You forget what you were worried about.",
    "A tiny rebellion goes unnoticed.",
    "You celebrate too early. Still counts.",
    "Something feels wrong but fun.",
    "You commit to the bit.",
    "Today has excellent side-quest energy.",
    "You confuse everyone briefly. Delightful.",
    "A shortcut turns scenic.",
    "You leave things slightly better and sillier.",
    "A moment deserves jazz hands.",
    "You grin and no one asks questions.",
    "Something dumb pays off immediately.",
    "You pretend you're not pleased.",
    "The vibes approve.",
    "You do a little victory nod.",
    "A weird idea clocks in early.",
    "You laugh at your own timing.",
    "This fortune is proud of you.",
    "You make it work by winging it.",
    "A tiny surprise improves your day.",
    "You accidentally pick the right song.",
    "Today is going off-script.",
    "You enjoy the confusion.",
    "A joke lives rent-free all afternoon.",
    "You break the ice by slipping on it.",
    "Something small becomes legendary (to you).",
    "You do not explain yourself. Correct.",
    "This counts as a win.",
    "You are doing fine. Suspiciously fine.",
    "A nonsense decision feels correct.",
    "You laugh before you understand.",
    "Today's success is mostly vibes.",
    "You cause joy without documentation.",
    "A little chaos improves the flavor.",
    "You survive entirely on 'eh, why not.'",
    "You do the funny version.",
    "Everything is okay enough.",
    "This fortune high-fives you and vanishes.",
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
