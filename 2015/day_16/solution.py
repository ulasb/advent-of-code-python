#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 16: Aunt Sue

This script parses a list of "Aunt Sue" objects with various attributes and finds
the one that matches a specific set of criteria.

Part 1: Exact match on known attributes.
Part 2: Range-based match on specific attributes (cats, trees, pomeranians, goldfish).
"""

import argparse
import logging
import operator
import re
import sys
import unittest
from typing import Dict, List, Optional

# Constants
DEFAULT_INPUT_FILE = "input.txt"
TARGET_ATTRIBUTES = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

PART_2_CHECKS = {
    "cats": operator.gt,
    "trees": operator.gt,
    "pomeranians": operator.lt,
    "goldfish": operator.lt,
}

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class Aunt:
    """
    Represents an Aunt Sue with a name and a set of attributes.
    """

    def __init__(self, name: str, attributes: Dict[str, int]):
        """
        Initialize an Aunt object.

        Args:
            name: The name of the aunt (e.g., "Sue 1").
            attributes: A dictionary of attributes (e.g., {"cars": 2, "perfumes": 1}).
        """
        self.name = name
        self.attributes = attributes

    def __repr__(self) -> str:
        attr_str = ", ".join(f"{k}={v}" for k, v in self.attributes.items())
        return f"Aunt(name='{self.name}', {attr_str})"


def parse_line(line: str) -> Optional[Aunt]:
    """
    Parse a single line of input into an Aunt object.
    Example line: "Sue 1: children: 1, cars: 8"

    Args:
        line: The input line to parse.

    Returns:
        Optional[Aunt]: The parsed Aunt object, or None if parsing fails.
    """
    # Splits "Sue 1: children: 1, cars: 8" into name="Sue 1" and attributes
    name_part, sep, raw_attrs = line.partition(":")
    if not sep:
        return None

    name = name_part.strip()
    raw_attrs = raw_attrs.strip()

    attributes = {}
    # Split by comma to get "key: value" pairs
    parts = raw_attrs.split(",")
    for part in parts:
        if ":" in part:
            key, value_str = part.split(":", 1)
            key = key.strip()
            try:
                value = int(value_str.strip())
                attributes[key] = value
            except ValueError:
                continue

    return Aunt(name, attributes)


def parse_input(filename: str = DEFAULT_INPUT_FILE) -> List[Aunt]:
    """
    Parse the input file and return a list of Aunt objects.

    Args:
        filename: Path to the input file.

    Returns:
        List[Aunt]: A list of parsed Aunt objects.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    aunts = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            aunt = parse_line(line)
            if aunt:
                aunts.append(aunt)
    return aunts


def find_matching_aunt_exact(aunts: List[Aunt], aunt_to_be_matched: Aunt) -> Optional[Aunt]:
    """
    Find an aunt that matches the target aunt's attributes exactly.
    Only attributes present on the candidate aunt are checked against the target.

    Args:
        aunts: List of candidate Aunt objects.
        aunt_to_be_matched: The target Aunt object with all criteria.

    Returns:
        Optional[Aunt]: The matching Aunt object, or None if not found.
    """
    for aunt in aunts:
        # Check if all existing attributes match the target's attributes
        match = all(
            value == aunt_to_be_matched.attributes.get(key)
            for key, value in aunt.attributes.items()
            if key in aunt_to_be_matched.attributes
        )
        if match:
            return aunt
    return None


def find_matching_aunt_ranges(aunts: List[Aunt], aunt_to_be_matched: Aunt) -> Optional[Aunt]:
    """
    Find an aunt that matches the target aunt's attributes with ranges.
    - cats, trees: candidates must have GREATER than the target value.
    - pomeranians, goldfish: candidates must have FEWER than the target value.
    - others: candidates must have EXACTLY the target value.

    Args:
        aunts: List of candidate Aunt objects.
        aunt_to_be_matched: The target Aunt object with all criteria.

    Returns:
        Optional[Aunt]: The matching Aunt object, or None if not found.
    """
    for aunt in aunts:
        match = True
        for key, value in aunt.attributes.items():
            if key in aunt_to_be_matched.attributes:
                target_val = aunt_to_be_matched.attributes[key]
                # Use operator.eq as default comparison
                op = PART_2_CHECKS.get(key, operator.eq)
                if not op(value, target_val):
                    match = False
                    break
        if match:
            return aunt
    return None


class TestAuntMatching(unittest.TestCase):
    """Unit tests for Aunt matching logic."""

    def setUp(self):
        self.target_aunt = Aunt("Target", TARGET_ATTRIBUTES)

    def test_find_matching_aunt_exact(self):
        """Test exact matching logic."""
        aunt1 = Aunt("Sue 1", {"cars": 2, "children": 3})  # Should match
        aunt2 = Aunt("Sue 2", {"cars": 3, "children": 3})  # Should fail (cars mismatch)

        self.assertEqual(find_matching_aunt_exact([aunt1], self.target_aunt), aunt1)
        self.assertIsNone(find_matching_aunt_exact([aunt2], self.target_aunt))

    def test_find_matching_aunt_ranges(self):
        """Test range-based matching logic (Part 2)."""
        # "cats" > 7
        aunt_cats_match = Aunt("Sue Cats", {"cats": 8})
        aunt_cats_fail = Aunt("Sue Cats Fail", {"cats": 7})

        # "pomeranians" < 3
        aunt_pom_match = Aunt("Sue Pom", {"pomeranians": 1})
        aunt_pom_fail = Aunt("Sue Pom Fail", {"pomeranians": 3})

        self.assertEqual(find_matching_aunt_ranges([aunt_cats_match], self.target_aunt), aunt_cats_match)
        self.assertIsNone(find_matching_aunt_ranges([aunt_cats_fail], self.target_aunt))

        self.assertEqual(find_matching_aunt_ranges([aunt_pom_match], self.target_aunt), aunt_pom_match)
        self.assertIsNone(find_matching_aunt_ranges([aunt_pom_fail], self.target_aunt))


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 16: Aunt Sue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f"Input file containing aunt data (default: {DEFAULT_INPUT_FILE})",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run unit tests instead of main program",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main function to run the Aunt matching.
    """
    args = parse_arguments()

    if args.test:
        sys.argv = [sys.argv[0]]  # Reset sys.argv for unittest
        unittest.main(exit=True, verbosity=2)
        return

    try:
        logger.info(f"Reading data from {args.file}")
        aunts = parse_input(args.file)
        logger.info(f"Successfully parsed {len(aunts)} Aunt objects.")

        # Define the target aunt (Sender) using the global constant
        aunt_to_be_matched = Aunt("Sender", TARGET_ATTRIBUTES)

        # Part 1
        logger.info("Finding match for Part 1 (Exact match)...")
        match_part1 = find_matching_aunt_exact(aunts, aunt_to_be_matched)
        if match_part1:
            print(f"Part 1: {match_part1.name}")
        else:
            print("Part 1: No match found.")

        # Part 2
        logger.info("Finding match for Part 2 (Ranges)...")
        match_part2 = find_matching_aunt_ranges(aunts, aunt_to_be_matched)
        if match_part2:
            print(f"Part 2: {match_part2.name}")
        else:
            print("Part 2: No match found.")

    except FileNotFoundError:
        logger.error(f"Input file '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
