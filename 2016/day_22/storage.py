"""
Advent of Code 2016 - Day 22: Grid Computing

Created and published by Ulaş Bardak.
This project is licensed under the Mozilla Public License 2.0.
The MPL 2.0 is a free and open source, weak copyleft license that allows
for the use of the licensed code in other projects while requiring that
any modifications to the source code stay under the same license.
"""

import itertools
import collections
import dataclasses
from typing import List, Tuple, Set, Iterable

INPUT_FILE_DEFAULT = "input.txt"
DF_NODE_PREFIX = "/dev/grid/node-x"


@dataclasses.dataclass(frozen=True, slots=True)
class Node:
    """
    Represents a storage node in the grid.

    Attributes
    ----------
    x : int
        The x-coordinate of the node.
    y : int
        The y-coordinate of the node.
    size : int
        Total capacity of the node in Terabytes.
    used : int
        Used space in Terabytes.
    free : int
        Available space in Terabytes.
    """
    x: int
    y: int
    size: int
    used: int
    free: int

def parse_nodes(lines: Iterable[str]) -> List[Node]:
    """
    Parses the output of the 'df' command into a list of Node objects.

    Parameters
    ----------
    lines : Iterable[str]
        The lines from the input source.

    Returns
    -------
    List[Node]
        A list of parsed Node objects.
    """
    nodes = []
    for line in lines:
        if line.startswith(DF_NODE_PREFIX):
            parts = line.split()
            x, y = parts[0].split("-")[1:]
            x = int(x[1:])
            y = int(y[1:])
            size = int(parts[1][:-1])
            used = int(parts[2][:-1])
            free = int(parts[3][:-1])
            nodes.append(Node(x, y, size, used, free))
    return nodes


def is_viable_pair(node1: Node, node2: Node) -> bool:
    """
    Checks if node1's data can fit into node2's free space.

    Parameters
    ----------
    node1 : Node
        Source node.
    node2 : Node
        Destination node.

    Returns
    -------
    bool
        True if the pair is viable.
    """
    return (node1.used > 0) and (node1 != node2) and (node1.used <= node2.free)


def solve_part1(nodes: List[Node]) -> int:
    """
    Calculates the number of viable pairs in the grid.

    Parameters
    ----------
    nodes : List[Node]
        All nodes in the grid.

    Returns
    -------
    int
        The count of viable pairs.
    """
    return sum(
        1
        for node1, node2 in itertools.product(nodes, repeat=2)
        if is_viable_pair(node1, node2)
    )


def solve_part2(nodes: List[Node]) -> int:
    """
    Finds the minimum number of steps to move the goal data to (0,0).
    Uses a Full BFS tracking (empty_x, empty_y, goal_x, goal_y).

    Parameters
    ----------
    nodes : List[Node]
        All nodes in the grid.

    Returns
    -------
    int
        The minimum number of moves, or -1 if no solution exists.
    """
    max_x = max(node.x for node in nodes)
    max_y = max(node.y for node in nodes)

    try:
        empty_node = next(n for n in nodes if n.used == 0)
    except StopIteration:
        raise ValueError("Grid has no empty node.") from None

    empty_capacity = empty_node.size

    # Identify obstacles (large nodes that cannot fit data into the empty node)
    walls: Set[Tuple[int, int]] = {(n.x, n.y) for n in nodes if n.used > empty_capacity}

    # Initial state: (empty_x, empty_y, goal_x, goal_y)
    start_state = (empty_node.x, empty_node.y, max_x, 0)

    # Target: goal_x == 0, goal_y == 0
    queue = collections.deque([(start_state, 0)])
    visited = {start_state}

    while queue:
        (ex, ey, gx, gy), dist = queue.popleft()

        if gx == 0 and gy == 0:
            return dist

        # Try moving empty node to an adjacent slot
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = ex + dx, ey + dy

            # Constraints: within grid and not a wall
            if 0 <= nx <= max_x and 0 <= ny <= max_y and (nx, ny) not in walls:
                # If the empty node swaps with the goal data, goal data moves to the old empty spot
                new_gx, new_gy = gx, gy
                if nx == gx and ny == gy:
                    new_gx, new_gy = ex, ey

                new_state = (nx, ny, new_gx, new_gy)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, dist + 1))

    return -1


def main(input_filename: str = INPUT_FILE_DEFAULT) -> None:
    """
    Main entry point for solving the puzzle.

    Parameters
    ----------
    input_filename : str, optional
        Path to the puzzle input file, by default "input.txt"
    """
    with open(input_filename) as f:
        nodes = parse_nodes(f)

    # Part 1
    p1_result = solve_part1(nodes)
    print(f"Part 1: {p1_result}")

    # Part 2
    print("Running Part 2 solver...")
    p2_result = solve_part2(nodes)
    print(f"Part 2: {p2_result}")


if __name__ == "__main__":
    main()
