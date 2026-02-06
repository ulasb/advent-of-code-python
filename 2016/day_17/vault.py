"""
Two Steps Forward, One Step Back: Advent of Code 2016, Day 17.

Created and published by Ulaş Bardak.
This code is licensed under the Mozilla Public License 2.0.
The MPL is a copyleft license that is easy to comply with. You must make the
source code for any modified MPL-licensed files available under the MPL,
but you can combine the MPL-licensed code with code under other licenses.
"""

import hashlib
from collections import deque
from typing import Optional

# The maze is 4x4, so the maximum coordinates are (3, 3).
MAX_X = 3
MAX_Y = 3

def get_available_rooms(
    passcode: str, cur_room: tuple[int, int], path: str
) -> list[tuple[str, tuple[int, int]]]:
    """
    Get all reachable rooms from the current position based on the hash.

    Parameters
    ----------
    passcode : str
        The puzzle input passcode.
    cur_room : tuple[int, int]
        Current (x, y) coordinates in the 4x4 grid.
    path : str
        The path of 'U', 'D', 'L', 'R' moves taken so far.

    Returns
    -------
    list[tuple[str, tuple[int, int]]]
        A list of tuples containing the new path string and the new (x, y) coordinates.
    """
    x, y = cur_room
    h = hashlib.md5((passcode + path).encode()).hexdigest()[:4]
    available = []

    # Directions: 0: Up, 1: Down, 2: Left, 3: Right
    # Up
    if h[0] in "bcdef" and y > 0:
        available.append((path + "U", (x, y - 1)))
    # Down
    if h[1] in "bcdef" and y < MAX_Y:
        available.append((path + "D", (x, y + 1)))
    # Left
    if h[2] in "bcdef" and x > 0:
        available.append((path + "L", (x - 1, y)))
    # Right
    if h[3] in "bcdef" and x < MAX_X:
        available.append((path + "R", (x + 1, y)))

    return available


def find_shortest_path(passcode: str) -> Optional[str]:
    """
    Find the shortest path from (0, 0) to (3, 3) using BFS.

    Parameters
    ----------
    passcode : str
        The puzzle input passcode.

    Returns
    -------
    Optional[str]
        The shortest path string, or None if no path exists.
    """
    queue: deque[tuple[tuple[int, int], str]] = deque([((0, 0), "")])

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == (MAX_X, MAX_Y):
            return path

        for new_path, new_pos in get_available_rooms(passcode, (x, y), path):
            queue.append((new_pos, new_path))

    return None


def find_longest_path_len(passcode: str) -> int:
    """
    Find the length of the longest path from (0, 0) to (3, 3) using BFS.

    This explores all possible paths until they either reach the vault
    (stopping that branch) or run out of open doors.

    Parameters
    ----------
    passcode : str
        The puzzle input passcode.

    Returns
    -------
    int
        The length of the longest path.
    """
    queue: deque[tuple[tuple[int, int], str]] = deque([((0, 0), "")])
    max_len = 0

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == (MAX_X, MAX_Y):
            max_len = max(max_len, len(path))
            continue

        for new_path, new_pos in get_available_rooms(passcode, (x, y), path):
            queue.append((new_pos, new_path))

    return max_len


if __name__ == "__main__":
    PASSCODE = "pslxynzg"
    shortest = find_shortest_path(PASSCODE)
    if shortest:
        print(shortest)

    longest_len = find_longest_path_len(PASSCODE)
    print(longest_len)
