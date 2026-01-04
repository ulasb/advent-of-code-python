#!/usr/bin/env python3

import argparse
import unittest
from typing import Set

# Module-level constants for better performance
VOWELS: Set[str] = {'a', 'e', 'i', 'o', 'u'}
PROBLEM_STRINGS: Set[str] = {"ab", "cd", "pq", "xy"}

def string_is_nice_part_2(string_to_test: str) -> bool:
    """
    Check if string is nice according to Part 2 rules:
    - Contains at least one letter that repeats with exactly one letter between them (xyx)
    - Contains at least one pair of letters that appears at least twice without overlapping
    """
    has_repeated_pair = False
    has_letter_with_gap = False

    # Check for letter repeating with one letter gap (e.g., xyx)
    for i in range(2, len(string_to_test)):
        if string_to_test[i] == string_to_test[i-2]:
            has_letter_with_gap = True
            break

    # Check for repeated pairs without overlapping
    for i in range(len(string_to_test) - 1):
        pair = string_to_test[i:i+2]
        # Look for this pair appearing again later, ensuring no overlap
        next_occurrence = string_to_test.find(pair, i + 2)
        if next_occurrence != -1:
            has_repeated_pair = True
            break

    return has_repeated_pair and has_letter_with_gap

def string_is_nice_part_1(string_to_test: str) -> bool:
    """
    Check if string is nice according to Part 1 rules:
    - Contains at least 3 vowels (a, e, i, o, u)
    - Contains at least one letter that appears twice in a row
    - Does not contain any of the forbidden substrings: ab, cd, pq, xy
    """
    if not string_to_test:
        return False

    vowel_count = 0
    has_double_chars = False

    for i, char in enumerate(string_to_test):
        # Count vowels
        if char in VOWELS:
            vowel_count += 1

        # Check for double characters
        if i > 0 and char == string_to_test[i-1]:
            has_double_chars = True

        # Check for forbidden substrings (early exit for efficiency)
        if i > 0 and string_to_test[i-1:i+1] in PROBLEM_STRINGS:
            return False

    return vowel_count >= 3 and has_double_chars


class TestStringIsNicePart1(unittest.TestCase):
    def test_ugknbfddgicrmopn_is_nice(self):
        """Test that ugknbfddgicrmopn is considered nice"""
        self.assertTrue(string_is_nice_part_1("ugknbfddgicrmopn"))

    def test_aaa_is_nice(self):
        """Test that aaa is considered nice"""
        self.assertTrue(string_is_nice_part_1("aaa"))

    def test_jchzalrnumimnmhp_is_not_nice(self):
        """Test that jchzalrnumimnmhp is not considered nice"""
        self.assertFalse(string_is_nice_part_1("jchzalrnumimnmhp"))

    def test_haegwjzuvuyypxyu_is_not_nice(self):
        """Test that haegwjzuvuyypxyu is not considered nice"""
        self.assertFalse(string_is_nice_part_1("haegwjzuvuyypxyu"))

    def test_dvszwmarrgswjxmb_is_not_nice(self):
        """Test that dvszwmarrgswjxmb is not considered nice"""
        self.assertFalse(string_is_nice_part_1("dvszwmarrgswjxmb"))


class TestStringIsNicePart2(unittest.TestCase):
    def test_qjhvhtzxzqqjkmpb_is_nice(self):
        """Test that qjhvhtzxzqqjkmpb is considered nice"""
        self.assertTrue(string_is_nice_part_2("qjhvhtzxzqqjkmpb"))

    def test_xxyxx_is_nice(self):
        """Test that xxyxx is considered nice"""
        self.assertTrue(string_is_nice_part_2("xxyxx"))

    def test_uurcxstgmygtbstg_is_not_nice(self):
        """Test that uurcxstgmygtbstg is not considered nice"""
        self.assertFalse(string_is_nice_part_2("uurcxstgmygtbstg"))

    def test_ieodomkazucvgmuy_is_not_nice(self):
        """Test that ieodomkazucvgmuy is not considered nice"""
        self.assertFalse(string_is_nice_part_2("ieodomkazucvgmuy"))


def main():
    parser = argparse.ArgumentParser(description='Process strings from a file for Advent of Code Day 5')
    parser.add_argument('filename', nargs='?', default='input.txt',
                        help='File to read strings from (default: input.txt)')

    args = parser.parse_args()

    nice_count_part_1 = 0
    nice_count_part_2 = 0

    try:
        with open(args.filename, 'r') as file:
            for line in file:
                # Strip whitespace and newline characters
                cleaned_line = line.strip()
                if cleaned_line:  # Only add non-empty lines
                    if string_is_nice_part_1(cleaned_line):
                        nice_count_part_1 += 1
                    if string_is_nice_part_2(cleaned_line):
                        nice_count_part_2 += 1
        print(f"Part 1 nice string total: {nice_count_part_1}")
        print(f"Part 2 nice string total: {nice_count_part_2}")
    

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1

    return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run the main program
        exit(main())
