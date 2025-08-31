import curses
import random
import time
import json
from STWordsList import diff1, diff2, diff3, diff4, diff5

diff_words = {
    1: diff1,
    2: diff2, 
    3: diff3,
    4: diff4,
    5: diff5
}
options = [
    "Normal - 1x Points",
    "Seasoned - 2x Points", 
]

upgrades = [
    {"name": "Extra Time", "description": "Increase time limit by 5 seconds"},
    {"name": "More Points", "description": "Increase your point gain"},
    {"name": "Fewer Words", "description": "Decrease number of words per stage"},
    {"name": "Slower Difficulty Increase", "description": "Difficulty increases more slowly"},
    {"name": "Triple Trouble", "description": "Next upgrade gives 3x its effects"}
]
extra_time = 0
more_points = 0
fewer_words = 0
slower_difficulty = 0
triple_trouble = 0

def choose_upgrade(stdscr, available_upgrades):
    """
    Displays an upgrade selection screen. User selects one upgrade.
    available_upgrades: list of upgrade dicts
    Returns the chosen upgrade.
    """
    # Pick 3 random upgrades from the list
    upgrades_to_choose = random.sample(available_upgrades, 3)
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose your upgrade (Use ↑↓ arrows, Enter to select)")

        for i, upgrade in enumerate(upgrades_to_choose):
            line = f"{upgrade['name']}: {upgrade['description']}"
            if i == current_selection:
                stdscr.addstr(i + 2, 0, f"> {line} <", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, f"  {line}  ")

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(upgrades_to_choose) - 1:
            current_selection += 1
        elif key == 10:  # Enter key
            return upgrades_to_choose[current_selection]
        elif key == 27:  # ESC key
            return None

def play_stage(stdscr, stage, selected_difficulty, score):
    # Increase difficulty every 3 stages, capped at diff5
    if slower_difficulty > 0:
        word_difficulty = min(1 + ((stage - 1) // (3 + slower_difficulty)), 5)
    else:
        word_difficulty = min(1 + (stage // 3), 5)
    words = random.choices(diff_words[word_difficulty], k=max(1, 10-fewer_words))

    # Time limit shrinks every stage, but not below 10s
    base_time = 30
    if selected_difficulty == 1:
        time_limit = max(10, base_time * 1.5 - (stage - 1) + (extra_time * 5))
    else:
        time_limit = max(10, base_time - (stage - 1) + (extra_time * 5))

    current_word_index = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while current_word_index < len(words):
        current_word = words[current_word_index]
        typed_text = ""
        word_start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            time_left = max(0, time_limit - elapsed_time)

            stdscr.clear()
            stdscr.addstr(0, 0, f"Stage: {stage}")
            stdscr.addstr(1, 0, f"Score: {score:.1f}")
            stdscr.addstr(2, 0, f"Time left: {time_left:.1f} seconds")
            stdscr.addstr(4, 0, f"Type this word: {current_word}")
            stdscr.addstr(6, 0, f"Your input: {typed_text}")
            stdscr.addstr(8, 0, "Press ESC to quit at any time.")
            stdscr.refresh()

            # Check if time ran out
            if time_left <= 0:
                return score, False  # Game over

            char = stdscr.getch()
            if char == -1:
                continue
            if char == 27:  # ESC
                return score, False
            if char in (curses.KEY_BACKSPACE, 127):
                typed_text = typed_text[:-1]
            else:
                typed_text += chr(char)

            # Word completed correctly
            if typed_text == current_word:
                word_elapsed = time.time() - word_start_time
                multiplier = 1 + 0.5 * more_points
                score += (10 * selected_difficulty * multiplier) / (word_elapsed + 1)

                current_word_index += 1
                break
            # Wrong input, trim
            elif not current_word.startswith(typed_text):
                typed_text = typed_text[:-1]

    return score, True  # Stage completed

def main(stdscr):
    # Initialize curses settings
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    
    # Display initial messages
    stdscr.addstr(0, 0, "Speed Typer Game")
    stdscr.addstr(1, 0, "Instructions: Type the words as fast and accurately as you can.")
    stdscr.addstr(2, 0, "Press any key to start...")
    stdscr.refresh()
    stdscr.getch()

    # Start section - DIFFICULTY MENU
    stdscr.clear()
    current_selection = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select Difficulty (Use ↑↓ arrows, Enter to select)")
        
        # Display options with highlighting
        for i, option in enumerate(options):
            if i == current_selection:
                stdscr.addstr(i + 2, 0, f"> {option} <", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, f"  {option}  ")
        
        stdscr.refresh()
        
        # Get user input
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(options) - 1:
            current_selection += 1
        elif key == 10:  # Enter key
            selected_difficulty = current_selection + 1
            break
        elif key == 27:  # ESC key
            selected_difficulty = None
            break
    
    # Only after breaking from the menu loop does the countdown start
    if selected_difficulty is not None:
        # Countdown
        for i in range(5, 0, -1):
            stdscr.clear()
            stdscr.addstr(0, 0, f"Starting in {i}...")
            stdscr.addstr(1, 0, "Get Ready!")
            stdscr.addstr(2, 0, "Type the following words as fast and accurately as you can!")
            stdscr.refresh()
            time.sleep(1)

        # Start stages after countdown
        stage = 1
        score = 0

        while True:
            score, survived = play_stage(stdscr, stage, selected_difficulty, score)

            if not survived:  # Player quit or time ran out
                stdscr.clear()
                stdscr.addstr(0, 0, f"Game Over! Final Score: {score:.1f}")
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                break

            # Upgrade every 5 stages
            if stage % 5 == 0 or stage == 1:
                chosen_upgrade = choose_upgrade(stdscr, upgrades)
                stdscr.clear()
                if chosen_upgrade:
                    stdscr.addstr(0, 0, f"You chose: {chosen_upgrade['name']} - {chosen_upgrade['description']}")
                    stdscr.refresh()
                    time.sleep(3)

                    global extra_time, more_points, fewer_words, slower_difficulty, triple_trouble
                    name = chosen_upgrade['name']
    
                    if name == "Triple Trouble":
                        triple_trouble += 1
                    else:
                        multiplier = 3 if triple_trouble > 0 else 1

                        if name == "Extra Time":
                            extra_time += 1 * multiplier
                        elif name == "More Points":
                            more_points += 1 * multiplier
                        elif name == "Fewer Words":
                            fewer_words += 1 * multiplier
                        elif name == "Slower Difficulty Increase":
                            slower_difficulty += 1 * multiplier

                        triple_trouble = 0  # Reset after applying

                else:
                    stdscr.addstr(0, 0, "No upgrade chosen.")
                stdscr.addstr(2, 0, "Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()

    
            # Stage transition countdown
            next_upgrade = 5 - (stage % 5)
            stdscr.clear()
            stdscr.addstr(0, 0, f"Stage {stage} complete! Score: {score:.1f}")
            stdscr.addstr(1, 0, f"Next upgrade in {next_upgrade} stages.")
            for i in range(5, 0, -1):
                stdscr.addstr(3, 0, f"Next stage in {i}...")
                stdscr.refresh()
                time.sleep(1)

            stage += 1




# Start the curses application
curses.wrapper(main)