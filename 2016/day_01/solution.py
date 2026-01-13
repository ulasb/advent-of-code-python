#!/usr/bin/env python3
"""
Advent of Code 2016 - Day 1 Solution

Created by Ulaş Bardak
Licensed under Mozilla Public License 2.0
"""
import sys
import unittest
from enum import Enum


class Direction(Enum):
    """Enumeration for cardinal directions.

    Values correspond to clockwise rotation: NORTH=0, EAST=1, SOUTH=2, WEST=3.
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def update_location(current_direction, current_location, direction_string):
    """Update location based on current direction and direction string.

    Direction string format: Lx or Rx where x is number of steps.
    L = turn left, R = turn right.

    Parameters
    ----------
    current_direction : Direction
        Current Direction enum value
    current_location : tuple
        Tuple (x, y) representing current position
    direction_string : str
        String like "L5" or "R3"

    Returns
    -------
    tuple
        Tuple of (new_direction, new_location, positions_visited)
        where positions_visited is a list of all positions visited during this move
    """
    # Parse the direction string
    turn = direction_string[0]  # 'L' or 'R'
    steps = int(direction_string[1:])  # number after L/R

    # 1. Update direction based on turn (L or R)
    if turn == "L":
        current_direction = Direction((current_direction.value - 1) % 4)
    else:
        current_direction = Direction((current_direction.value + 1) % 4)

    # 2. Move in the new direction by 'steps' amount (one step at a time)
    positions_visited = []
    new_location = current_location
    direction_deltas = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0),
    }
    dx, dy = direction_deltas[current_direction]
    for _ in range(steps):
        new_location = (new_location[0] + dx, new_location[1] + dy)
        positions_visited.append(new_location)

    # 3. Return new direction, location, and all positions visited
    return current_direction, new_location, positions_visited


def process_directions(directions):
    """Process a list of directions and return final location, direction, and HQ location if found.

    Parameters
    ----------
    directions : list
        List of direction strings (e.g., ["R8", "L4"])

    Returns
    -------
    tuple
        (final_location, final_direction, hq_location)
        where hq_location is None if no location was visited twice
    """
    # Start facing North at (0, 0)
    current_direction = Direction.NORTH
    current_location = (0, 0)

    visited_locations = set()
    visited_locations.add((0, 0))
    hq_location = None

    # Process each direction
    for direction in directions:
        current_direction, current_location, positions_visited = updateLocation(
            current_direction, current_location, direction
        )

        # Check each position visited during this move for HQ location
        if hq_location is None:
            for pos in positions_visited:
                if pos in visited_locations:
                    hq_location = pos
                else:
                    visited_locations.add(pos)


    return current_location, current_direction, hq_location


class TestAdventOfCodeDay1(unittest.TestCase):
    """Test cases for Advent of Code 2016 Day 1 solution."""

    def test_hq_location(self):
        """Test HQ location detection: R8, R4, R4, R8 should find HQ at distance 4."""
        directions = ["R8", "R4", "R4", "R8"]
        final_loc, final_dir, hq_loc = process_directions(directions)

        self.assertIsNotNone(hq_loc, "HQ location should be found")
        hq_distance = abs(hq_loc[0]) + abs(hq_loc[1])
        self.assertEqual(hq_distance, 4, f"HQ should be 4 blocks away, got {hq_distance}")

    def test_distance_r2_l3(self):
        """Test R2, L3 should end at (2, 3), 5 blocks away."""
        directions = ["R2", "L3"]
        final_loc, final_dir, hq_loc = process_directions(directions)

        self.assertEqual(final_loc, (2, 3))
        distance = abs(final_loc[0]) + abs(final_loc[1])
        self.assertEqual(distance, 5)

    def test_distance_r2_r2_r2(self):
        """Test R2, R2, R2 should end at (0, -2), 2 blocks away."""
        directions = ["R2", "R2", "R2"]
        final_loc, final_dir, hq_loc = process_directions(directions)

        self.assertEqual(final_loc, (0, -2))
        distance = abs(final_loc[0]) + abs(final_loc[1])
        self.assertEqual(distance, 2)

    def test_distance_r5_l5_r5_r3(self):
        """Test R5, L5, R5, R3 should end 12 blocks away."""
        directions = ["R5", "L5", "R5", "R3"]
        final_loc, final_dir, hq_loc = process_directions(directions)

        distance = abs(final_loc[0]) + abs(final_loc[1])
        self.assertEqual(distance, 12)


def main():
    # Check if we should run tests
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=[''], exit=False, verbosity=2)
        return

    # Parse command line arguments
    input_file = "input.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    # Read the input file
    try:
        with open(input_file, 'r') as f:
            # Read all content and split by commas, strip whitespace
            directions = [d.strip() for d in f.read().strip().split(',')]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Process the directions
    final_location, final_direction, hq_location = process_directions(directions)

    # Print results
    if hq_location:
        print(f"First twice visited location: {hq_location}")
        print(f"Distance to HQ: {abs(hq_location[0]) + abs(hq_location[1])}")

    print(f"Final location: {final_location}")
    print(f"Final direction: {final_direction}")
    print(f"Distance: {abs(final_location[0]) + abs(final_location[1])}")


if __name__ == "__main__":
    main()