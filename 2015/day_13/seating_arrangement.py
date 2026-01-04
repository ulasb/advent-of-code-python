#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 13: Knights of the Dinner Table

This script finds the optimal seating arrangement that maximizes total happiness
based on pairwise happiness changes when people sit next to each other.
"""

import argparse
import logging
import math
import sys
import time
import unittest
from collections import defaultdict
from itertools import permutations
from typing import DefaultDict, Dict, List, Tuple

# Constants
ME = "me"
GAIN = "gain"
LOSE = "lose"
DEFAULT_INPUT_FILE = "input.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_input(filename: str = DEFAULT_INPUT_FILE) -> DefaultDict[str, DefaultDict[str, int]]:
    """
    Parse the input file and build a happiness dictionary.

    Args:
        filename: Path to the input file

    Returns:
        DefaultDict[str, DefaultDict[str, int]]: happiness[person1][person2] = happiness change for person1 when next to person2

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the input file format is invalid
    """
    with open(filename, 'r') as f:
        return parse_happiness_lines(f)


def calculate_total_happiness(arrangement_tuple: Tuple[str, ...], happiness: DefaultDict[str, DefaultDict[str, int]]) -> int:
    """
    Calculate total happiness for a circular seating arrangement.

    Args:
        arrangement_tuple: Tuple of people in seating order
        happiness: Dictionary with happiness changes

    Returns:
        int: Total happiness score
    """
    total = 0
    n = len(arrangement_tuple)

    if n == 0:
        return 0  # No people, no happiness
    elif n == 1:
        return 0  # Single person has no neighbors
    elif n == 2:
        # Each person has one neighbor (the other person)
        person1, person2 = arrangement_tuple
        total += happiness[person1][person2]  # person1's happiness with person2
        total += happiness[person2][person1]  # person2's happiness with person1
        return total
    else:
        # For n >= 3, each person has two distinct neighbors in a circle
        for i in range(n):
            left = arrangement_tuple[i-1]  # Previous person (wraps around)
            right = arrangement_tuple[(i+1) % n]  # Next person
            current = arrangement_tuple[i]

            # Add happiness for both directions
            total += happiness[current][left]
            total += happiness[current][right]

        return total


def find_optimal_arrangement(happiness: DefaultDict[str, DefaultDict[str, int]]) -> Tuple[int, Tuple[str, ...]]:
    """
    Find the seating arrangement with maximum total happiness.

    Args:
        happiness: Dictionary with happiness changes

    Returns:
        Tuple[int, Tuple[str, ...]]: (max_happiness, best_arrangement)
    """
    people = sorted(list(happiness.keys()))  # Sort for consistent ordering
    n = len(people)
    max_happiness = float('-inf')
    best_arrangement = None

    # For circular arrangements, we can fix one person's position
    # This reduces complexity from n! to (n-1)! since rotations are equivalent
    if n == 0:
        num_arrangements = 1  # Empty arrangement
    else:
        num_arrangements = math.factorial(n - 1) if n > 1 else 1

    logger.info(f"Evaluating {n} people ({num_arrangements} unique circular arrangements)")

    start_time = time.time()

    if n == 0:
        # Handle empty case
        max_happiness = 0
        best_arrangement = ()
    elif n == 1:
        # Single person case
        arrangement = tuple(people)
        max_happiness = calculate_total_happiness(arrangement, happiness)
        best_arrangement = arrangement
    else:
        # For n >= 2, fix the first person and permute the rest
        fixed_person = people[0]
        remaining_people = people[1:]

        for perm in permutations(remaining_people):
            arrangement = (fixed_person,) + perm
            current_happiness = calculate_total_happiness(arrangement, happiness)
            if current_happiness > max_happiness:
                max_happiness = current_happiness
                best_arrangement = arrangement

    elapsed_time = time.time() - start_time
    logger.info(f"Evaluation took {elapsed_time:.2f}s")

    return max_happiness, best_arrangement


def add_yourself(happiness: DefaultDict[str, DefaultDict[str, int]]) -> None:
    """
    Add yourself ("me") to the happiness dictionary with zero happiness changes.

    For Advent of Code Part 2, we add ourselves with no happiness preference
    for sitting next to anyone, and no one has any happiness preference for
    sitting next to us.

    Args:
        happiness: Dictionary with happiness changes (modified in-place)
    """
    # Get all existing people
    existing_people = list(happiness.keys())

    # Add "me" with zero happiness for sitting next to anyone
    # (defaultdict will automatically return 0, but we'll be explicit)
    for person in existing_people:
        happiness[ME][person] = 0
        happiness[person][ME] = 0


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 13: Find optimal seating arrangement for maximum happiness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 seating_arrangement.py                    # Use default input.txt
  python3 seating_arrangement.py -f custom.txt     # Use custom input file
  python3 seating_arrangement.py --test           # Run unit tests
        """
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f'Input file containing happiness statements (default: {DEFAULT_INPUT_FILE})'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Run unit tests instead of main program'
    )

    return parser.parse_args()


def parse_happiness_lines(lines: List[str]) -> DefaultDict[str, DefaultDict[str, int]]:
    """
    Parse a list of happiness statement strings and build a happiness dictionary.
    Helper function for testing.

    Args:
        lines: List of strings in the format "Person would gain/lose X happiness units by sitting next to Person."

    Returns:
        DefaultDict[str, DefaultDict[str, int]]: happiness[person1][person2] = happiness change for person1 when next to person2
    """
    happiness = defaultdict(lambda: defaultdict(int))

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Parse: "Alice would gain 54 happiness units by sitting next to Bob."
        parts = line.split()

        # Validate line format
        if len(parts) != 11:
            raise ValueError(f"Invalid input line format: {line}")

        person1 = parts[0]
        change = parts[2]  # "gain" or "lose"
        amount_str = parts[3]
        person2 = parts[-1].rstrip('.')  # Remove period from last word

        # Validate change type
        if change not in (GAIN, LOSE):
            raise ValueError(f"Invalid change type '{change}' in line: {line}")

        # Validate amount
        try:
            amount = int(amount_str)
        except ValueError:
            raise ValueError(f"Invalid happiness amount '{amount_str}' in line: {line}")

        # Convert "lose" to negative
        if change == LOSE:
            amount = -amount

        happiness[person1][person2] = amount

    return happiness


class TestSeatingArrangement(unittest.TestCase):
    """Unit tests for the seating arrangement optimization."""

    def test_optimal_arrangement_small_case(self):
        """Test the optimal arrangement calculation with a small test case."""
        # Test data provided by user
        test_lines = [
            "Alice would gain 54 happiness units by sitting next to Bob.",
            "Alice would lose 79 happiness units by sitting next to Carol.",
            "Alice would lose 2 happiness units by sitting next to David.",
            "Bob would gain 83 happiness units by sitting next to Alice.",
            "Bob would lose 7 happiness units by sitting next to Carol.",
            "Bob would lose 63 happiness units by sitting next to David.",
            "Carol would lose 62 happiness units by sitting next to Alice.",
            "Carol would gain 60 happiness units by sitting next to Bob.",
            "Carol would gain 55 happiness units by sitting next to David.",
            "David would gain 46 happiness units by sitting next to Alice.",
            "David would lose 7 happiness units by sitting next to Bob.",
            "David would gain 41 happiness units by sitting next to Carol."
        ]

        happiness = parse_happiness_lines(test_lines)
        max_happiness, best_arrangement = find_optimal_arrangement(happiness)

        # Expected optimal happiness is 330
        self.assertEqual(max_happiness, 330)

        # Verify the arrangement produces the expected happiness
        calculated_happiness = calculate_total_happiness(best_arrangement, happiness)
        self.assertEqual(calculated_happiness, 330)

    def test_add_yourself(self):
        """Test adding yourself with zero happiness changes."""
        test_lines = [
            "Alice would gain 10 happiness units by sitting next to Bob.",
            "Bob would gain 20 happiness units by sitting next to Alice.",
        ]

        happiness = parse_happiness_lines(test_lines)

        # Before adding "me", should have 2 people
        self.assertEqual(len(happiness), 2)
        self.assertIn("Alice", happiness)
        self.assertIn("Bob", happiness)

        # Add "me"
        add_yourself(happiness)

        # Should now have 3 people
        self.assertEqual(len(happiness), 3)
        self.assertIn("me", happiness)

        # Check that "me" has zero happiness with everyone
        self.assertEqual(happiness["me"]["Alice"], 0)
        self.assertEqual(happiness["me"]["Bob"], 0)

        # Check that everyone has zero happiness with "me"
        self.assertEqual(happiness["Alice"]["me"], 0)
        self.assertEqual(happiness["Bob"]["me"], 0)

    def test_parse_happiness_lines_invalid_format(self):
        """Test that parse_happiness_lines raises ValueError for invalid input."""
        # Test invalid change type
        with self.assertRaises(ValueError):
            parse_happiness_lines(["Alice would invalid 10 happiness units by sitting next to Bob."])

        # Test invalid number
        with self.assertRaises(ValueError):
            parse_happiness_lines(["Alice would gain invalid happiness units by sitting next to Bob."])

        # Test incomplete line
        with self.assertRaises(ValueError):
            parse_happiness_lines(["Alice would gain"])

    def test_empty_arrangement(self):
        """Test behavior with empty arrangement."""
        happiness = defaultdict(lambda: defaultdict(int))
        # Empty tuple should return 0 happiness
        self.assertEqual(calculate_total_happiness((), happiness), 0)

    def test_single_person_arrangement(self):
        """Test arrangement with only one person."""
        happiness = defaultdict(lambda: defaultdict(int))
        happiness["Alice"]["Alice"] = 10  # Self-happiness doesn't make sense but test the logic
        arrangement = ("Alice",)
        # Single person has no neighbors, so happiness should be 0
        self.assertEqual(calculate_total_happiness(arrangement, happiness), 0)

    def test_find_optimal_with_empty_happiness(self):
        """Test find_optimal_arrangement with empty happiness dictionary."""
        happiness = defaultdict(lambda: defaultdict(int))
        max_happiness, best_arrangement = find_optimal_arrangement(happiness)
        # Empty arrangement has 0 happiness (no people, no unhappiness)
        self.assertEqual(max_happiness, 0)
        self.assertEqual(best_arrangement, ())

    def test_calculate_total_happiness(self):
        """Test the total happiness calculation for a specific arrangement."""
        test_lines = [
            "Alice would gain 54 happiness units by sitting next to Bob.",
            "Bob would gain 83 happiness units by sitting next to Alice.",
        ]

        happiness = parse_happiness_lines(test_lines)
        arrangement_tuple = ("Alice", "Bob")

        # For a 2-person arrangement, each person has one neighbor (the other person)
        # So we count: Alice with Bob (54) + Bob with Alice (83) = 137
        total = calculate_total_happiness(arrangement_tuple, happiness)
        self.assertEqual(total, 137)


def main(args: argparse.Namespace) -> None:
    """
    Main function to run the seating arrangement optimization.

    Args:
        args: Parsed command-line arguments
    """
    try:
        logger.info(f"Reading happiness data from {args.file}")
        happiness = parse_input(args.file)

        logger.info("Finding optimal arrangement for Part 1...")
        max_happiness, best_arrangement = find_optimal_arrangement(happiness)
        arrangement_str = ' -> '.join(best_arrangement)
        if best_arrangement:
            arrangement_str += f" -> {best_arrangement[0]}"
        logger.info(f"Optimal seating arrangement: {arrangement_str}")
        logger.info(f"Maximum total happiness: {max_happiness}")

        # Part 2: Add ourselves - with no happiness change for everyone
        logger.info(f"Adding '{ME}' to the arrangement for Part 2...")
        add_yourself(happiness)
        max_happiness, best_arrangement = find_optimal_arrangement(happiness)
        arrangement_str = ' -> '.join(best_arrangement)
        if best_arrangement:
            arrangement_str += f" -> {best_arrangement[0]}"
        logger.info(f"Optimal seating arrangement (including {ME}): {arrangement_str}")
        logger.info(f"Maximum total happiness (including {ME}): {max_happiness}")

    except FileNotFoundError:
        logger.error(f"Input file '{args.file}' not found.")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input format: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()

    if args.test:
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        main(args)
