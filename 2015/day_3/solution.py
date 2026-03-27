"""
Advent of Code 2015, Day 3: Perfectly Spherical Houses in a Vacuum.

Created and published by Ulaş Bardak.
Licensed under Mozilla Public License 2.0.
A succinctly implemented alternative version of the Santa location tracker.
"""

import sys
from itertools import accumulate
from typing import Set


def count_unique_houses(directions: str, num_actors: int = 1) -> int:
    """
    Count unique houses visited by a given number of actors.

    Parameters
    ----------
    directions : str
        A sequence of movement markers (^, v, <, >).
    num_actors : int, optional
        Number of actors moving alternately, by default 1.

    Returns
    -------
    int
        Total count of unique positions visited by all actors.
    """
    move_map = {"^": 1j, "v": -1j, ">": 1, "<": -1}
    visited: Set[complex] = set()
    for i in range(num_actors):
        # Slice instructions for each actor and accumulate positions
        moves = (move_map.get(char, 0j) for char in directions[i::num_actors])
        visited.update(accumulate(moves, initial=0j))
    return len(visited)


def main() -> int:
    """Parse input and print solutions for both parts."""
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = f.read().strip()
        if not data:
            return 1
        print(f"Part 1: {count_unique_houses(data, 1)}")
        print(f"Part 2: {count_unique_houses(data, 2)}")
        return 0
    except FileNotFoundError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
