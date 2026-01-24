"""
Unit tests for Day 9: Explosives in Cyberspace.
"""

import unittest
from decompress import get_decompressed_length_v1, get_decompressed_length_v2


class TestDecompression(unittest.TestCase):
    """Test cases for compressed data decompression lengths."""

    def test_part1_examples(self) -> None:
        """Test Part 1 decompression rules with provided examples."""
        self.assertEqual(get_decompressed_length_v1("ADVENT"), 6)
        self.assertEqual(get_decompressed_length_v1("A(1x5)BC"), 7)
        self.assertEqual(get_decompressed_length_v1("(3x3)XYZ"), 9)
        self.assertEqual(get_decompressed_length_v1("A(2x2)BCD(2x2)EFG"), 11)
        self.assertEqual(get_decompressed_length_v1("(6x1)(1x3)A"), 6)
        self.assertEqual(get_decompressed_length_v1("X(8x2)(3x3)ABCY"), 18)

    def test_part2_examples(self) -> None:
        """Test Part 2 decompression rules with provided examples."""
        self.assertEqual(get_decompressed_length_v2("(3x3)XYZ"), 9)
        self.assertEqual(get_decompressed_length_v2("X(8x2)(3x3)ABCY"), 20)
        self.assertEqual(
            get_decompressed_length_v2("(27x12)(20x12)(13x14)(7x10)(1x12)A"), 241920
        )
        self.assertEqual(
            get_decompressed_length_v2(
                "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
            ),
            445,
        )


if __name__ == "__main__":
    unittest.main()
