"""
Advent of Code 2016 - Day 24: Air Duct Spelunking
Created and published by Ulaş Bardak.
Licensed under the Mozilla Public License 2.0 (MPL 2.0).
MPL 2.0 is a copyleft license that allows you to use, modify, and distribute
this code, but you must make the source code of any modified versions available
under the same license.
"""

import sys
from itertools import permutations
from collections import deque


def parse_input(input_string: str) -> dict[int, tuple[int, int]]:
    """
    Parse the input string and return a dictionary of numbered points.

    Parameters
    ----------
    input_string : str
        The raw input string containing the map.

    Returns
    -------
    dict[int, tuple[int, int]]
        A dictionary where keys are the numbers on the map and values are (x, y) coordinates.
    """
    numbered_points = {}
    for y, line in enumerate(input_string.strip().split("\n")):
        for x, char in enumerate(line):
            if char.isdigit():
                numbered_points[int(char)] = (x, y)
    return numbered_points


def bfs(start: tuple[int, int], end: tuple[int, int], grid: list[str]) -> int:
    """
    Calculate the shortest distance between two points using BFS.

    Parameters
    ----------
    start : tuple[int, int]
        The starting (x, y) coordinates.
    end : tuple[int, int]
        The target (x, y) coordinates.
    grid : list[str]
        The map represented as a list of strings.

    Returns
    -------
    int
        The shortest distance between start and end. Returns infinity if no path exists.
    """
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == end:
            return dist
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and grid[ny][nx] != "#"
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    return float("inf")


def solve_tsp(
    distances: dict[tuple[int, int], int],
    points: list[int],
    return_to_zero: bool = False,
) -> int:
    """
    Solve the traveling salesman problem for a subset of points starting from '0'.

    Parameters
    ----------
    distances : dict[tuple[int, int], int]
        Precomputed distances between all pairs of points.
    points : list[int]
        The list of numbered points to visit.
    return_to_zero : bool, optional
        Whether the path must end by returning to point '0' (default is False).

    Returns
    -------
    int
        The minimum total distance for the path.
    """
    others = [p for p in points if p != 0]
    min_total_distance = float("inf")

    for p in permutations(others):
        path = (0,) + p
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += distances[(path[i], path[i + 1])]

        if return_to_zero:
            total_distance += distances[(path[-1], 0)]

        min_total_distance = min(min_total_distance, total_distance)
    return min_total_distance


def solve(filename: str = "input.txt") -> tuple[int, int]:
    """
    Solve both Part 1 and Part 2 of the puzzle.

    Parameters
    ----------
    filename : str, optional
        The path to the input file (default is "input.txt").

    Returns
    -------
    tuple[int, int]
        A tuple containing (Part 1 result, Part 2 result).
    """
    with open(filename, "r") as f:
        input_string = f.read()

    numbered_points = parse_input(input_string)
    grid = input_string.strip().split("\n")
    distances = {}
    points = sorted(numbered_points.keys())

    # Precompute all-pairs shortest paths between numbered points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]
            d = bfs(numbered_points[p1], numbered_points[p2], grid)
            distances[(p1, p2)] = d
            distances[(p2, p1)] = d

    part1 = solve_tsp(distances, points, return_to_zero=False)
    part2 = solve_tsp(distances, points, return_to_zero=True)

    return part1, part2


if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        p1, p2 = solve(target_file)
        print(f"Part 1: {p1}")
        print(f"Part 2: {p2}")
    except FileNotFoundError:
        print(f"Error: File '{target_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
