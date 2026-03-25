#!/usr/bin/env python3
"""
Brief AOC 2015 Day 2 implementation.
Licensed under Mozilla Public License 2.0 by Ulaş Bardak.
"""

import sys
import unittest
from typing import List, Tuple


def solve(filename: str = "input.txt") -> Tuple[int, int]:
    """
    Solve part 1 and 2 for the given input file.

    Parameters
    ----------
    filename : str
        Path to input file.

    Returns
    -------
    Tuple[int, int]
        Total wrapping paper and ribbon needed.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            presents = [sorted(map(int, l.strip().split("x"))) for l in f if "x" in l]
    except FileNotFoundError:
        return 0, 0

    paper = sum(3 * a * b + 2 * a * c + 2 * b * c for a, b, c in presents)
    ribbon = sum(2 * (a + b) + a * b * c for a, b, c in presents)
    return paper, ribbon


class TestAoC(unittest.TestCase):
    """Test cases for the succinct solution."""

    def test_examples(self):
        """Test with provided examples."""
        import io
        from unittest.mock import patch
        with patch("builtins.open", return_value=io.StringIO("2x3x4\n1x1x10\n")):
            p1, p2 = solve("dummy.txt")
        self.assertEqual((p1, p2), (101, 48))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
        ans1, ans2 = solve(file)
        print(f"Total wrapping paper: {ans1}")
        print(f"Total ribbon length: {ans2}")
