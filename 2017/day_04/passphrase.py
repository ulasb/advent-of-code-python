"""
Advent of Code 2017 - Day 4: High-Entropy Passphrases
Created and published by Ulaş Bardak.

This project is licensed under the Mozilla Public License 2.0 (MPL 2.0).
MPL 2.0 is a copyleft license that is easy to understand. It allows for
commercial use, modification, and distribution, but requires that the
source code of any modified files be made available under the same license.
"""

import sys
import unittest
from typing import List


def is_valid_part1(phrase: str) -> bool:
    """
    Check if a passphrase is valid for Part 1.

    A passphrase is valid if it contains no duplicate words.

    Parameters
    ----------
    phrase : str
        The passphrase to check, consisting of words separated by spaces.

    Returns
    -------
    bool
        True if the passphrase is valid, False otherwise.
    """
    words = phrase.split()
    if not words:
        return False
    return len(words) == len(set(words))


def is_valid_part2(phrase: str) -> bool:
    """
    Check if a passphrase is valid for Part 2.

    A passphrase is valid if it contains no words that are anagrams of each other.

    Parameters
    ----------
    phrase : str
        The passphrase to check, consisting of words separated by spaces.

    Returns
    -------
    bool
        True if the passphrase is valid, False otherwise.
    """
    words = phrase.split()
    if not words:
        return False
    # Sort characters in each word to easily detect anagrams
    sorted_words = ["".join(sorted(word)) for word in words]
    return len(sorted_words) == len(set(sorted_words))


def solve_part1(lines: List[str]) -> int:
    """
    Solve Part 1: Count the number of valid passphrases in the input lines.

    Parameters
    ----------
    lines : List[str]
        A list of strings, each representing a passphrase.

    Returns
    -------
    int
        The count of valid passphrases for Part 1.
    """
    count = 0
    for line in lines:
        if line.strip() and is_valid_part1(line.strip()):
            count += 1
    return count


def solve_part2(lines: List[str]) -> int:
    """
    Solve Part 2: Count the number of valid passphrases for Part 2.

    Parameters
    ----------
    lines : List[str]
        A list of strings, each representing a passphrase.

    Returns
    -------
    int
        The count of valid passphrases for Part 2.
    """
    count = 0
    for line in lines:
        if line.strip() and is_valid_part2(line.strip()):
            count += 1
    return count


def main(filename: str = "input.txt") -> int:
    """
    Main entry point for the script.

    Parameters
    ----------
    filename : str, optional
        The path to the input file, by default "input.txt".

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}", file=sys.stderr)
        return 1

    print(f"Part 1: {solve_part1(lines)}")
    print(f"Part 2: {solve_part2(lines)}")
    return 0


class TestPassphrases(unittest.TestCase):
    """
    Unit tests for passphrase validation based on provided examples.
    """

    def test_is_valid_part1(self):
        """Test cases for Part 1 validation."""
        self.assertTrue(is_valid_part1("aa bb cc dd ee"))
        self.assertFalse(is_valid_part1("aa bb cc dd aa"))
        self.assertTrue(is_valid_part1("aa bb cc dd aaa"))

    def test_is_valid_part2(self):
        """Test cases for Part 2 validation."""
        self.assertTrue(is_valid_part2("abcde fghij"))
        self.assertFalse(is_valid_part2("abcde xyz ecdab"))
        self.assertTrue(is_valid_part2("a ab abc abd abf abj"))
        self.assertTrue(is_valid_part2("iiii oiii ooii oooi oooo"))
        self.assertFalse(is_valid_part2("oiii ioii iioi iiio"))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.argv.pop(1)
        unittest.main()
    else:
        file_arg = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
        sys.exit(main(file_arg))
