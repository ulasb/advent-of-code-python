import unittest
from spiral import find_distance, find_first_larger

class TestSpiral(unittest.TestCase):
    def test_part1_distance(self):
        """Test Manhattan distance for various goal values."""
        self.assertEqual(find_distance(1), 0)
        self.assertEqual(find_distance(12), 3)
        self.assertEqual(find_distance(23), 2)
        self.assertEqual(find_distance(1024), 31)

    def test_part2_first_larger(self):
        """Test finding the first value larger than goal."""
        # 1, 1, 2, 4, 5, 10, 11, 23, 25, 26, 54, 57, 59, 122, 133, 142, 147, 304, 330, 351, 362, 747, 806
        self.assertEqual(find_first_larger(1), 2)
        self.assertEqual(find_first_larger(2), 4)
        self.assertEqual(find_first_larger(4), 5)
        self.assertEqual(find_first_larger(5), 10)
        self.assertEqual(find_first_larger(10), 11)
        self.assertEqual(find_first_larger(11), 23)
        self.assertEqual(find_first_larger(23), 25)
        self.assertEqual(find_first_larger(25), 26)
        self.assertEqual(find_first_larger(747), 806)

if __name__ == '__main__':
    unittest.main()
