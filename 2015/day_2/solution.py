#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 2: I Was Told There Would Be No Math

This script reads present dimensions from a file and processes them.
Each line contains three dimensions separated by 'x'.
"""

import sys
import argparse
import unittest
import cProfile
import pstats
from typing import List, Tuple

# Constants
EXPECTED_DIMENSIONS = 3
DOUBLE_FACTOR = 2
MAX_REASONABLE_DIMENSION = 10000  # Sanity check for dimension values


def validate_dimensions(dimensions: List[int], line_num: int, line: str) -> bool:
    """
    Validate that dimensions are reasonable positive integers.

    Args:
        dimensions: List of dimension values
        line_num: Line number for error reporting
        line: Original line content for error reporting

    Returns:
        True if valid, False otherwise
    """
    for i, dim in enumerate(dimensions):
        if dim <= 0:
            print(f"Warning: Line {line_num} contains non-positive dimension {dim} at position {i+1}: {line}")
            return False
        if dim > MAX_REASONABLE_DIMENSION:
            print(f"Warning: Line {line_num} contains unreasonably large dimension {dim} at position {i+1}: {line}")
            return False
    return True


def read_present_dimensions(filename: str) -> List[List[int]]:
    """
    Read present dimensions from a file.

    Args:
        filename: Path to the input file

    Returns:
        List of lists, where each inner list contains three integers
        representing the dimensions of a present (sorted in ascending order)
    """
    presents = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                # Remove whitespace and split by 'x'
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                # Split by 'x' and convert to integers
                try:
                    parts = line.split('x')
                    if len(parts) != EXPECTED_DIMENSIONS:
                        print(f"Warning: Line {line_num} does not contain exactly {EXPECTED_DIMENSIONS} dimensions: {line}")
                        continue

                    dimensions = [int(dim) for dim in parts]
                    if not validate_dimensions(dimensions, line_num, line):
                        continue
                    dimensions.sort()
                    presents.append(dimensions)
                except ValueError as e:
                    print(f"Error on line {line_num}: Could not parse dimensions from '{line}' - {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error on line {line_num}: {e}")
                    continue

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{filename}'.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: File '{filename}' contains invalid UTF-8 characters.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading file '{filename}': {e}")
        sys.exit(1)

    return presents

def get_ribbon_length(presents: List[List[int]]) -> int:
    """
    Calculate the length of ribbon needed for a list of presents.

    Args:
        presents: List of present dimensions, each as a sorted list of 3 integers

    Returns:
        Total ribbon length needed (wrap + bow)
    """
    return sum(
        # Bow: volume of present
        p[0] * p[1] * p[2] +
        # Wrap: shortest distance around sides (first two dimensions after sorting)
        DOUBLE_FACTOR * p[0] + DOUBLE_FACTOR * p[1]
        for p in presents
    )
        

def get_total_wrapping_paper(presents: List[List[int]]) -> int:
    """
    Calculate the total wrapping paper required for a list of presents.

    Args:
        presents: List of present dimensions, each as a sorted list of 3 integers

    Returns:
        Total square feet of wrapping paper needed
    """
    def calculate_paper_for_present(p: List[int]) -> int:
        """Calculate wrapping paper needed for a single present."""
        # Areas of all three faces
        area1, area2, area3 = p[0]*p[1], p[1]*p[2], p[0]*p[2]
        # Total surface area (double each face) plus slack (smallest face)
        return DOUBLE_FACTOR*area1 + DOUBLE_FACTOR*area2 + DOUBLE_FACTOR*area3 + area1

    return sum(calculate_paper_for_present(p) for p in presents)


def main() -> None:
    """
    Main function to handle command line arguments and process the input file.
    """
    parser = argparse.ArgumentParser(
        description='Read present dimensions from a file for Advent of Code Day 2'
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        default='input.txt',
        help='Path to input file (default: input.txt)'
    )
    parser.add_argument(
        '--profile',
        action='store_true',
        help='Enable performance profiling'
    )

    args = parser.parse_args()

    def run_calculations():
        """Run the main calculations - extracted for profiling."""
        # Read the present dimensions
        presents = read_present_dimensions(args.input_file)
        print(f"Successfully read {len(presents)} presents from '{args.input_file}'")

        # Calculate wrapping paper and ribbon
        total_wrapping_paper = get_total_wrapping_paper(presents)
        total_ribbon_length = get_ribbon_length(presents)

        print(f"Total wrapping paper needed {total_wrapping_paper}")
        print(f"Total ribbon length needed {total_ribbon_length}")

    if args.profile:
        print("Running with performance profiling enabled...")
        profiler = cProfile.Profile()
        profiler.enable()
        run_calculations()
        profiler.disable()

        # Print profiling statistics
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        print("\n=== Performance Profile (Top 10 functions by cumulative time) ===")
        stats.print_stats(10)
    else:
        run_calculations()


class TestWrappingPaper(unittest.TestCase):
    """Test cases for the wrapping paper and ribbon calculations."""

    def assert_wrapping_paper_calculation(self, dimensions: List[int], expected: int, description: str):
        """Helper method to test wrapping paper calculations."""
        with self.subTest(dimensions=dimensions, expected=expected):
            result = get_total_wrapping_paper([dimensions])
            self.assertEqual(result, expected, f"Failed for {description}")

    def assert_ribbon_calculation(self, dimensions: List[int], expected: int, description: str):
        """Helper method to test ribbon calculations."""
        with self.subTest(dimensions=dimensions, expected=expected):
            result = get_ribbon_length([dimensions])
            self.assertEqual(result, expected, f"Failed for {description}")

    def test_wrapping_paper_calculations(self):
        """Test wrapping paper calculations for various present dimensions."""
        self.assert_wrapping_paper_calculation([2, 3, 4], 58, "2x3x4 present")
        self.assert_wrapping_paper_calculation([1, 1, 10], 43, "1x1x10 present")

    def test_multiple_presents(self):
        """Test wrapping paper calculation for multiple presents."""
        presents = [[2, 3, 4], [1, 1, 10]]
        result = get_total_wrapping_paper(presents)
        # 58 + 43 = 101
        self.assertEqual(result, 101)

    def test_empty_list(self):
        """Test wrapping paper calculation for an empty list of presents."""
        presents = []
        result = get_total_wrapping_paper(presents)
        self.assertEqual(result, 0)

    def test_ribbon_calculations(self):
        """Test ribbon length calculations for various present dimensions."""
        self.assert_ribbon_calculation([2, 3, 4], 34, "2x3x4 present")
        self.assert_ribbon_calculation([1, 1, 10], 14, "1x1x10 present")

    def test_ribbon_multiple_presents(self):
        """Test ribbon length calculation for multiple presents."""
        presents = [[2, 3, 4], [1, 1, 10]]
        result = get_ribbon_length(presents)
        # 34 + 14 = 48
        self.assertEqual(result, 48)

    def test_ribbon_empty_list(self):
        """Test ribbon length calculation for an empty list of presents."""
        presents = []
        result = get_ribbon_length(presents)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    # Check if running tests
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        main()
