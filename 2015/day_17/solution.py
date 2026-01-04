#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 17: No Such Thing as Too Much

This script finds all combinations of containers that sum to a target volume.
It follows the project guidelines for style, documentation, and performance.
"""

import argparse
import logging
import sys
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "input.txt"
TARGET_VOLUME = 150


def load_containers(filename: str = DEFAULT_INPUT_FILE) -> List[int]:
    """
    Reads a list of integer container sizes from the specified file.

    Parameters
    ----------
    filename : str
        Path to the input file.

    Returns
    -------
    List[int]
        A list of container sizes.

    Raises
    ------
    FileNotFoundError
        If the input file doesn't exist.
    ValueError
        If a line in the input file is not a valid integer.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def solve(containers: List[int], target: int) -> Dict[int, int]:
    """
    Calculates combinations using dynamic programming.

    This function tracks how many ways we can achieve a specific volume 
    using a specific number of containers.

    Parameters
    ----------
    containers : List[int]
        List of available container sizes.
    target : int
        The target volume to reach.

    Returns
    -------
    Dict[int, int]
        A dictionary where keys are the number of containers used 
        and values are the count of combinations for that number.
    """
    # ways[v] stores a dictionary: {num_containers: count_of_combinations}
    # where v is the volume reached.
    ways: List[defaultdict[int, int]] = [defaultdict(int) for _ in range(target + 1)]
    
    # Base case: 0 volume is reached using 0 containers in 1 way.
    ways[0][0] = 1

    for size in containers:
        # Iterate backwards through volumes to ensure each container is used once
        for v in range(target, size - 1, -1):
            prev_v = v - size
            for count, num_ways in ways[prev_v].items():
                new_count = count + 1
                ways[v][new_count] += num_ways

    return ways[target]


def main():
    """
    Main execution logic for the daily puzzle.
    """
    parser = argparse.ArgumentParser(description="Advent of Code 2015 - Day 17")
    parser.add_argument(
        "input_file",
        nargs="?",
        default=DEFAULT_INPUT_FILE,
        help="Input file containing container sizes",
    )
    args = parser.parse_args()

    try:
        containers = load_containers(args.input_file)
    except FileNotFoundError:
        logger.error(f"File {args.input_file} not found.")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Error parsing file: {e}")
        sys.exit(1)

    if not containers:
        logger.warning("No containers loaded.")
        return

    logger.info(f"Loaded {len(containers)} containers.")
    
    # Calculate combinations for the target volume
    matches_by_count = solve(containers, TARGET_VOLUME)

    if not matches_by_count:
        print(f"No combinations found for target {TARGET_VOLUME}.")
        return

    # Part 1: Total combinations reaching the target
    part1_total = sum(matches_by_count.values())
    print(f"Part 1: {part1_total}")

    # Part 2: Combinations using the absolute minimum number of containers
    min_containers = min(matches_by_count.keys())
    part2_total = matches_by_count[min_containers]
    print(f"Part 2: {part2_total}")


if __name__ == "__main__":
    main()
