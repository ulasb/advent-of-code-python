"""
Advent of Code 2016, Day 10: Balance Bots

This script parses bot instructions to determine how bots handle chips.
Created and published by Ulaş Bardak.
This project is licensed under the Mozilla Public License 2.0 (MPL 2.0).
The MPL 2.0 is a copyleft license that allows you to use, modify, and distribute
the code, provided that you make the source code of any modifications available
under the same license.
"""

import sys
import re
from typing import Dict, List, Any, DefaultDict
from collections import defaultdict


def parse_input(
    filename: str = "input.txt",
) -> tuple[
    DefaultDict[int, List[int]], Dict[int, Dict[str, Any]], DefaultDict[int, List[int]]
]:
    """
    Parse the input file for bot instructions.

    Parameters
    ----------
    filename : str
        The path to the input file. Default is "input.txt".

    Returns
    -------
    tuple[DefaultDict[int, List[int]], Dict[int, Dict[str, Any]], DefaultDict[int, List[int]]]
        A tuple containing:
        - holding: DefaultDict keyed by bot ID with list of values.
        - directions: Dict keyed by bot ID with low/high target types and IDs.
        - outputs: DefaultDict keyed by output ID with list of values.
    """
    holding: DefaultDict[int, List[int]] = defaultdict(list)
    directions: Dict[int, Dict[str, Any]] = {}
    outputs: DefaultDict[int, List[int]] = defaultdict(list)

    # Regular expressions for the two patterns
    # 1) value X goes to bot Y
    value_pattern = re.compile(r"value (\d+) goes to bot (\d+)")
    # 2) bot X gives low to [bot|output] Y and high to [bot|output] Z
    direction_pattern = re.compile(
        r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)"
    )

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Pattern 1: value X goes to bot Y
            value_match = value_pattern.match(line)
            if value_match:
                val_x = int(value_match.group(1))
                bot_y = int(value_match.group(2))
                holding[bot_y].append(val_x)
                continue

            # Pattern 2: bot X gives low to Y and high to Z
            direction_match = direction_pattern.match(line)
            if direction_match:
                bot_x = int(direction_match.group(1))
                low_type = direction_match.group(2)
                low_id = int(direction_match.group(3))
                high_type = direction_match.group(4)
                high_id = int(direction_match.group(5))
                directions[bot_x] = {
                    "low": (low_type, low_id),
                    "high": (high_type, high_id),
                }
                continue

    return holding, directions, outputs


def execute_directions(
    holding: DefaultDict[int, List[int]],
    directions: Dict[int, Dict[str, Any]],
    outputs: DefaultDict[int, List[int]],
):
    """
    Execute the bot directions efficiently using a queue.

    Parameters
    ----------
    holding : DefaultDict[int, List[int]]
        The current chips held by each bot.
    directions : Dict[int, Dict[str, Any]]
        The rules for each bot.
    outputs : DefaultDict[int, List[int]]
        The values in each output bin.
    """
    # Track bots that have exactly two chips and are ready to act
    ready_bots = [bot_id for bot_id, chips in holding.items() if len(chips) == 2]

    while ready_bots:
        bot_id = ready_bots.pop()

        # If a bot has no directions, it cannot act (should not happen in valid input)
        if bot_id not in directions:
            continue

        chips = holding[bot_id]
        low_val = min(chips)
        high_val = max(chips)
        holding[bot_id] = []  # Bot gives away all its chips

        # Part 1: Check for the specific comparison (value 17 and 61)
        if low_val == 17 and high_val == 61:
            print(f"Part 1: Bot {bot_id} compares {low_val} and {high_val}")

        # Distribute chips according to directions
        for val, (target_type, target_id) in [
            (low_val, directions[bot_id]["low"]),
            (high_val, directions[bot_id]["high"]),
        ]:
            if target_type == "bot":
                holding[target_id].append(val)
                # If target bot now has 2 chips, it becomes ready
                if len(holding[target_id]) == 2:
                    ready_bots.append(target_id)
            else:  # target_type == "output"
                outputs[target_id].append(val)


def main():
    """Main entry point for the script."""
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        holding, directions, outputs = parse_input(filename)

        print(f"Execution started with {len(holding)} bots initially holding chips.")
        execute_directions(holding, directions, outputs)

        # Part 2: Product of chips in output bins 0, 1, and 2
        try:
            val0 = outputs[0][0]
            val1 = outputs[1][0]
            val2 = outputs[2][0]
            product = val0 * val1 * val2
            print(f"Part 2: Product of chips in outputs 0, 1, and 2 is {product}")
        except (KeyError, IndexError):
            print("Part 2: Unable to calculate (output bins 0, 1, or 2 are missing).")

        print("Execution complete.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
