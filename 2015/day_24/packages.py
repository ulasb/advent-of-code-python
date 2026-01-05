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


def can_partition(weights: List[int], target: int, num_groups: int) -> bool:
    """
    Checks if the given weights can be partitioned into num_groups of weight target.

    Parameters
    ----------
    weights : List[int]
        The weights to partition.
    target : int
        The target weight for each group.
    num_groups : int
        The number of groups to form.

    Returns
    -------
    bool
        True if partitioning is possible, False otherwise.
    """
    if num_groups == 1:
        return sum(weights) == target

    def search(current_target: int, start_idx: int, current_weights: List[int]) -> bool:
        if current_target == 0:
            # We found one group of the target weight.
            # Now we check if the remaining weights can form the next group.
            return can_partition(current_weights, target, num_groups - 1)

        for i in range(start_idx, len(current_weights)):
            w = current_weights[i]
            if w <= current_target:
                # Recurse while removing the selected weight from the options
                new_weights = current_weights[:i] + current_weights[i + 1 :]
                if search(current_target - w, i, new_weights):
                    return True
        return False

    return search(target, 0, sorted(weights, reverse=True))


def find_min_packages(
    weights: List[int], target_weight: int, num_groups: int
) -> Optional[List[int]]:
    """
    Finds the smallest set of packages that sum to target_weight and can be
    partitioned into the required number of groups.

    If multiple sets of the same minimum size exist, returns the one with the
    smallest product (Quantum Entanglement).

    Parameters
    ----------
    weights : List[int]
        The list of package weights available.
    target_weight : int
        The target weight for each group.
    num_groups : int
        The total number of groups to form.

    Returns
    -------
    Optional[List[int]]
        The list of weights in the winning group, or None if no result is found.
    """
    # Sort weights descending for faster pruning in later steps
    weights = sorted(weights, reverse=True)

    # Try combinations of increasing size (1, 2, 3...)
    for r in range(1, len(weights) + 1):
        # Find all combinations of size r that sum to the target
        valid_combos = [
            list(c) for c in combinations(weights, r) if sum(c) == target_weight
        ]

        if not valid_combos:
            continue

        # Sort combinations by product (Quantum Entanglement) to find the best first
        valid_combos.sort(key=prod)

        for combo in valid_combos:
            # Verify if the remaining weights can be partitioned correctly
            remaining = list(weights)
            for w in combo:
                remaining.remove(w)

            if can_partition(remaining, target_weight, num_groups - 1):
                return combo

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
    try:
        with open(filename, "r") as f:
            return [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found.")


def parse_args():
    """
    Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Advent of Code 2015 Day 24 Solver")
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

    # Solve for 3 groups (Part 1) and 4 groups (Part 2)
    for num_groups, part_num in [(3, 1), (4, 2)]:
        if total_weight % num_groups == 0:
            logger.info(f"Part {part_num}: Balancing into {num_groups} groups")
            target_weight = total_weight // num_groups
            best_group = find_min_packages(weights, target_weight, num_groups)

            if best_group:
                logger.info(f"Minimum package count: {len(best_group)}")
                logger.info(f"Quantum Entanglement: {prod(best_group)}")
            else:
                logger.warning(f"No solution found for Part {part_num}.")
        else:
            logger.error(f"Total weight {total_weight} not divisible by {num_groups}.")


if __name__ == "__main__":
    main()
