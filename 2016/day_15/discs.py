"""
Solution for Advent of Code 2016, Day 15.

This script calculates the first time step to press a button so that a capsule
falls through a series of rotating discs.

Created and published by Ulaş Bardak.
Following Mozilla Public License 2.0:
This license allows for the use, modification, and distribution of the source code,
provided that any modifications to the original code are also made available under
the same license. It balances the interests of open source and proprietary development.
"""

import sys
import re
import math
from dataclasses import dataclass
from typing import List


@dataclass
class Disc:
    """
    Representation of a rotating disc.

    Attributes
    ----------
    num_positions : int
        The total number of positions on the disc.
    starting_position : int
        The position of the disc at time=0.
    index : int
        The 1-based index (order) of the disc.
    """

    num_positions: int
    starting_position: int
    index: int


def parse_discs(filename: str) -> List[Disc]:
    """
    Parse the disc configurations from the input file.

    Parameters
    ----------
    filename : str
        The path to the input file.

    Returns
    -------
    List[Disc]
        A list of Disc objects parsed from the file.
    """
    discs = []
    # Regex to match: Disc #<n> has <n> positions; at time=0, it is at position <n>.
    pattern = re.compile(
        r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)."
    )

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.search(line)
            if match:
                index = int(match.group(1))
                num_pos = int(match.group(2))
                start_pos = int(match.group(3))
                discs.append(
                    Disc(
                        num_positions=num_pos, starting_position=start_pos, index=index
                    )
                )

    return discs


def solve(discs: List[Disc]) -> int:
    """
    Find the first time step that satisfies the condition for all discs.

    The condition for each disc is: (starting_position + time + index) % num_positions == 0.

    Parameters
    ----------
    discs : List[Disc]
        The list of discs to synchronize.

    Returns
    -------
    int
        The earliest time step to push the button.
    """
    time = 0
    step = 1
    for disc in discs:
        while (disc.starting_position + time + disc.index) % disc.num_positions != 0:
            time += step
        # Update step to the least common multiple of the current step and the disc's positions
        step = math.lcm(step, disc.num_positions)
    return time


def main() -> None:
    """
    Main entry point for the script.
    """
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
        discs = parse_discs(filename)

        # Part 1
        result_p1 = solve(discs)
        print(f"Part 1: {result_p1}")

        # Part 2: Add a new disc with 11 positions at position 0, at the next index
        discs_p2 = discs + [Disc(num_positions=11, starting_position=0, index=len(discs) + 1)]
        result_p2 = solve(discs_p2)
        print(f"Part 2: {result_p2}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
