"""
Advent of Code 2017 - Day 3: Spiral Memory

Created and published by Ulaş Bardak.
This code is licensed under the Mozilla Public License 2.0 (MPL 2.0).
MPL 2.0 is a copyleft license that allows for the integration of licensed code
into larger works, provided that the MPL-licensed components remain under the MPL
and their source code remains available.
"""

import math
import sys


def find_distance(goal: int) -> int:
    """
    Calculate the Manhattan distance from the goal square to square 1.

    Parameters
    ----------
    goal : int
        The target square number on the spiral grid.

    Returns
    -------
    int
        The Manhattan distance to square 1.
    """
    if goal == 1:
        return 0

    # Find the ring number 'n' (radius)
    n = int(math.ceil((math.sqrt(goal) - 1) / 2))

    side_length = 2 * n + 1
    max_val = side_length**2

    # The centers of the four sides of the ring
    centers = [max_val - n - k * (side_length - 1) for k in range(4)]
    min_dist_to_center = min(abs(goal - c) for c in centers)

    return n + min_dist_to_center


def find_first_larger(goal: int) -> int:
    """
    Find the first value written in the spiral grid that is larger than the goal.

    The grid is populated by summing all adjacent squares (including diagonals).

    Parameters
    ----------
    goal : int
        The value to exceed.

    Returns
    -------
    int
        The first value larger than the goal.
    """
    grid: dict[tuple[int, int], int] = {(0, 0): 1}
    x, y = 0, 0
    dx, dy = 1, 0

    while True:
        x += dx
        y += dy

        # Calculate sum of neighbors
        val = 0
        for nx in range(x - 1, x + 2):
            for ny in range(y - 1, y + 2):
                if (nx, ny) in grid:
                    val += grid[(nx, ny)]

        grid[(x, y)] = val

        if val > goal:
            return val

        # Change direction if the square to the left is empty
        if (x - dy, y + dx) not in grid:
            dx, dy = -dy, dx


def read_input(filename: str = "input.txt") -> int:
    """
    Read the goal value from the input file.

    Parameters
    ----------
    filename : str
        The name of the file containing the goal value.

    Returns
    -------
    int
        The goal value.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is empty or contains an invalid integer.
    """
    with open(filename, "r") as f:
        content = f.read().strip()
        if not content:
            raise ValueError(f"Error: {filename} is empty.")
        return int(content)


def solve(goal: int) -> tuple[int, int]:
    """
    Solve Part 1 and Part 2 of the puzzle.

    Parameters
    ----------
    goal : int
        The target square number on the spiral grid.

    Returns
    -------
    tuple[int, int]
        The results for Part 1 and Part 2.
    """
    distance = find_distance(goal)
    first_larger = find_first_larger(goal)
    return distance, first_larger


if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        goal_val = read_input(target_file)
        res_p1, res_p2 = solve(goal_val)
        print(f"Part 1: {res_p1}")
        print(f"Part 2: {res_p2}")
    except (FileNotFoundError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
