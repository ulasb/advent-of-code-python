"""
This module provides the solution for Advent of Code 2016, Day 6.
The logic involves finding the most and least common characters at each position.

Created and published by Ulaş Bardak.
Following Mozilla Public License 2.0.
MPL 2.0 is a copyleft license that is easy to comply with. It allows you to
distribute the software, but you must make the source code available if you
distribute it in executable form.
"""

import sys
from collections import Counter, defaultdict
from typing import Dict, List


def solve_part1(chars: Dict[int, Counter]) -> str:
    """
    Find the most common character at each position.

    Parameters
    ----------
    chars : Dict[int, Counter]
        A mapping of column indices to a Counter of characters in that column.

    Returns
    -------
    str
        The message formed by the most common characters.
    """
    result = []
    for i in sorted(chars.keys()):
        result.append(chars[i].most_common(1)[0][0])
    return "".join(result)


def solve_part2(chars: Dict[int, Counter]) -> str:
    """
    Find the least common character at each position.

    Parameters
    ----------
    chars : Dict[int, Counter]
        A mapping of column indices to a Counter of characters in that column.

    Returns
    -------
    str
        The message formed by the least common characters.
    """
    result = []
    for i in sorted(chars.keys()):
        result.append(chars[i].most_common()[-1][0])
    return "".join(result)


def main() -> None:
    """
    Main entry point for the script. Reads the input file and prints solutions for Part 1 and Part 2.
    """
    # Use the first command line argument as the filename,
    # defaulting to 'input.txt' if none is provided.
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    chars: Dict[int, Counter] = defaultdict(Counter)

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                for i, char in enumerate(line):
                    chars[i][char] += 1

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)

    if not chars:
        print("Error: No data found in the input file.")
        sys.exit(1)

    print(solve_part1(chars))
    print(solve_part2(chars))


if __name__ == "__main__":
    main()
