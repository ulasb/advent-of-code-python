#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 23: Opening the Turing Lock

This script implements a simple virtual machine to process a list of instructions.
The code was created and published by Ulaş Bardak and is licensed under the
Mozilla Public License 2.0. The MPL 2.0 is a weak copyleft license that allows
for the modification and distribution of the code, but requires that any changes
to the code be made available under the same license.
"""

import argparse
import logging
import os
import sys
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "input.txt"


def read_instructions(filename: str = DEFAULT_INPUT_FILE) -> List[str]:
    """
    Read a list of instructions from a file.

    Parameters
    ----------
    filename : str, optional
        The path to the input file (default is "input.txt").

    Returns
    -------
    List[str]
        A list of instructions as strings.

    Raises
    ------
    FileNotFoundError
        If the input file doesn't exist.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Input file '{filename}' not found.")

    instructions = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line)
    return instructions


def execute(instructions: List[str], registers: Dict[str, int]) -> None:
    """
    Execute a list of instructions using the provided registers.

    The virtual machine supports the following instructions:
    - hlf r: sets register r to half its current value.
    - tpl r: sets register r to triple its current value.
    - inc r: increments register r by 1.
    - jmp offset: jump relative to current position.
    - jie r, offset: jump if r is even.
    - jio r, offset: jump if r is exactly 1.

    Parameters
    ----------
    instructions : List[str]
        The list of instructions to execute.
    registers : Dict[str, int]
        A dictionary mapping register names to integers.
        This dictionary is modified in-place.
    """
    pc = 0  # Program counter
    n = len(instructions)

    while 0 <= pc < n:
        line = instructions[pc]
        # Split by space and remove commas
        parts = line.replace(",", "").split()
        if not parts:
            pc += 1
            continue

        op = parts[0]

        try:
            pc_increment = 1
            if op == "hlf":
                registers[parts[1]] //= 2
            elif op == "tpl":
                registers[parts[1]] *= 3
            elif op == "inc":
                registers[parts[1]] += 1
            elif op == "jmp":
                pc_increment = int(parts[1])
            elif op == "jie":
                if registers[parts[1]] % 2 == 0:
                    pc_increment = int(parts[2])
            elif op == "jio":
                if registers[parts[1]] == 1:
                    pc_increment = int(parts[2])
            else:
                logger.warning(f"Unknown instruction at line {pc}: {line}")
                break

            pc += pc_increment
        except (IndexError, ValueError, KeyError) as e:
            logger.error(f"Error parsing instruction at line {pc} ('{line}'): {e}")
            break


def parse_arguments():
    """
    Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Advent of Code 2015 Day 23 Solver")
    parser.add_argument(
        "file",
        nargs="?",
        default=DEFAULT_INPUT_FILE,
        help="Path to the input file (default: input.txt)",
    )
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_arguments()

    try:
        instructions = read_instructions(args.file)
    except FileNotFoundError as e:
        logger.error(e)
        return

    # Part 1: Register a and b both start at 0
    regs_part1 = {"a": 0, "b": 0}
    execute(instructions, regs_part1)
    logger.info("Part 1 Results:")
    logger.info(f"Register a: {regs_part1['a']}")
    logger.info(f"Register b: {regs_part1['b']}")

    # Part 2: Register a starts at 1, b starts at 0
    regs_part2 = {"a": 1, "b": 0}
    execute(instructions, regs_part2)
    logger.info("Part 2 Results:")
    logger.info(f"Register a: {regs_part2['a']}")
    logger.info(f"Register b: {regs_part2['b']}")


if __name__ == "__main__":
    main()
