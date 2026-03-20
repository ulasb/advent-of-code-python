"""
Advent of Code 2017 - Day 8: I Heard You Like Registers
Created by Ulaş Bardak. Licensed under Mozilla Public License 2.0.
MPL 2.0 is a copyleft license that allows for commercial use, modification, and distribution,
but requires that source code changes be made available under the same license.
"""

import sys
from collections import defaultdict
from typing import Dict, Tuple, Callable


def solve_instructions(input_data: str) -> Tuple[int, int]:
    """
    Simulate a series of register instructions.

    Parameters
    ----------
    input_data : str
        The raw instruction data from the input.

    Returns
    -------
    Tuple[int, int]
        - Part 1: The largest value in any register after all instructions.
        - Part 2: The largest value held in any register during any part of the process.

    Notes
    -----
    Registers all start at 0.
    """
    registers: Dict[str, int] = defaultdict(int)
    max_ever = 0

    # Operators for condition check
    ops: Dict[str, Callable[[int, int], bool]] = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
    }

    for line in input_data.strip().split("\n"):
        if not line:
            continue

        # Format: b inc 5 if a > 1
        parts = line.split()
        if len(parts) < 7:
            continue

        target_reg = parts[0]
        operation = parts[1]
        amount = int(parts[2])
        # "if" is parts[3]
        cond_reg = parts[4]
        cond_op = parts[5]
        cond_val = int(parts[6])

        # Evaluate condition
        if ops[cond_op](registers[cond_reg], cond_val):
            # Apply operation
            if operation == "inc":
                registers[target_reg] += amount
            elif operation == "dec":
                registers[target_reg] -= amount

            # Update max ever (only if a register changes)
            if registers[target_reg] > max_ever:
                max_ever = registers[target_reg]

    part1_max = max(registers.values()) if registers else 0
    return part1_max, max_ever


def main(file_path: str = "input.txt"):
    """
    Read input file and print solutions for Part 1 and Part 2.

    Parameters
    ----------
    file_path : str
        Path to the input text file. Default is 'input.txt'.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            input_data = f.read()

        p1, p2 = solve_instructions(input_data)
        print(f"Part 1: {p1}")
        print(f"Part 2: {p2}")

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    main(path)
