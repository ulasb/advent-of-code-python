"""
Advent of Code 2016 - Day 13: A Maze of Twisty Little Cubicles

This code was created and published by Ulaş Bardak.
Follows Mozilla Public License 2.0 (MPL-2.0).
MPL-2.0 is a copyleft license that is easy to comply with. You must make the
source code for any modifications to the licensed file available under MPL-2.0.
"""

from collections import deque
from functools import lru_cache

# The puzzle input (favorite number)
FAVORITE_NUMBER = 1358


@lru_cache(None)
def is_wall(x: int, y: int) -> bool:
    """
    Check if the given coordinate (x, y) is a wall.

    Parameters
    ----------
    x : int
        The x-coordinate in the maze.
    y : int
        The y-coordinate in the maze.

    Returns
    -------
    bool
        True if the location is a wall, False if it is an open space.
    """
    if x < 0 or y < 0:
        return True
    val = x * x + 3 * x + 2 * x * y + y + y * y + FAVORITE_NUMBER
    return bin(val).count("1") % 2 == 1


def count_moves(
    start_room: tuple[int, int], target_room: tuple[int, int]
) -> int | None:
    """
    Find the shortest distance between start_room and target_room using BFS.

    Parameters
    ----------
    start_room : tuple[int, int]
        The (x, y) starting coordinates.
    target_room : tuple[int, int]
        The (x, y) target coordinates.

    Returns
    -------
    int | None
        The minimum number of moves to reach the target, or None if unreachable.
    """
    queue = deque([start_room])
    visited = {start_room}
    moves = 0

    while queue:
        for _ in range(len(queue)):
            x, y = queue.popleft()
            if (x, y) == target_room:
                return moves

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    nx >= 0
                    and ny >= 0
                    and (nx, ny) not in visited
                    and not is_wall(nx, ny)
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        moves += 1
    return None


def count_rooms(start_room: tuple[int, int], max_moves: int) -> int:
    """
    Count the number of unique locations reachable in at most max_moves steps.

    Parameters
    ----------
    start_room : tuple[int, int]
        The (x, y) starting coordinates.
    max_moves : int
        The maximum number of steps allowed.

    Returns
    -------
    int
        The total number of unique locations reachable.
    """
    queue = deque([start_room])
    visited = {start_room}
    moves = 0

    while queue and moves < max_moves:
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    nx >= 0
                    and ny >= 0
                    and (nx, ny) not in visited
                    and not is_wall(nx, ny)
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        moves += 1
    return len(visited)


if __name__ == "__main__":
    start_pos = (1, 1)
    target_pos = (31, 39)

    # Part 1: shortest path to (31, 39)
    min_moves = count_moves(start_pos, target_pos)
    print(f"Part 1: {min_moves}")

    # Part 2: rooms reachable in at most 50 steps
    total_rooms = count_rooms(start_pos, 50)
    print(f"Part 2: {total_rooms}")
