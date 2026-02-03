import unittest
from checksum import generate, checksum, calculate_disk_checksum


class TestChecksum(unittest.TestCase):
    """
    Unit tests for the dragon curve and checksum logic.
    """

    def test_dragon_curve(self) -> None:
        """
        Test the modified dragon curve generation.

        Suppose you want to fill a disk of length 20 using an initial state of 10000:
        Because 10000 is too short, we first use the modified dragon curve to make it longer.
        After one round, it becomes 10000011110 (11 characters), still too short.
        After two rounds, it becomes 10000011110010000111110 (23 characters), which is enough.
        """
        initial_state = "10000"

        # Round 1
        round1 = generate(initial_state)
        self.assertEqual(round1, "10000011110")
        self.assertEqual(len(round1), 11)

        # Round 2
        round2 = generate(round1)
        self.assertEqual(round2, "10000011110010000111110")
        self.assertEqual(len(round2), 23)

    def test_truncation(self: unittest.TestCase) -> None:
        """
        Test the truncation of the generated data to the disk size.

        Since we only need 20, but we have 23, we get rid of all but the first 20 characters:
        10000011110010000111.
        """
        data = "10000011110010000111110"
        truncated = data[:20]
        self.assertEqual(truncated, "10000011110010000111")
        self.assertEqual(len(truncated), 20)

    def test_checksum_rounds(self: unittest.TestCase) -> None:
        """
        Test the iterative checksum calculation steps.

        Next, we start calculating the checksum; after one round, we have 0111110101,
        which 10 characters long (even), so we continue.
        After two rounds, we have 01100, which is 5 characters long (odd), so we are done.
        """
        data = "10000011110010000111"

        # Round 1
        cs1 = checksum(data)
        self.assertEqual(cs1, "0111110101")
        self.assertEqual(len(cs1), 10)

        # Round 2
        cs2 = checksum(cs1)
        self.assertEqual(cs2, "01100")
        self.assertEqual(len(cs2), 5)

    def test_full_process(self: unittest.TestCase) -> None:
        """
        Test the end-to-end checksum calculation process.
        """
        result = calculate_disk_checksum("10000", 20)
        self.assertEqual(result, "01100")


if __name__ == "__main__":
    unittest.main()
