#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 18: Like a GIF For Your Yard

This script simulates a grid of lights following Conway's Game of Life rules
to determine how many lights remain on after 100 steps.
"""

import argparse
import logging
import sys
import unittest
from typing import List
from unittest.mock import mock_open, patch

# Constants
DEFAULT_INPUT_FILE = "input.txt"
ON = "#"
OFF = "."
STEPS = 100

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_grid(filename: str = DEFAULT_INPUT_FILE) -> List[List[bool]]:
    """
    Parse the input file and build a 2D grid.

    Parameters
    ----------
    filename : str
        Path to the input file

    Returns
    -------
    List[List[bool]]
        2D list where True = on, False = off

    Raises
    ------
    FileNotFoundError
        If the input file doesn't exist
    """
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Convert characters to boolean values
    return [[char == ON for char in line] for line in lines]


def count_neighbors(grid: List[List[bool]], row: int, col: int) -> int:
    """
    Count the number of neighbors that are on.

    Parameters
    ----------
    grid : List[List[bool]]
        The grid to check
    row : int
        Row index
    col : int
        Column index

    Returns
    -------
    int
        Number of neighbors that are on
    """
    height = len(grid)
    width = len(grid[0]) if grid else 0
    count = 0

    # Optimized: Direct grid access without bounds checking in inner loop
    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i != row or j != col) and grid[i][j]:
                count += 1

    return count


def step_cell(grid: List[List[bool]], row: int, col: int) -> bool:
    """
    Determine the state of a cell after one step using Game of Life rules.

    Parameters
    ----------
    grid : List[List[bool]]
        The current grid state
    row : int
        Row index
    col : int
        Column index

    Returns
    -------
    bool
        True if the cell should be on, False otherwise
    """
    neighbors = count_neighbors(grid, row, col)
    current_state = grid[row][col]

    # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    if current_state:
        return neighbors in (2, 3)
    else:
        return neighbors == 3


def simulate_step(grid: List[List[bool]]) -> List[List[bool]]:
    """
    Perform one step of the simulation.

    Parameters
    ----------
    grid : List[List[bool]]
        The current grid state

    Returns
    -------
    List[List[bool]]
        The new grid state after one step
    """
    height = len(grid)
    width = len(grid[0]) if grid else 0

    # Optimized: Use list comprehension instead of repeated appends
    return [[step_cell(grid, i, j) for j in range(width)] for i in range(height)]


def turn_on_corners(grid: List[List[bool]]) -> None:
    """
    Turn on the four corners of the grid.

    Parameters
    ----------
    grid : List[List[bool]]
        The grid to modify (modified in-place)
    """
    if not grid or not grid[0]:
        return

    height = len(grid)
    width = len(grid[0])
    grid[0][0] = True
    grid[0][width - 1] = True
    grid[height - 1][0] = True
    grid[height - 1][width - 1] = True


def count_lights_on(grid: List[List[bool]]) -> int:
    """
    Count the number of lights that are on.

    Parameters
    ----------
    grid : List[List[bool]]
        The grid to count

    Returns
    -------
    int
        Number of lights in the "on" state
    """
    return sum(sum(row) for row in grid)


def solve_part1(filename: str = DEFAULT_INPUT_FILE) -> int:
    """
    Solve Part 1: Lights follow Game of Life rules.

    Parameters
    ----------
    filename : str
        Path to the input file

    Returns
    -------
    int
        Number of lights on after STEPS iterations
    """
    grid = parse_grid(filename)
    logger.info(
        f"Initial state: {len(grid)}x{len(grid[0]) if grid else 0} grid, {count_lights_on(grid)} lights on"
    )

    for _ in range(STEPS):
        grid = simulate_step(grid)

    return count_lights_on(grid)


def solve_part2(filename: str = DEFAULT_INPUT_FILE) -> int:
    """
    Solve Part 2: Same as Part 1, but the four corners are always on.

    Parameters
    ----------
    filename : str
        Path to the input file

    Returns
    -------
    int
        Number of lights on after STEPS iterations with corners stuck on
    """
    grid = parse_grid(filename)
    turn_on_corners(grid)

    for _ in range(STEPS):
        grid = simulate_step(grid)
        turn_on_corners(grid)

    return count_lights_on(grid)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 18: Simulate a grid of lights following Game of Life rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 solution.py                    # Use default input.txt
  python3 solution.py -f custom.txt      # Use custom input file
  python3 solution.py --test             # Run unit tests
        """,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f"Input file containing the initial grid state (default: {DEFAULT_INPUT_FILE})",
    )

    parser.add_argument(
        "--test", action="store_true", help="Run unit tests instead of main program"
    )

    return parser.parse_args()


class TestLightGrid(unittest.TestCase):
    """Unit tests for the light grid simulation."""

    def test_parse_grid(self):
        """Test parsing a simple grid from string."""
        test_data = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        mock_file_content = "\n".join(test_data)

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            grid = parse_grid("test_input.txt")

        self.assertEqual(len(grid), 6)
        self.assertEqual(len(grid[0]), 6)
        self.assertEqual(count_lights_on(grid), 15)

    def test_count_neighbors(self):
        """Test neighbor counting."""
        grid = [[True, False, True], [False, True, False], [True, False, True]]

        # Center cell has 4 neighbors on
        self.assertEqual(count_neighbors(grid, 1, 1), 4)

        # Corner cell has 1 neighbor on
        self.assertEqual(count_neighbors(grid, 0, 0), 1)

    def test_step_cell(self):
        """Test individual cell stepping."""
        grid = [[True, False, True], [False, True, False], [True, False, True]]

        # Center cell (on, 4 neighbors) should turn off
        self.assertFalse(step_cell(grid, 1, 1))

        # Top-left corner (on, 1 neighbor) should turn off
        self.assertFalse(step_cell(grid, 0, 0))

    def test_small_example(self):
        """Test the small example from Advent of Code."""
        test_data = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        mock_file_content = "\n".join(test_data)

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            grid = parse_grid("test_input.txt")

        # After 4 steps, there should be 4 lights on
        for _ in range(4):
            grid = simulate_step(grid)

        self.assertEqual(count_lights_on(grid), 4)


def main():
    """Main entry point for the script."""
    args = parse_arguments()

    if args.test:
        # Run unit tests
        unittest.main(argv=["solution.py"])
        return

    # Solve both parts
    try:
        part1_answer = solve_part1(args.file)
        print(f"Part 1: Total lights on: {part1_answer}")

        part2_answer = solve_part2(args.file)
        print(f"Part 2: Total lights on: {part2_answer}")

    except FileNotFoundError:
        logger.error(f"Input file '{args.file}' not found")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
