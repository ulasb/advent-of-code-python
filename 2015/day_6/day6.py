#!/usr/bin/env python3

import argparse
import sys
from typing import List, Tuple

# Constants
NUM_ROWS = 1000
NUM_COLS = 1000

def create_grid(rows: int = NUM_ROWS, cols: int = NUM_COLS) -> List[List[int]]:
    """Create a grid initialized to 0."""
    return [[0 for _ in range(cols)] for _ in range(rows)]

def process_direction_part1(grid: List[List[int]], command: str,
                           start_x: int, start_y: int, end_x: int, end_y: int) -> int:
    """Process a direction for Part 1 (on/off lights). Returns the change in light count."""
    total_change = 0

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            if command == "toggle":
                if grid[x][y]:
                    grid[x][y] = 0
                    total_change -= 1
                else:
                    grid[x][y] = 1
                    total_change += 1
            elif command == "turn on":
                if not grid[x][y]:
                    grid[x][y] = 1
                    total_change += 1
            elif command == "turn off":
                if grid[x][y]:
                    grid[x][y] = 0
                    total_change -= 1
    return total_change

def process_direction_part2(grid: List[List[int]], command: str,
                           start_x: int, start_y: int, end_x: int, end_y: int) -> int:
    """Process a direction for Part 2 (brightness levels). Returns the change in total brightness."""
    total_change = 0

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            if command == "toggle":
                grid[x][y] += 2
                total_change += 2
            elif command == "turn on":
                grid[x][y] += 1
                total_change += 1
            elif command == "turn off":
                if grid[x][y] > 0:
                    grid[x][y] -= 1
                    total_change -= 1
    return total_change

def parse_line(line: str) -> Tuple[str, Tuple[int, int], Tuple[int, int]]:
    """Parse a single instruction line and return (command, start_coords, end_coords)."""
    line_parts = line.split()

    if len(line_parts) == 4:
        # "toggle x1,y1 through x2,y2"
        command = "toggle"
        start_coords = tuple(int(coord) for coord in line_parts[1].split(","))
        end_coords = tuple(int(coord) for coord in line_parts[3].split(","))
    else:
        # "turn on/off x1,y1 through x2,y2"
        command = f"{line_parts[0]} {line_parts[1]}"
        start_coords = tuple(int(coord) for coord in line_parts[2].split(","))
        end_coords = tuple(int(coord) for coord in line_parts[4].split(","))

    return command, start_coords, end_coords

def count_lights_on(grid: List[List[int]]) -> int:
    """Count the number of lights that are on (Part 1)."""
    return sum(sum(row) for row in grid)

def calculate_total_brightness(grid: List[List[int]]) -> int:
    """Calculate the total brightness of all lights (Part 2)."""
    return sum(sum(row) for row in grid)

def process_instructions(instructions: List[str], part: int = 2) -> Tuple[int, int]:
    """
    Process a list of instructions and return (lights_on, total_brightness).
    For Part 1, lights_on is the count of lights that are on.
    For Part 2, total_brightness is the sum of all brightness levels.
    """
    grid = create_grid()
    total_change = 0

    for instruction in instructions:
        instruction = instruction.strip()
        if not instruction:
            continue

        command, (start_x, start_y), (end_x, end_y) = parse_line(instruction)

        if part == 1:
            change = process_direction_part1(grid, command, start_x, start_y, end_x, end_y)
        else:  # part == 2
            change = process_direction_part2(grid, command, start_x, start_y, end_x, end_y)

        total_change += change

    lights_on = count_lights_on(grid)
    total_brightness = calculate_total_brightness(grid)

    return lights_on, total_brightness

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Advent of Code 2015 Day 6')
    parser.add_argument('input_file', nargs='?', default='input.txt',
                        help='Input file containing directions (default: input.txt)')
    parser.add_argument('--part', type=int, choices=[1, 2], default=2,
                        help='Which part of the puzzle to solve (default: 2)')
    args = parser.parse_args()

    # Read input file
    try:
        with open(args.input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    # Process instructions
    lights_on, total_brightness = process_instructions(lines, args.part)

    if args.part == 1:
        print(f"Lights on: {lights_on}")
    else:
        print(f"Total brightness: {total_brightness}")

# Unit Tests
import unittest

class TestDay6(unittest.TestCase):

    def test_parse_line_toggle(self):
        """Test parsing toggle instructions."""
        command, start, end = parse_line("toggle 0,0 through 999,999")
        self.assertEqual(command, "toggle")
        self.assertEqual(start, (0, 0))
        self.assertEqual(end, (999, 999))

    def test_parse_line_turn_on(self):
        """Test parsing turn on instructions."""
        command, start, end = parse_line("turn on 0,0 through 999,999")
        self.assertEqual(command, "turn on")
        self.assertEqual(start, (0, 0))
        self.assertEqual(end, (999, 999))

    def test_parse_line_turn_off(self):
        """Test parsing turn off instructions."""
        command, start, end = parse_line("turn off 499,499 through 500,500")
        self.assertEqual(command, "turn off")
        self.assertEqual(start, (499, 499))
        self.assertEqual(end, (500, 500))

    def test_part1_turn_on_all(self):
        """Part 1: turn on 0,0 through 999,999 would turn on (or leave on) every light."""
        instructions = ["turn on 0,0 through 999,999"]
        lights_on, _ = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 1000000)  # 1000 * 1000

    def test_part1_toggle_first_row(self):
        """Part 1: toggle 0,0 through 999,0 would toggle the first line of 1000 lights."""
        instructions = ["toggle 0,0 through 999,0"]
        lights_on, _ = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 1000)  # All lights in first row are toggled on

    def test_part1_turn_off_middle_four(self):
        """Part 1: turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights."""
        # First turn them on, then turn off
        instructions = [
            "turn on 499,499 through 500,500",
            "turn off 499,499 through 500,500"
        ]
        lights_on, _ = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 0)  # All middle four lights are off

    def test_part1_combined_scenario(self):
        """Test a more complex Part 1 scenario with multiple instructions."""
        instructions = [
            "turn on 0,0 through 999,999",      # Turn on all lights: 1,000,000 on
            "toggle 0,0 through 999,0",         # Toggle first row: 1,000 off, 999,000 on
            "turn off 499,499 through 500,500"  # Turn off middle 4: 998,996 on
        ]
        lights_on, _ = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 998996)

    def test_part2_turn_on_single_light(self):
        """Part 2: turn on 0,0 through 0,0 would increase the total brightness by 1."""
        instructions = ["turn on 0,0 through 0,0"]
        _, total_brightness = process_instructions(instructions, part=2)
        self.assertEqual(total_brightness, 1)

    def test_part2_toggle_all_lights(self):
        """Part 2: toggle 0,0 through 999,999 would increase the total brightness by 2000000."""
        instructions = ["toggle 0,0 through 999,999"]
        _, total_brightness = process_instructions(instructions, part=2)
        self.assertEqual(total_brightness, 2000000)  # 1000000 * 2

    def test_part2_multiple_operations(self):
        """Test Part 2 with multiple operations on the same area."""
        instructions = [
            "turn on 0,0 through 0,0",    # +1
            "turn on 0,0 through 0,0",    # +1, total = 2
            "toggle 0,0 through 0,0",     # +2, total = 4
            "turn off 0,0 through 0,0",   # -1, total = 3
            "turn off 0,0 through 0,0",   # -1, total = 2
            "turn off 0,0 through 0,0"    # -1, total = 1
        ]
        _, total_brightness = process_instructions(instructions, part=2)
        self.assertEqual(total_brightness, 1)

    def test_part2_turn_off_below_zero(self):
        """Test Part 2: turning off a light at brightness 0 should not go negative."""
        instructions = [
            "turn off 0,0 through 0,0",   # Should not decrease below 0
        ]
        _, total_brightness = process_instructions(instructions, part=2)
        self.assertEqual(total_brightness, 0)

    def test_empty_instructions(self):
        """Test with empty instruction list."""
        instructions = []
        lights_on, total_brightness = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 0)
        self.assertEqual(total_brightness, 0)

        lights_on, total_brightness = process_instructions(instructions, part=2)
        self.assertEqual(lights_on, 0)
        self.assertEqual(total_brightness, 0)

    def test_whitespace_only_lines(self):
        """Test with lines containing only whitespace."""
        instructions = ["   ", "\t", ""]
        lights_on, total_brightness = process_instructions(instructions, part=1)
        self.assertEqual(lights_on, 0)
        self.assertEqual(total_brightness, 0)

if __name__ == "__main__":
    # Allow running tests with --test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sys.argv = [sys.argv[0]]  # Clear argv for unittest
        unittest.main()
    else:
        main()
