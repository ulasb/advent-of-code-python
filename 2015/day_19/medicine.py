#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 19: Medicine for Rudolph

This script calculates the number of unique molecules possible after one replacement
(Part 1) and the minimum number of steps to transform 'e' into a target molecule (Part 2).

Code created and published by Ulaş Bardak.
Licensed under the Mozilla Public License 2.0.
"""

import argparse
import logging
import random
import unittest
from typing import List, Set, Tuple


# Constants
DEFAULT_INPUT_FILE = "input.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def read_input(input_file: str = DEFAULT_INPUT_FILE) -> Tuple[List[List[str]], str]:
    """
    Reads the input file and returns the replacements and the original molecule.

    Args:
        input_file: The path to the input file, by default "input.txt"

    Returns:
        Tuple[List[List[str]], str]: A tuple containing a list of replacements
        (list of [from, to] pairs) and the original molecule string.

    Raises:
        FileNotFoundError: If the input file doesn't exist.
    """
    replacements = []
    try:
        with open(input_file, "r") as f:
            content = f.read()
        
        replacements_str, molecule_str = content.strip().split("\n\n")
        
        replacements.extend(line.split(" => ") for line in replacements_str.splitlines())
    except FileNotFoundError:
        logger.error(f"Error: Input file '{input_file}' not found.")
        raise

    return replacements, molecule_str


def solve_part1(molecule: str, replacements: List[List[str]]) -> int:
    """
    Calculates the number of unique molecules that can be created with one replacement.

    Args:
        molecule: The starting molecule string.
        replacements: A list of [from, to] replacement pairs.

    Returns:
        int: The number of unique molecules.
    """
    molecules: Set[str] = set()
    for replacement_from, replacement_to in replacements:
        start_position = 0
        while True:
            start_position = molecule.find(replacement_from, start_position)
            if start_position == -1:
                break
            new_molecule = (
                molecule[:start_position]
                + replacement_to
                + molecule[start_position + len(replacement_from) :]
            )
            molecules.add(new_molecule)
            start_position += 1
    return len(molecules)


def solve_part2(target: str, replacements: List[List[str]]) -> int:
    """
    Calculates the minimum number of steps to go from 'e' to the target molecule.
    Uses a greedy reduction search from the target back to 'e'.

    Args:
        target: The target molecule string.
        replacements: A list of [from, to] replacement pairs.

    Returns:
        int: The minimum number of steps.
    """
    # A backward search from the target molecule to "e" is much more efficient.
    # Since the grammar is mostly reductions when going backwards, we can often
    # find the path by greedily applying replacements. If we get stuck, we shuffle
    # the replacements and start over.
    reverse_replacements = [(to, from_) for from_, to in replacements]

    # Sort replacements by length (descending) to favor longer reductions
    reverse_replacements.sort(key=lambda x: len(x[0]), reverse=True)

    molecule = target
    steps = 0

    while molecule != "e":
        changed = False
        for mol_from, mol_to in reverse_replacements:
            if mol_from in molecule:
                # Replace the LAST occurrence of mol_from with mol_to
                # This often works better for AoC grammars, though first occurrence also works.
                # Here we use replace(..., 1) which replaces the first occurrence.
                molecule = molecule.replace(mol_from, mol_to, 1)
                steps += 1
                changed = True
                break

        if not changed:
            # We got stuck, shuffle replacements and try again from the target molecule
            random.shuffle(reverse_replacements)
            molecule = target
            steps = 0

    return steps


class TestMedicine(unittest.TestCase):
    """Unit tests for the solution."""

    def test_example_part1(self):
        """Test Part 1 with a simple example."""
        replacements = [["H", "HO"], ["H", "OH"], ["O", "HH"]]
        self.assertEqual(solve_part1("HOH", replacements), 4)
        self.assertEqual(solve_part1("HOHOHO", replacements), 7)

    def test_example_part2(self):
        """Test Part 2 with a simple example."""
        replacements = [["e", "H"], ["e", "O"], ["H", "HO"], ["H", "OH"], ["O", "HH"]]
        self.assertEqual(solve_part2("HOH", replacements), 3)


def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Advent of Code 2015 - Day 19")
    parser.add_argument(
        "--file",
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f"Input file path (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--test", action="store_true", help="Run unit tests instead of the solution"
    )
    return parser.parse_args()


def main():
    """
    Main entry point for the script.
    """
    args = parse_arguments()

    if args.test:
        unittest.main(argv=[""], exit=False)
        return

    try:
        replacements, original_molecule = read_input(args.file)

        # Part 1
        part1_result = solve_part1(original_molecule, replacements)
        logger.info(f"Part 1: {part1_result}")

        # Part 2
        part2_result = solve_part2(original_molecule, replacements)
        logger.info(f"Part 2: {part2_result}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()