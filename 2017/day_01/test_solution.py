"""
Unit tests for Advent of Code 2017 Day 1 solution.
"""

import unittest
from solution import solve_part1, solve_part2


class TestInverseCaptcha(unittest.TestCase):
    """Test cases for the Inverse Captcha solution."""

    def test_part1_cases(self):
        """Test the Part 1 examples provided in the plan."""
        self.assertEqual(solve_part1([1, 1, 2, 2]), 3)
        self.assertEqual(solve_part1([1, 1, 1, 1]), 4)
        self.assertEqual(solve_part1([1, 2, 3, 4]), 0)
        self.assertEqual(solve_part1([9, 1, 2, 1, 2, 1, 2, 9]), 9)

    def test_part2_cases(self):
        """Test the Part 2 examples provided in the plan."""
        self.assertEqual(solve_part2([1, 2, 1, 2]), 6)
        self.assertEqual(solve_part2([1, 2, 2, 1]), 0)
        self.assertEqual(solve_part2([1, 2, 3, 4, 2, 5]), 4)
        self.assertEqual(solve_part2([1, 2, 3, 1, 2, 3]), 12)
        self.assertEqual(solve_part2([1, 2, 1, 3, 1, 4, 1, 5]), 4)


if __name__ == "__main__":
    unittest.main()
