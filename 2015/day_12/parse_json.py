#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 12: JSAbacusFramework.io

Solution for summing numbers in JSON structures.
Part 1: Sum all numbers in the JSON
Part 2: Sum all numbers, ignoring objects that contain "red"
"""

import json
import sys
import os
import argparse
import unittest
from typing import Any, Union, Optional

def read_input(filename: str) -> str:
    """
    Read the input file and return the contents.

    Args:
        filename: Path to the input file

    Returns:
        The file contents as a string

    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there's an error reading the file
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except IOError as e:
        raise IOError(f"Error reading file '{filename}': {e}") from e

def parse_json(json_string: str) -> Any:
    """
    Parse the JSON string into a Python object.

    Args:
        json_string: Valid JSON string

    Returns:
        Parsed JSON object (dict, list, etc.)

    Raises:
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error parsing JSON: {e}", e.doc, e.pos)


# Constants
RED_VALUE = "red"

def sum_numbers(obj: Any, bad_value: Optional[str] = None) -> int:
    """
    Recursively traverse the JSON object and sum all numbers.

    For Part 2, if bad_value is specified and any dictionary contains
    bad_value as a value, that entire dictionary is ignored.

    Args:
        obj: JSON object (dict, list, or primitive)
        bad_value: Value that causes entire dictionaries to be ignored

    Returns:
        Sum of all numbers in the structure
    """
    total = 0

    if isinstance(obj, dict):
        # For dictionaries, check if bad_value is present
        if bad_value is not None and bad_value in obj.values():
            return 0  # Ignore this entire dictionary
        # Otherwise, recurse through all values
        for value in obj.values():
            total += sum_numbers(value, bad_value)
    elif isinstance(obj, list):
        # For lists, recurse through all items
        for item in obj:
            total += sum_numbers(item, bad_value)
    elif isinstance(obj, (int, float)):
        # For numbers, add their integer value to the total
        total += int(obj)
    # Ignore strings, booleans, and null values (implicitly return 0)

    return total


class TestJSONSum(unittest.TestCase):
    """Unit tests for Advent of Code Day 12 JSON summing functions."""

    def test_part1_basic_arrays_and_objects(self):
        """Test Part 1: basic arrays and objects."""
        # [1,2,3] and {"a":2,"b":4} both have a sum of 6
        self.assertEqual(sum_numbers([1, 2, 3]), 6)
        self.assertEqual(sum_numbers({"a": 2, "b": 4}), 6)

    def test_part1_nested_structures(self):
        """Test Part 1: nested structures."""
        # [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3
        self.assertEqual(sum_numbers([[[3]]]), 3)
        self.assertEqual(sum_numbers({"a": {"b": 4}, "c": -1}), 3)

    def test_part1_zero_sum_cases(self):
        """Test Part 1: cases that sum to zero."""
        # {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0
        self.assertEqual(sum_numbers({"a": [-1, 1]}), 0)
        self.assertEqual(sum_numbers([-1, {"a": 1}]), 0)

    def test_part1_empty_structures(self):
        """Test Part 1: empty structures."""
        # [] and {} both have a sum of 0
        self.assertEqual(sum_numbers([]), 0)
        self.assertEqual(sum_numbers({}), 0)

    def test_part2_basic_case(self):
        """Test Part 2: basic case still works."""
        # [1,2,3] still has a sum of 6
        self.assertEqual(sum_numbers([1, 2, 3], RED_VALUE), 6)

    def test_part2_ignore_red_object(self):
        """Test Part 2: ignore object containing red."""
        # [1,{"c":"red","b":2},3] now has a sum of 4
        self.assertEqual(sum_numbers([1, {"c": RED_VALUE, "b": 2}, 3], RED_VALUE), 4)

    def test_part2_ignore_entire_structure(self):
        """Test Part 2: ignore entire structure with red."""
        # {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0
        self.assertEqual(sum_numbers({"d": RED_VALUE, "e": [1, 2, 3, 4], "f": 5}, RED_VALUE), 0)

    def test_part2_red_in_array_no_effect(self):
        """Test Part 2: red in array has no effect."""
        # [1,"red",5] has a sum of 6
        self.assertEqual(sum_numbers([1, RED_VALUE, 5], RED_VALUE), 6)


def main(input_file: Optional[str] = None):
    """Main solution function."""
    # Get the input file path
    if input_file:
        script_dir = os.path.dirname(__file__)
        input_file = os.path.join(script_dir, input_file)
    else:
        input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

    try:
        # Read and parse the input
        json_string = read_input(input_file)
        data = parse_json(json_string)

        # Part 1: Sum all numbers
        part1_result = sum_numbers(data)
        print(f"Part 1 - Sum of all numbers: {part1_result}")

        # Part 2: Sum all numbers, ignoring objects with "red"
        part2_result = sum_numbers(data, RED_VALUE)
        print(f"Part 2 - Sum ignoring '{RED_VALUE}' objects: {part2_result}")

    except (FileNotFoundError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        sys.exit(1)

def run_tests(verbose: bool = False):
    """Run the unit test suite."""
    if verbose:
        print("Running unit tests (verbose mode)...")
        verbosity = 2
    else:
        print("Running unit tests...")
        verbosity = 1

    unittest.main(argv=[''], exit=False, verbosity=verbosity)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 12: JSAbacusFramework.io",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse_json.py              # Run tests then solve both parts
  python parse_json.py --test-only  # Run only unit tests
  python parse_json.py --no-tests   # Skip tests, solve only
  python parse_json.py --verbose    # Run tests with verbose output
  python parse_json.py --input-file custom.json  # Use custom input file
        """
    )

    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Run only the unit tests, do not solve the puzzle'
    )

    parser.add_argument(
        '--no-tests',
        action='store_true',
        help='Skip running unit tests, solve the puzzle only'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose test output'
    )

    parser.add_argument(
        '--input-file',
        type=str,
        help='Path to input file (default: input.txt in script directory)'
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    # Validate argument combinations
    if args.test_only and args.no_tests:
        parser.error("--test-only and --no-tests cannot be used together")

    if args.test_only:
        # Run only tests
        run_tests(verbose=args.verbose)
    elif args.no_tests:
        # Skip tests, run only main solution
        main(input_file=args.input_file)
    else:
        # Default: Run tests first, then main solution
        run_tests(verbose=args.verbose)
        print("\n" + "="*50)
        main(input_file=args.input_file)
