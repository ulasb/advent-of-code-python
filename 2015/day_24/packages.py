#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 24: It Hangs in the Balance

This script finds the ideal configuration for balancing packages on a sleigh.
The code was created and published by Ulaş Bardak and is licensed under the
Mozilla Public License 2.0. The MPL 2.0 is a weak copyleft license that allows
for the modification and distribution of the code, but requires that any changes
to the code be made available under the same license.
"""

import sys
import argparse
import logging
from math import prod
from itertools import combinations
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "input.txt"


def find_min_packages(weights: List[int], target_weight: int) -> Optional[List[int]]:
    """
    Finds the smallest set of packages that sum to target_weight.

    If multiple sets of the same minimum size exist, returns the one with the
    smallest product (Quantum Entanglement).

    Parameters
    ----------
    weights : List[int]
        The list of package weights available.
    target_weight : int
        The target weight for the first group.

    Returns
    -------
    Optional[List[int]]
        The list of weights in the winning group, or None if no result is found.
    """
    # Try combinations of increasing size (1, 2, 3...)
    for r in range(1, len(weights) + 1):
        possible_sets = []
        for combo in combinations(weights, r):
            if sum(combo) == target_weight:
                possible_sets.append(list(combo))

        # If we found any sets of this size, find the one with the smallest product
        if possible_sets:
            return min(possible_sets, key=prod)

    return None


def read_weights(filename: str = DEFAULT_INPUT_FILE) -> List[int]:
    """
    Reads the weights from the input file.

    Parameters
    ----------
    filename : str, optional
        The path to the input file (default is "input.txt").

    Returns
    -------
    List[int]
        A list of integer weights.

    Raises
    ------
    FileNotFoundError
        If the input file doesn't exist.
    """
    weights = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    weights.append(int(line))
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found.")
    return weights


def parse_args():
    """
    Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 Day 24 Solver"
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=DEFAULT_INPUT_FILE,
        help="Path to the input file (default: input.txt)",
    )
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_args()

    try:
        weights = read_weights(args.file)
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid data in file: {e}")
        sys.exit(1)

    total_weight = sum(weights)

    # Part 1: Divide into 3 groups
    if total_weight % 3 == 0:
        logger.info("Part 1: Balancing into 3 groups")
        target_p1 = total_weight // 3
        best_group_p1 = find_min_packages(weights, target_p1)
        if best_group_p1:
            logger.info(f"Minimum package count: {len(best_group_p1)}")
            logger.info(f"Quantum Entanglement: {prod(best_group_p1)}")
        else:
            logger.warning("No solution found for Part 1.")
    else:
        logger.error(f"Total weight {total_weight} not divisible by 3.")

    # Part 2: Divide into 4 groups
    if total_weight % 4 == 0:
        logger.info("Part 2: Balancing into 4 groups")
        target_p2 = total_weight // 4
        best_group_p2 = find_min_packages(weights, target_p2)
        if best_group_p2:
            logger.info(f"Minimum package count: {len(best_group_p2)}")
            logger.info(f"Quantum Entanglement: {prod(best_group_p2)}")
        else:
            logger.warning("No solution found for Part 2.")
    else:
        logger.error(f"Total weight {total_weight} not divisible by 4.")


if __name__ == "__main__":
    main()
