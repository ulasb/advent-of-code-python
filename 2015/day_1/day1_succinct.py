"""Advent of Code 2015 Day 1 - Succinct Parentheses Parser."""

import sys
import unittest
from itertools import accumulate


def solve(data: str) -> tuple[int, int]:
    """
    Solve Day 1 puzzle for both parts efficiently.

    Parameters
    ----------
    data : str
        The input string of parentheses.

    Returns
    -------
    tuple[int, int]
        Final floor (Part 1) and first basement entry index (Part 2).
    """
    moves = [1 if c == "(" else -1 for c in data if c in "()"]
    return sum(moves), next((i for i, v in enumerate(accumulate(moves), 1) if v == -1), -1)


class TestDay1Succinct(unittest.TestCase):
    """Verify succinct logic against puzzle examples."""

    def test_solve(self) -> None:
        """Run all test cases from the problem description."""
        cases = [
            ("(())", 0, -1),
            ("(((", 3, -1),
            ("))(((((", 3, 1),
            ("())", -1, 3),
            (")", -1, 1),
            ("()())", -1, 5),
        ]
        for s, p1, p2 in cases:
            with self.subTest(s=s):
                self.assertEqual(solve(s), (p1, p2))


if __name__ == "__main__":
    if len(sys.argv) == 1 and sys.stdin.isatty():
        unittest.main()
    else:
        file_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                p1, p2 = solve(f.read().strip())
                print(f"Final floor: {p1}\nFirst basement entry: {p2}")
        except FileNotFoundError:
            print(f"Error: {file_path} not found.", file=sys.stderr)
            sys.exit(1)
