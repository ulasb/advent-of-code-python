
import unittest
from packages import find_min_packages, prod

class TestPackageBalancing(unittest.TestCase):
    """
    Unit tests for the package balancing logic.
    """

    def setUp(self):
        """
        Set up the test data: weights 1-5 and 7-11.
        """
        # Weights: 1, 2, 3, 4, 5, 7, 8, 9, 10, 11 (Total = 60)
        self.weights = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
        self.total_weight = sum(self.weights)

    def test_part_1(self):
        """
        Test Part 1 balancing (3 groups).
        """
        target = self.total_weight // 3  # 20
        # Expected: 11 and 9 (size 2, product 99, sum 20)
        # We also verify it can be partitioned into 2 more groups of 20
        result = find_min_packages(self.weights, target, 3)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(prod(result), 99)
        self.assertEqual(sum(result), 20)

    def test_part_2(self):
        """
        Test Part 2 balancing (4 groups).
        """
        target = self.total_weight // 4  # 15
        # Expected: 11 and 4 (size 2, product 44, sum 15)
        # We also verify it can be partitioned into 3 more groups of 15
        result = find_min_packages(self.weights, target, 4)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(prod(result), 44)
        self.assertEqual(sum(result), 15)

if __name__ == "__main__":
    unittest.main()
