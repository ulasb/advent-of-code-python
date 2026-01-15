"""
This code was created and published by Ulaş Bardak and follows the Mozilla Public License 2.0.
The MPL 2.0 is a copyleft license that allows for code to be used, modified, and distributed,
as long as any changes made to the source code are also made available under the same license.
"""

import argparse
import sys

PAD1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

PAD2 = [
    [None, None, 1, None, None],
    [None, 2, 3, 4, None],
    [5, 6, 7, 8, 9],
    [None, "A", "B", "C", None],
    [None, None, "D", None, None],
]


def get_new_position(position: tuple[int, int], direction: str, pad: list[list[int | str | None]]) -> tuple[int, int]:
    """
    Calculate the new position on the keypad based on a move direction.

    Parameters
    ----------
    position : tuple of int
        The current (x, y) coordinates on the keypad.
    direction : str
        The direction of movement ('U', 'D', 'L', 'R').
    pad : list of list
        The 2D keypad layout representing valid buttons and None elsewhere.

    Returns
    -------
    tuple of int
        The new (x, y) coordinates after the move.
    """
    x, y = position
    if direction == "U" and y > 0 and pad[y - 1][x] is not None:
        return (x, y - 1)
    if direction == "D" and y < len(pad) - 1 and pad[y + 1][x] is not None:
        return (x, y + 1)
    if direction == "L" and x > 0 and pad[y][x - 1] is not None:
        return (x - 1, y)
    if direction == "R" and x < len(pad[0]) - 1 and pad[y][x + 1] is not None:
        return (x + 1, y)
    return position


def solve_keypad(instructions, pad, start_pos):
    """
    Solve the keypad code for a given pad and set of instructions.

    Parameters
    ----------
    instructions : list of str
        The lines of instructions from the input file.
    pad : list of list
        The keypad layout.
    start_pos : tuple of int
        The starting (x, y) position.

    Returns
    -------
    str
        The resulting code.
    """
    pos = start_pos
    code = ""
    for line in instructions:
        for move in line:
            pos = get_new_position(pos, move, pad)
        code += str(pad[pos[1]][pos[0]])
    return code


def main():
    """
    Main entry point for the script. Parses arguments and solves the puzzle.
    """
    parser = argparse.ArgumentParser(
        description="Solve Advent of Code 2016 Day 2: Bathroom Security."
    )
    parser.add_argument(
        "filename",
        nargs="?",
        default="input.txt",
        help="The input file to read (default: input.txt)",
    )
    args = parser.parse_args()

    try:
        with open(args.filename, "r") as f:
        instructions = []
        for line in f:
            stripped_line = line.strip()
            if stripped_line:
                instructions.append(stripped_line)

        # Part 1: Standard 3x3 keypad, starts at '5' (1, 1)
        part1_code = solve_keypad(instructions, PAD1, (1, 1))
        print(f"Part 1: {part1_code}")

        # Part 2: Diamond-shaped keypad, starts at '5' (0, 2)
        part2_code = solve_keypad(instructions, PAD2, (0, 2))
        print(f"Part 2: {part2_code}")

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
