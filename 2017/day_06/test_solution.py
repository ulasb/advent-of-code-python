"""
Unit tests for Advent of Code 2017, Day 6 solution.

Created and published by Ulaş Bardak.
License: Mozilla Public License 2.0 (MPL 2.0).
"""

import unittest
from solution import redistribute, solve


class TestMemoryReallocation(unittest.TestCase):
    """Test cases for the memory reallocation routine."""

    def test_redistribute(self):
        """Test a single redistribution step."""
        banks = [0, 2, 7, 0]
        # Step 1: Max is 7 at index 2
        banks = redistribute(banks)
        self.assertEqual(banks, [2, 4, 1, 2])

        # Step 2: Max is 4 at index 1
        banks = redistribute(banks)
        self.assertEqual(banks, [3, 1, 2, 3])

        # Step 3: Max is 3 at index 0 (tie with index 3)
        banks = redistribute(banks)
        self.assertEqual(banks, [0, 2, 3, 4])

        # Step 4: Max is 4 at index 3
        banks = redistribute(banks)
        self.assertEqual(banks, [1, 3, 4, 1])

        # Step 5: Max is 4 at index 2
        banks = redistribute(banks)
        self.assertEqual(banks, [2, 4, 1, 2])

    def test_solve(self):
        """Test the full solve logic with the example case."""
        initial_banks = [0, 2, 7, 0]
        cycles, loop_size = solve(initial_banks)
        self.assertEqual(cycles, 5)
        self.assertEqual(loop_size, 4)


if __name__ == "__main__":
    unittest.main()
