#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 8: Matchsticks

This module solves the "Matchsticks" puzzle from Advent of Code 2015 Day 8.
The puzzle involves calculating differences between string representations:
- Part 1: Difference between code characters and in-memory characters
- Part 2: Difference between encoded characters and code characters
"""

import argparse
import sys
from typing import Tuple
import unittest


def calculate_memory_length(string_literal: str) -> int:
    """
    Calculate the actual length of a string when stored in memory,
    accounting for escape sequences.

    Args:
        string_literal: The string literal including surrounding quotes

    Returns:
        The number of characters in memory

    Raises:
        ValueError: If the string literal is malformed
    """
    if len(string_literal) < 2 or not (string_literal.startswith('"') and string_literal.endswith('"')):
        raise ValueError(f"Invalid string literal format: {string_literal!r}")

    # Remove surrounding quotes and process escape sequences
    content = string_literal[1:-1]
    memory_chars = 0
    i = 0

    while i < len(content):
        if content[i] == '\\':
            if i + 1 >= len(content):
                raise ValueError(f"Incomplete escape sequence at position {i}")

            escape_char = content[i + 1]
            if escape_char == '\\' or escape_char == '"':
                # Simple escapes: \\ and \"
                memory_chars += 1
                i += 2
            elif escape_char == 'x':
                # Hex escape: \xHH
                if i + 3 >= len(content):
                    raise ValueError(f"Incomplete hex escape sequence at position {i}")
                try:
                    # Validate that it's valid hex, but count as 1 character
                    int(content[i + 2:i + 4], 16)
                    memory_chars += 1
                    i += 4
                except ValueError:
                    raise ValueError(f"Invalid hex escape sequence: {content[i:i+4]!r}")
            else:
                raise ValueError(f"Unknown escape sequence: \\{escape_char}")
        else:
            memory_chars += 1
            i += 1

    return memory_chars


def calculate_encoded_length(string_literal: str) -> int:
    """
    Calculate the length of the string when encoded with escape sequences.

    When encoding a string, we need to:
    - Add surrounding quotes
    - Escape all backslashes and quotes with backslashes

    Args:
        string_literal: The original string literal (with quotes)

    Returns:
        The number of characters needed to encode this string
    """
    # Start with 2 for the surrounding quotes we'll add
    encoded_length = 2

    for char in string_literal:
        if char in ('"', '\\'):
            # These characters need to be escaped, so they become 2 characters each
            encoded_length += 2
        else:
            encoded_length += 1

    return encoded_length


def process_line(line: str) -> Tuple[int, int, int]:
    """
    Process a single line from the input file.

    Args:
        line: The line to process (may include newline character)

    Returns:
        A tuple of (code_length, memory_length, encoded_length):
        - code_length: Number of characters in the source code representation
        - memory_length: Number of characters when stored in memory
        - encoded_length: Number of characters needed to encode the string

    Raises:
        ValueError: If the line contains an invalid string literal
    """
    # Remove whitespace including newlines
    string_literal = line.strip()

    if not string_literal:
        raise ValueError("Empty line encountered")

    # Code length is simply the length of the string as written
    code_length = len(string_literal)

    # Memory length accounts for escape sequences
    memory_length = calculate_memory_length(string_literal)

    # Encoded length is how many characters it takes to represent this string with escapes
    encoded_length = calculate_encoded_length(string_literal)

    return code_length, memory_length, encoded_length


def main() -> None:
    """
    Main function to read input file and solve both parts of Day 8.

    Part 1: Find the difference between code representation and memory representation
    Part 2: Find the difference between encoded representation and code representation
    """
    parser = argparse.ArgumentParser(
        description='Advent of Code 2015 - Day 8: Matchsticks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Process input.txt
  %(prog)s my_input.txt       # Process custom file
  %(prog)s test               # Run unit tests
        """
    )
    parser.add_argument(
        'filename',
        nargs='?',
        default='input.txt',
        help='Input file to process (default: input.txt)'
    )

    args = parser.parse_args()

    # Initialize counters for both parts
    total_code_characters = 0
    total_memory_characters = 0
    total_encoded_characters = 0

    try:
        with open(args.filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.rstrip('\n\r')  # Remove line endings but preserve spaces
                if not line:  # Skip empty lines
                    continue

                try:
                    code_len, mem_len, enc_len = process_line(line)
                    total_code_characters += code_len
                    total_memory_characters += mem_len
                    total_encoded_characters += enc_len
                except ValueError as e:
                    print(f"Error processing line {line_number}: {e}", file=sys.stderr)
                    print(f"Line content: {line!r}", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"Unexpected error processing line {line_number}: {e}", file=sys.stderr)
                    sys.exit(1)

        # Part 1: Difference between code representation and memory representation
        part1_answer = total_code_characters - total_memory_characters

        # Part 2: Difference between encoded representation and code representation
        part2_answer = total_encoded_characters - total_code_characters

        print(f"Part 1: {part1_answer}")
        print(f"Part 2: {part2_answer}")
        print(f"Total lines processed: {line_number}")

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{args.filename}': {e}", file=sys.stderr)
        sys.exit(1)


class TestDay8(unittest.TestCase):
    """Unit tests for Advent of Code 2015 Day 8"""

    def test_memory_length_examples(self):
        """Test memory length calculations from problem examples"""
        # "" is 2 characters of code (the two double quotes), but the string contains zero characters
        self.assertEqual(len('""'), 2)
        self.assertEqual(calculate_memory_length('""'), 0)

        # "abc" is 5 characters of code, but 3 characters in the string data
        self.assertEqual(len('"abc"'), 5)
        self.assertEqual(calculate_memory_length('"abc"'), 3)

        # "aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote character, for a total of 7 characters in the string data
        self.assertEqual(len('"aaa\\"aaa"'), 10)
        self.assertEqual(calculate_memory_length('"aaa\\"aaa"'), 7)

        # "\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal notation
        self.assertEqual(len('"\\x27"'), 6)
        self.assertEqual(calculate_memory_length('"\\x27"'), 1)

    def test_encoded_length_examples(self):
        """Test encoded length calculations from problem examples"""
        # "" encodes to "\"\"", an increase from 2 characters to 6
        self.assertEqual(len('""'), 2)
        self.assertEqual(calculate_encoded_length('""'), 6)

        # "abc" encodes to "\"abc\"", an increase from 5 characters to 9
        self.assertEqual(len('"abc"'), 5)
        self.assertEqual(calculate_encoded_length('"abc"'), 9)

        # "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to 16
        self.assertEqual(len('"aaa\\"aaa"'), 10)
        self.assertEqual(calculate_encoded_length('"aaa\\"aaa"'), 16)

        # "\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11
        self.assertEqual(len('"\\x27"'), 6)
        self.assertEqual(calculate_encoded_length('"\\x27"'), 11)

    def test_process_line_examples(self):
        """Test process_line function with examples"""
        # Test the complete processing for each example
        code_len, mem_len, enc_len = process_line('""')
        self.assertEqual(code_len, 2)
        self.assertEqual(mem_len, 0)
        self.assertEqual(enc_len, 6)

        code_len, mem_len, enc_len = process_line('"abc"')
        self.assertEqual(code_len, 5)
        self.assertEqual(mem_len, 3)
        self.assertEqual(enc_len, 9)

        code_len, mem_len, enc_len = process_line('"aaa\\"aaa"')
        self.assertEqual(code_len, 10)
        self.assertEqual(mem_len, 7)
        self.assertEqual(enc_len, 16)

        code_len, mem_len, enc_len = process_line('"\\x27"')
        self.assertEqual(code_len, 6)
        self.assertEqual(mem_len, 1)
        self.assertEqual(enc_len, 11)

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        # Empty string
        self.assertEqual(calculate_memory_length('""'), 0)
        self.assertEqual(calculate_encoded_length('""'), 6)

        # String with only escaped quote
        self.assertEqual(calculate_memory_length('"\\""'), 1)  # One quote character
        self.assertEqual(calculate_encoded_length('"\\""'), 10)  # Both \ and " need escaping

        # String with only escaped backslash
        self.assertEqual(calculate_memory_length('"\\\\"'), 1)  # One backslash character
        self.assertEqual(calculate_encoded_length('"\\\\"'), 10)  # Both \ characters need escaping

        # Mixed escapes: backslash + escaped quote
        self.assertEqual(calculate_memory_length('"\\\\\\""'), 2)  # backslash + quote

    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        # Missing closing quote
        with self.assertRaises(ValueError):
            calculate_memory_length('"hello')

        # Missing opening quote
        with self.assertRaises(ValueError):
            calculate_memory_length('hello"')

        # Empty input
        with self.assertRaises(ValueError):
            calculate_memory_length('')

        # Incomplete hex escape
        with self.assertRaises(ValueError):
            calculate_memory_length('"\\x"')

        # Invalid hex digits
        with self.assertRaises(ValueError):
            calculate_memory_length('"\\xGG"')

        # Unknown escape sequence
        with self.assertRaises(ValueError):
            calculate_memory_length('"\\z"')

        # Empty line in process_line
        with self.assertRaises(ValueError):
            process_line('')


def run_tests() -> None:
    """Run the unit tests for this module."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    # Check for test command
    if len(sys.argv) > 1 and sys.argv[1] in ('test', '--test', '-t'):
        run_tests()
    else:
        main()
