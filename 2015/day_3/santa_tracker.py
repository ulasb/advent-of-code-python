#!/usr/bin/env python3
"""
Santa Location Tracker for Advent of Code 2015 Day 3

This script tracks Santa's movement based on directional instructions
and counts how many times each location is visited.

Part 1: Single Santa following all directions
Part 2: Santa and Robot Santa alternating directions
"""

import sys
import unittest
from collections import defaultdict
from typing import Dict, Tuple

# Direction mappings as module constants
DIRECTION_MAP = {
    '^': (0, 1),   # up
    'v': (0, -1),  # down
    '>': (1, 0),   # right
    '<': (-1, 0)   # left
}

START_POSITION = (0, 0)


def track_santa_visits(directions: str) -> Dict[Tuple[int, int], int]:
    """
    Track Santa's movement and count visits to each location.

    Args:
        directions: String of directional characters (^ v < >)

    Returns:
        Dictionary mapping (x, y) coordinates to visit count
    """
    x, y = START_POSITION
    visits = defaultdict(int)

    # Count initial position
    visits[(x, y)] = 1

    # Process each direction
    for direction in directions:
        if direction in DIRECTION_MAP:
            dx, dy = DIRECTION_MAP[direction]
            x += dx
            y += dy
            visits[(x, y)] += 1
        else:
            print(f"Warning: Unknown direction '{direction}' ignored", file=sys.stderr)

    return visits


def track_santa_and_robot_santa(directions: str) -> int:
    """
    Track Santa and Robot Santa's movement and count unique locations visited.

    Santa and Robot Santa alternate moves, both starting at (0,0).

    Args:
        directions: String of directional characters (^ v < >)

    Returns:
        Number of unique locations visited by either Santa
    """
    santa_x, santa_y = START_POSITION
    robot_x, robot_y = START_POSITION

    # Use a set to track unique locations visited
    visited = {START_POSITION}

    # Process each direction, alternating between Santa and Robot Santa
    for i, direction in enumerate(directions):
        if direction in DIRECTION_MAP:
            dx, dy = DIRECTION_MAP[direction]

            if i % 2 == 0:
                # Santa's turn (even indices: 0, 2, 4...)
                santa_x += dx
                santa_y += dy
                visited.add((santa_x, santa_y))
            else:
                # Robot Santa's turn (odd indices: 1, 3, 5...)
                robot_x += dx
                robot_y += dy
                visited.add((robot_x, robot_y))
        else:
            print(f"Warning: Unknown direction '{direction}' ignored", file=sys.stderr)

    return len(visited)


class TestSantaTracker(unittest.TestCase):
    """Unit tests for the track_santa_visits function."""

    def test_single_right_move(self):
        """Test that '>' delivers presents to 2 houses: starting location and one to the east."""
        result = track_santa_visits(">")
        expected = {(0, 0): 1, (1, 0): 1}
        self.assertEqual(result, expected)

    def test_square_path_with_return(self):
        """Test that '^>v<' delivers presents to 4 houses in a square, including twice to starting location."""
        result = track_santa_visits("^>v<")
        expected = {(0, 0): 2, (0, 1): 1, (1, 1): 1, (1, 0): 1}
        self.assertEqual(result, expected)

    def test_alternating_up_down(self):
        """Test that '^v^v^v^v^v' delivers presents to only 2 houses."""
        result = track_santa_visits("^v^v^v^v^v")
        expected = {(0, 0): 6, (0, 1): 5}
        self.assertEqual(result, expected)

    def test_empty_directions(self):
        """Test that empty directions only visit the starting location once."""
        result = track_santa_visits("")
        expected = {(0, 0): 1}
        self.assertEqual(result, expected)

    def test_invalid_characters_ignored(self):
        """Test that invalid characters are ignored."""
        result = track_santa_visits("^>x<v")
        # Should ignore 'x' and process "^><v"
        # ^: (0,0)->(0,1), >: (0,1)->(1,1), x: ignored, <: (1,1)->(0,1), v: (0,1)->(0,0)
        expected = {(0, 0): 2, (0, 1): 2, (1, 1): 1}
        self.assertEqual(result, expected)

    def test_robot_santa_single_moves(self):
        """Test that '^v' with robot santa visits 3 locations."""
        result = track_santa_and_robot_santa("^v")
        # Santa: ^ -> (0,1), Robot: v -> (0,-1)
        self.assertEqual(result, 3)  # (0,0), (0,1), (0,-1)

    def test_robot_santa_empty_directions(self):
        """Test that empty directions only visit the starting location once."""
        result = track_santa_and_robot_santa("")
        self.assertEqual(result, 1)

    def test_robot_santa_alternating_pattern(self):
        """Test alternating pattern with robot santa."""
        result = track_santa_and_robot_santa("^^")
        # Santa: ^ -> (0,1), Robot: ^ -> (0,1)
        self.assertEqual(result, 2)  # (0,0), (0,1)

    def test_robot_santa_up_down_separate(self):
        """Test that ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south."""
        result = track_santa_and_robot_santa("^v")
        # Santa: ^ -> (0,1), Robo-Santa: v -> (0,-1)
        self.assertEqual(result, 3)  # (0,0), (0,1), (0,-1)

    def test_robot_santa_square_path_three_houses(self):
        """Test that ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started."""
        result = track_santa_and_robot_santa("^>v<")
        # Santa: ^ -> (0,1), v -> (0,0)
        # Robo-Santa: > -> (1,0), < -> (0,0)
        self.assertEqual(result, 3)  # (0,0), (0,1), (1,0)

    def test_robot_santa_long_alternating_path(self):
        """Test that ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other."""
        result = track_santa_and_robot_santa("^v^v^v^v^v")
        # Santa: positions 0,2,4,6,8 -> ^ ^ ^ ^ ^ -> (0,1), (0,2), (0,3), (0,4), (0,5)
        # Robo-Santa: positions 1,3,5,7,9 -> v v v v v -> (0,-1), (0,-2), (0,-3), (0,-4), (0,-5)
        self.assertEqual(result, 11)  # 5 Santa houses + 5 Robo-Santa houses + 1 shared start


def main():
    """Main function to handle file input and output results."""
    # Get filename from command line argument or use default
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        # Read the directions from file
        with open(filename, 'r') as file:
            directions = file.read().strip()

        if not directions:
            print("Error: Input file is empty", file=sys.stderr)
            sys.exit(1)

        # Track visits for both parts
        visits = track_santa_visits(directions)
        robot_visits = track_santa_and_robot_santa(directions)

        # Output results
        print(f"Processed {len(directions)} directions from {filename}")
        print(f"\nPart 1 - Santa alone:")
        print(f"Total unique locations visited: {len(visits)}")

        print(f"\nPart 2 - Santa and Robot Santa:")
        print(f"Total unique locations visited: {robot_visits}")


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Check if tests should be run
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run the main program
        main()
