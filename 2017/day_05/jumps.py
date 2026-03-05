"""
Advent of Code 2017, Day 5: A Maze of Twisty Trampolines, All Alike

Created and published by Ulaş Bardak.
This project is licensed under the Mozilla Public License 2.0 (MPL 2.0).
The MPL 2.0 is a free and open-source, "weak" copyleft license that allows for
commercial use, modification, and distribution, but requires that any
modifications to the code be made available under the same license.
"""

import unittest
import sys


def solve_part1(instructions: list[int]) -> int:
    """
    Calculate the number of steps to exit the maze for Part 1.

    In Part 1, after each jump, the offset of the instruction you were
    just on increases by 1.

    Parameters
    ----------
    instructions : list of int
        The initial jump offsets.

    Returns
    -------
    int
        The total number of steps taken to exit the maze.
    """
    # Work on a copy to avoid modifying the original list if reused
    jumps = instructions[:]
    idx = 0
    steps = 0
    size = len(jumps)

    while 0 <= idx < size:
        offset = jumps[idx]
        jumps[idx] += 1
        idx += offset
        steps += 1

    return steps


def solve_part2(instructions: list[int]) -> int:
    """
    Calculate the number of steps to exit the maze for Part 2.

    In Part 2, after each jump, if the offset was three or more, it
    decreases by 1. Otherwise, it increases by 1.

    Parameters
    ----------
    instructions : list of int
        The initial jump offsets.

    Returns
    -------
    int
        The total number of steps taken to exit the maze.
    """
    jumps = instructions[:]
    idx = 0
    steps = 0
    size = len(jumps)

    while 0 <= idx < size:
        offset = jumps[idx]
        if offset >= 3:
            jumps[idx] -= 1
        else:
            jumps[idx] += 1
        idx += offset
        steps += 1

    return steps


class TestJumps(unittest.TestCase):
    """Test cases for the jump maze solution."""

    def test_example_part1(self):
        """Test Part 1 with the provided example."""
        example = [0, 3, 0, 1, -3]
        self.assertEqual(solve_part1(example), 5)

    def test_example_part2(self):
        """Test Part 2 with the provided example."""
        example = [0, 3, 0, 1, -3]
        self.assertEqual(solve_part2(example), 10)


def main(file_path: str = "input.txt") -> int:
    """
    Main entry point for the script.

    Parameters
    ----------
    file_path : str
        Path to the input file containing jump offsets.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            instructions = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find input file '{file_path}'.")
        return 1
    except ValueError as e:
        print(f"Error: Invalid input in file. {e}")
        return 1

    part1_result = solve_part1(instructions)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(instructions)
    print(f"Part 2: {part2_result}")

    return 0


if __name__ == "__main__":
    # If arguments are passed, assume they are for the script (e.g., input file)
    # However, if we want to run tests based on standard unittest flow:
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Remove the 'test' argument so unittest doesn't get confused
        sys.argv.pop(1)
        unittest.main()
    else:
        # Check if input.txt exists, if not, or if requested, run tests anyway or just main
        sys.exit(main())
