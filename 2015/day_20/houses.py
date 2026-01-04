"""
This script was created and published by Ulaş Bardak.
It is licensed under the Mozilla Public License 2.0 (MPL 2.0).
The MPL 2.0 is a permissive, file-level license that allows for the integration of 
this code into larger works, provided that the source code of this file remains 
available under the MPL 2.0.

Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
"""

import numpy as np

# Constants based on the problem description
MIN_PRESENTS_GOAL = 29000000
PART1_PRESENTS_PER_ELF = 10
PART2_PRESENTS_PER_ELF = 11
PART2_MAX_HOUSES_PER_ELF = 50


def solve_part1(goal: int) -> int | None:
    """
    Find the lowest house number that receives at least the goal number of presents.
    
    In Part 1, each elf delivers 10 times their ID in presents to every multiple of their ID.

    Parameters
    ----------
    goal : int
        The minimum number of presents a house must receive.

    Returns
    -------
    int | None
        The number of the first house to reach the goal, or None if not found.
    """
    # Each elf contributes 10 * its ID. We can divide the goal by 10 to work with smaller numbers.
    target_sum_per_house = goal // PART1_PRESENTS_PER_ELF
    # A practical upper bound for the house number is the target itself.
    max_house_limit = target_sum_per_house

    house_presents_counts = np.zeros(max_house_limit + 1, dtype=int)

    for elf_id in range(1, max_house_limit + 1):
        # Elf 'elf_id' delivers 'elf_id' presents to houses elf_id, 2*elf_id, 3*elf_id, ...
        # Using numpy slicing for high performance
        house_presents_counts[elf_id::elf_id] += elf_id

        # Once we've processed elf 'N', the count for house 'N' is finalized
        # because any elf with an ID > N will only visit houses > N.
        if house_presents_counts[elf_id] >= target_sum_per_house:
            return elf_id
    return None


def solve_part2(goal: int) -> int | None:
    """
    Find the lowest house number that receives at least the goal number of presents in Part 2.
    
    In Part 2, each elf delivers 11 times their ID in presents to 50 houses.

    Parameters
    ----------
    goal : int
        The minimum number of presents a house must receive.

    Returns
    -------
    int | None
        The number of the first house to reach the goal, or None if not found.
    """
    # In Part 2, each elf delivers 11 * its ID, but only to 50 houses.
    target_sum_per_house = (goal + PART2_PRESENTS_PER_ELF - 1) // PART2_PRESENTS_PER_ELF
    max_house_limit = target_sum_per_house

    house_presents_counts = np.zeros(max_house_limit + 1, dtype=int)

    for elf_id in range(1, max_house_limit + 1):
        # Elf 'elf_id' delivers 'elf_id' presents to at most 50 houses.
        last_house_for_elf = elf_id * PART2_MAX_HOUSES_PER_ELF
        house_presents_counts[elf_id : last_house_for_elf + 1 : elf_id] += elf_id

        # House 'elf_id' is now finalized.
        if house_presents_counts[elf_id] >= target_sum_per_house:
            return elf_id
    return None


if __name__ == "__main__":
    print(f"Part 1 First House: {solve_part1(MIN_PRESENTS_GOAL)}")
    print(f"Part 2 First House: {solve_part2(MIN_PRESENTS_GOAL)}")
