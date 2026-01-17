"""
Advent of Code 2016 - Day 3: Squares With Three Sides

This script checks how many triangles can be formed from given triplets of numbers.
Part 1 checks rows, Part 2 checks columns.

Created and published by Ulaş Bardak.
This code follows the Mozilla Public License 2.0.
MPL 2.0 is a copyleft license that is easy to use and compatible with other licenses.
It requires that modifications to the MPL-licensed source code be made available under the MPL.
"""

import sys
import argparse
from typing import List


def is_valid_triangle(sides: List[int]) -> bool:
    """
    Check if a list of three sides can form a valid triangle.

    The sum of any two sides must be greater than the third side.

    Parameters
    ----------
    sides : List[int]
        A list or triplet of integers representing the side lengths.

    Returns
    -------
    bool
        True if the sides form a valid triangle, False otherwise.
    """
    if len(sides) != 3:
        return False
    a, b, c = sides
    return a + b > c and a + c > b and b + c > a


def solve_part1(data: List[List[int]]) -> int:
    """
    Solve Part 1: Count valid triangles where each row is a triplet.

    Parameters
    ----------
    data : List[List[int]]
        The input data as a list of triplets.

    Returns
    -------
    int
        The number of valid triangles.
    """
    return sum(1 for triplet in data if is_valid_triangle(triplet))


def solve_part2(data: List[List[int]]) -> int:
    """
    Solve Part 2: Count valid triangles where triplets are formed vertically.

    Parameters
    ----------
    data : List[List[int]]
        The input data as a list of horizontal triplets.

    Returns
    -------
    int
        The number of valid triangles.
    """
    count = 0
    # Process 3 rows at a time
    for i in range(0, len(data) - 2, 3):
        # Transpose the 3x3 block
        row1, row2, row3 = data[i], data[i + 1], data[i + 2]
        for col in range(3):
            triplet = [row1[col], row2[col], row3[col]]
            if is_valid_triangle(triplet):
                count += 1
    return count


def main() -> None:
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Advent of Code 2016 Day 3")
    parser.add_argument(
        "filename",
        nargs="?",
        default="input.txt",
        help="Input file (default: input.txt)",
    )
    args = parser.parse_args()

    data: List[List[int]] = []
    try:
        with open(args.filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [int(x) for x in line.split()]
                if len(parts) == 3:
                    data.append(parts)

        part1_result = solve_part1(data)
        print(f"Part 1 - Total number of valid triangles: {part1_result}")

        part2_result = solve_part2(data)
        print(f"Part 2 - Total number of valid triangles: {part2_result}")

    except FileNotFoundError:
        print(f"Error: {args.filename} not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing input: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
