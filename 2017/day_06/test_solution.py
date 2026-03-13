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
        """Test multiple redistribution steps."""
        steps = [
            # initial state, expected state
            ([0, 2, 7, 0], [2, 4, 1, 2]),  # Step 1: Max is 7 at index 2
            ([2, 4, 1, 2], [3, 1, 2, 3]),  # Step 2: Max is 4 at index 1
            ([3, 1, 2, 3], [0, 2, 3, 4]),  # Step 3: Max is 3 at index 0 (tie with index 3)
            ([0, 2, 3, 4], [1, 3, 4, 1]),  # Step 4: Max is 4 at index 3
            ([1, 3, 4, 1], [2, 4, 1, 2]),  # Step 5: Max is 4 at index 2
        ]
        for i, (initial, expected) in enumerate(steps):
            with self.subTest(step=i + 1):
                self.assertEqual(redistribute(initial), expected)

    def test_solve(self):
        """Test the full solve logic with the example case."""
        initial_banks = [0, 2, 7, 0]
        cycles, loop_size = solve(initial_banks)
        self.assertEqual(cycles, 5)
        self.assertEqual(loop_size, 4)


if __name__ == "__main__":
    unittest.main()
