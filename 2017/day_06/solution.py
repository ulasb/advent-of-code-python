"""
Advent of Code 2017, Day 6: Memory Reallocation

This script solves the memory redistribution problem where blocks are balanced
among memory banks until a configuration is seen again.

Created and published by Ulaş Bardak.
License: Mozilla Public License 2.0 (MPL 2.0).
High-level description: MPL 2.0 is a copyleft license that is easy to comply with.
You can use the code in a larger work, but you must make the source code of the
MPL-licensed files available if you distribute it.
"""

import sys
import os
from typing import List, Tuple, Dict, Optional


def redistribute(banks: List[int]) -> List[int]:
    """
    Perform one cycle of redistribution on the memory banks.

    Parameters
    ----------
    banks : List[int]
        The current state of the memory banks.

    Returns
    -------
    List[int]
        The new state of the memory banks after redistribution.
    """
    new_banks = list(banks)
    num_banks = len(new_banks)
    if num_banks == 0:
        return new_banks

    # Find the bank with the most blocks. Ties won by lowest-numbered bank.
    max_blocks = max(new_banks)
    max_index = new_banks.index(max_blocks)

    # Remove all blocks from the selected bank.
    blocks_to_distribute = new_banks[max_index]
    new_banks[max_index] = 0

    # Redistribute the blocks starting from the next bank.
    current_index = (max_index + 1) % num_banks
    while blocks_to_distribute > 0:
        new_banks[current_index] += 1
        blocks_to_distribute -= 1
        current_index = (current_index + 1) % num_banks

    return new_banks


def solve(initial_banks: List[int]) -> Tuple[int, int]:
    """
    Find how many cycles it takes to see a repeated state and the size of the loop.

    Parameters
    ----------
    initial_banks : List[int]
        The starting block counts in each memory bank.

    Returns
    -------
    Tuple[int, int]
        (cycles_until_repeat, loop_size)
    """
    seen_states: Dict[Tuple[int, ...], int] = {}
    current_banks = list(initial_banks)
    cycles = 0

    while tuple(current_banks) not in seen_states:
        seen_states[tuple(current_banks)] = cycles
        current_banks = redistribute(current_banks)
        cycles += 1

    first_seen_cycle = seen_states[tuple(current_banks)]
    loop_size = cycles - first_seen_cycle

    return cycles, loop_size


def main(input_file: str = "input.txt") -> None:
    """
    Main entry point for the script.

    Parameters
    ----------
    input_file : str, optional
        Path to the input file, by default "input.txt".
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    try:
        with open(input_file, "r") as f:
            line = f.read().strip()
            if not line:
                print("Error: Input file is empty.")
                return
            # Input is typically a tab/space separated list of numbers
            initial_banks = [int(x) for x in line.split()]
    except ValueError as e:
        print(f"Error: Invalid input format. Expected space-separated integers. {e}")
        return
    except Exception as e:
        print(f"Error: Unexpected error reading input. {e}")
        return

    part1, part2 = solve(initial_banks)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    # Use command line argument for input file if provided, else default to input.txt
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    main(input_path)
