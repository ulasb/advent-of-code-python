"""
Advent of Code 2017 - Day 2: Corruption Checksum
Created and published by Ulaş Bardak.
This project is licensed under the Mozilla Public License 2.0 (MPL 2.0).
MPL 2.0 is a copyleft license that is easy to understand. It allows for
commercial use, modification, and distribution, but requires that the
source code of any modified files be made available under the same license.
"""

import sys
import unittest


def solve_part1(lines: list[str]) -> int:
    """
    Calculate the checksum for Part 1.

    The checksum is the sum of the difference between the largest value and the
    smallest value in each row.

    Parameters
    ----------
    lines : list of str
        The input data as a list of strings, where each string represents a row.

    Returns
    -------
    int
        The calculated checksum.
    """
    checksum = 0
    for line in lines:
        if not line.strip():
            continue
        numbers = [int(x) for x in line.split()]
        if numbers:
            checksum += max(numbers) - min(numbers)
    return checksum


def solve_part2(lines: list[str]) -> int:
    """
    Calculate the checksum for Part 2.

    The checksum is the sum of each row's result, where the result is the quotient
    of the only two numbers in the row that evenly divide each other.

    Parameters
    ----------
    lines : list of str
        The input data as a list of strings, where each string represents a row.

    Returns
    -------
    int
        The calculated checksum.
    """
    checksum = 0
    for line in lines:
        if not line.strip():
            continue
        numbers = sorted([int(x) for x in line.split()])
        found = False
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[j] % numbers[i] == 0:
                    checksum += numbers[j] // numbers[i]
                    found = True
                    break
            if found:
                break
    return checksum


def main(filename: str = "input.txt") -> int:
    """
    Main entry point for the script.

    Parameters
    ----------
    filename : str, optional
        The path to the input file, by default "input.txt".

    Returns
    -------
    int
        Exit code (0 for success, 1 for errors).
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}", file=sys.stderr)
        return 1

    print(f"Part 1: {solve_part1(lines)}")
    print(f"Part 2: {solve_part2(lines)}")
    return 0


class TestChecksum(unittest.TestCase):
    """
    Unit tests for the checksum logic.
    """

    def test_solve_part1(self):
        """Test Part 1 with the example from AoC."""
        example_input = ["5 1 9 5", "7 5 3", "2 4 6 8"]
        self.assertEqual(solve_part1(example_input), 18)

    def test_solve_part2(self):
        """Test Part 2 with the example from AoC."""
        example_input = ["5 9 2 8", "9 4 7 3", "3 8 6 5"]
        self.assertEqual(solve_part2(example_input), 9)


if __name__ == "__main__":
    # If "test" is passed as an argument, run tests instead of the solution
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Remove "test" from argv so unittest doesn't get confused
        sys.argv.pop(1)
        unittest.main()
    else:
        file_arg = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
        sys.exit(main(file_arg))
