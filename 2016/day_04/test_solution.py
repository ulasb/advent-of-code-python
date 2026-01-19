# Created and published by Ulaş Bardak.
# This code is licensed under the Mozilla Public License 2.0 (MPL-2.0).
# The MPL 2.0 is a "weak" copyleft license that allows you to use this
# code in your own projects, while requiring that any modifications to
# the licensed files be shared under the same license terms.

import unittest
from solution import validate


class TestDay04(unittest.TestCase):
    """
    Unit tests for Advent of Code 2016, Day 4.
    """

    def test_valid_rooms(self):
        """
        Tests rooms that are expected to be valid.
        """
        # Now returns (sector_id, name)
        self.assertEqual(validate("aaaaa-bbb-z-y-x-123[abxyz]"), (123, "aaaaabbbzyx"))
        self.assertEqual(validate("a-b-c-d-e-f-g-h-987[abcde]"), (987, "abcdefgh"))
        self.assertEqual(validate("not-a-real-room-404[oarel]"), (404, "notarealroom"))

    def test_invalid_rooms(self):
        """
        Tests rooms that are expected to be invalid.
        """
        self.assertEqual(validate("totally-real-room-200[decoy]"), (0, ""))


if __name__ == "__main__":
    unittest.main()
