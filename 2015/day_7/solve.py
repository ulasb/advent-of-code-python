#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 7: Some Assembly Required

This script simulates a digital circuit with bitwise operations.
It reads circuit definitions from a file and computes signal values on wires.
"""

import argparse
import sys
from typing import Dict
import unittest

# Constants
UINT16_MASK = 0xFFFF  # 16-bit unsigned integer mask


def resolve_wire(wires: Dict[str, str], value: str, memo: Dict[str, int] = None) -> int:
    """
    Recursively resolve the value of a wire in the circuit.

    Args:
        wires: Dictionary mapping wire names to their expressions
        value: The expression or wire name to resolve
        memo: Memoization cache for computed values

    Returns:
        The 16-bit unsigned integer value of the wire/expression
    """
    if memo is None:
        memo = {}

    # Check memo first
    if value in memo:
        return memo[value]

    # Handle direct numeric values
    if value.isdigit():
        result = int(value)
    else:
        # Parse the expression
        parts = value.split()

        if len(parts) == 1:
            # Direct wire reference - resolve recursively
            result = resolve_wire(wires, wires[parts[0]], memo)
        elif len(parts) == 2:
            # NOT operation (unary)
            if parts[0] != "NOT":
                raise ValueError(f"Invalid unary operation: {value}")
            operand = resolve_wire(wires, parts[1], memo)
            result = (~operand) & UINT16_MASK
        elif len(parts) == 3:
            # Binary operations
            left_operand = resolve_wire(wires, parts[0], memo)
            operation = parts[1]

            if operation in ("AND", "OR"):
                right_operand = resolve_wire(wires, parts[2], memo)
                if operation == "AND":
                    result = (left_operand & right_operand) & UINT16_MASK
                else:  # OR
                    result = (left_operand | right_operand) & UINT16_MASK
            elif operation in ("LSHIFT", "RSHIFT"):
                # Shift amount is always a literal number
                shift_amount = int(parts[2])
                if operation == "LSHIFT":
                    result = (left_operand << shift_amount) & UINT16_MASK
                else:  # RSHIFT
                    result = (left_operand >> shift_amount) & UINT16_MASK
            else:
                raise ValueError(f"Unknown operation: {operation}")
        else:
            raise ValueError(f"Invalid expression format: {value}")

    # Cache and return result
    memo[value] = result
    return result


class TestAdventOfCodeDay7(unittest.TestCase):
    """Test cases for Advent of Code 2015 Day 7"""

    def test_sample_circuit(self):
        """Test the sample circuit with expected wire values"""
        # Sample input circuit
        test_input = [
            "123 -> x",
            "456 -> y",
            "x AND y -> d",
            "x OR y -> e",
            "x LSHIFT 2 -> f",
            "y RSHIFT 2 -> g",
            "NOT x -> h",
            "NOT y -> i"
        ]

        # Expected results
        expected_values = {
            'd': 72,
            'e': 507,
            'f': 492,
            'g': 114,
            'h': 65412,
            'i': 65079,
            'x': 123,
            'y': 456
        }

        # Build wires dictionary
        wires = {}
        for line in test_input:
            parts = line.strip().split(" -> ")
            wires[parts[1]] = parts[0]

        # Test each wire
        for wire_name, expected_value in expected_values.items():
            with self.subTest(wire=wire_name):
                actual_value = resolve_wire(wires, wire_name)
                self.assertEqual(actual_value, expected_value,
                               f"Wire {wire_name} should be {expected_value}, got {actual_value}")

    def test_direct_number(self):
        """Test direct number assignment"""
        wires = {'a': '123'}
        self.assertEqual(resolve_wire(wires, 'a'), 123)

    def test_direct_wire_reference(self):
        """Test direct wire to wire connection"""
        wires = {'a': '123', 'b': 'a'}
        self.assertEqual(resolve_wire(wires, 'b'), 123)

    def test_not_operation(self):
        """Test NOT operation"""
        wires = {'a': '123', 'b': 'NOT a'}
        self.assertEqual(resolve_wire(wires, 'b'), 65412)  # ~123 & 0xFFFF

    def test_and_operation(self):
        """Test AND operation"""
        wires = {'a': '123', 'b': '456', 'c': 'a AND b'}
        self.assertEqual(resolve_wire(wires, 'c'), 72)  # 123 & 456

    def test_or_operation(self):
        """Test OR operation"""
        wires = {'a': '123', 'b': '456', 'c': 'a OR b'}
        self.assertEqual(resolve_wire(wires, 'c'), 507)  # 123 | 456

    def test_lshift_operation(self):
        """Test LSHIFT operation"""
        wires = {'a': '123', 'b': 'a LSHIFT 2'}
        self.assertEqual(resolve_wire(wires, 'b'), 492)  # 123 << 2

    def test_rshift_operation(self):
        """Test RSHIFT operation"""
        wires = {'a': '456', 'b': 'a RSHIFT 2'}
        self.assertEqual(resolve_wire(wires, 'b'), 114)  # 456 >> 2

    def test_complex_expression(self):
        """Test a more complex expression"""
        wires = {
            'x': '123',
            'y': 'NOT x',
            'z': 'y AND 255'
        }
        # NOT 123 = 65412, 65412 & 255 = 132
        self.assertEqual(resolve_wire(wires, 'z'), 132)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Advent of Code 2015 - Day 7: Some Assembly Required')
    parser.add_argument('input_file', nargs='?', default='input.txt',
                        help='Input file to process (default: input.txt)')
    parser.add_argument('--test', action='store_true',
                        help='Run unit tests instead of processing input file')

    # Parse arguments
    args = parser.parse_args()

    if args.test:
        # Run tests
        unittest.main(argv=[''], exit=False, verbosity=2)
        return

    wires = {}

    try:
        # Open and read the input file
        with open(args.input_file, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove trailing whitespace (including newline)
                line = line.strip().split(" -> ")
                wires[line[1]] = line[0]

            # Part A
            if "a" in wires:
                value_a = resolve_wire(wires, "a")
                print(f"Part A - Signal on wire a: {value_a}")
            else:
                print("Error: Wire 'a' not found in input", file=sys.stderr)
                sys.exit(1)

            # Part B - Override wire 'b' with the value from Part A
            wires_copy = wires.copy()
            wires_copy["b"] = str(value_a)
            value_a_part2 = resolve_wire(wires_copy, "a")
            print(f"Part B - Signal on wire a: {value_a_part2}")
            


    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
