"""
Advent of Code 2017 - Day 1: Inverse Captcha

This script solves the first day's challenge of Advent of Code 2017.
The problem involves finding the sum of digits in a circular list that match
their neighbors (either the next digit or the one halfway around).

This code is published by Ulaş Bardak under the Mozilla Public License 2.0.
"""

import sys
import os
from typing import List


def solve_part1(digits: List[int]) -> int:
    """
    Calculate the sum of digits that match the next digit in a circular list.

    Parameters
    ----------
    digits : List[int]
        A list of integers representing the captcha sequence.

    Returns
    -------
    int
        The calculated sum based on the Part 1 rules.
    """
    total_sum = 0
    n = len(digits)
    for i in range(n):
        if digits[i] == digits[(i + 1) % n]:
            total_sum += digits[i]
    return total_sum


def solve_part2(digits: List[int]) -> int:
    """
    Calculate the sum of digits that match the digit halfway around the circular list.

    Parameters
    ----------
    digits : List[int]
        A list of integers representing the captcha sequence.

    Returns
    -------
    int
        The calculated sum based on the Part 2 rules.
    """
    total_sum = 0
    n = len(digits)
    offset = n // 2
    for i in range(n):
        if digits[i] == digits[(i + offset) % n]:
            total_sum += digits[i]
    return total_sum


def main():
    """
    Main entry point for the solution script.

    Reads the input filename from command line arguments (defaults to 'input.txt')
    and prints the solution for Part 1 and Part 2.
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        sys.exit(1)

    with open(filename, "r") as f:
        input_data = f.read().strip()

    if not input_data:
        print("Error: Input file is empty.")
        sys.exit(1)

    digits = [int(d) for d in input_data]

    # Part 1
    result_p1 = solve_part1(digits)
    print(f"Part 1: {result_p1}")

    # Part 2
    result_p2 = solve_part2(digits)
    print(f"Part 2: {result_p2}")


if __name__ == "__main__":
    main()
