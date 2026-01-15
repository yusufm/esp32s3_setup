#!/usr/bin/env python3
"""
Generate fortune slip bitmaps with lucky numbers
"""

import argparse
import random
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import fortunes directly to avoid MicroPython dependencies
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

from render_fortune_slip import main as render_slip


def get_fortune_with_lucky_numbers(fortune_text):
    """Add lucky numbers to a fortune."""
    lucky_numbers = sorted(random.sample(range(1, 100), 6))
    return f"{fortune_text}\n\nLucky numbers: {', '.join(map(str, lucky_numbers))}"


def generate_all_fortunes(font_path, output_dir="src"):
    """Generate bitmap files for all fortunes with lucky numbers."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate fortune slips
    for i, fortune in enumerate(FORTUNES):
        fortune_with_numbers = get_fortune_with_lucky_numbers(fortune)
        
        # Generate filename
        if i == 0:
            filename = "fortune_slip_bitmap.py"
        else:
            filename = f"fortune_slip_bitmap_{i:03d}.py"
        
        outfile = output_path / filename
        
        # Call render_slip with the fortune text using known-good parameters
        sys.argv = [
            "render_fortune_slip.py",
            "--text", fortune_with_numbers,
            "--font", font_path,
            "--width", "650",
            "--height", "364", 
            "--rotate", "90",
            "--auto_size",
            "--size_min", "24",
            "--size_max", "80",
            "--margin", "0.04",
            "--out", str(outfile)
        ]
        
        try:
            render_slip()
            print(f"Generated: {outfile}")
        except Exception as e:
            print(f"Error generating {outfile}: {e}")
    
    print(f"\nGenerated {len(FORTUNES)} fortune slip bitmaps")
    print("Update config.FORTUNE_SLIP_MODULES to include the new files")


def main():
    parser = argparse.ArgumentParser(description="Generate fortune slip bitmaps with lucky numbers")
    parser.add_argument("--font", required=True, help="Path to .ttf font file")
    parser.add_argument("--output", default="src", help="Output directory (default: src)")
    parser.add_argument("--count", type=int, help="Generate only this many fortunes (for testing)")
    
    args = parser.parse_args()
    
    if args.count:
        # Temporarily limit fortunes for testing
        global FORTUNES
        FORTUNES = FORTUNES[:args.count]
    
    generate_all_fortunes(args.font, args.output)


if __name__ == "__main__":
    main()
