import unittest
from vault import find_shortest_path

class TestVault(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(find_shortest_path("ihgpwlah"), "DDRRRD")

    def test_case_2(self):
        self.assertEqual(find_shortest_path("kglvqrro"), "DDUDRLRRUDRD")

    def test_case_3(self):
        self.assertEqual(find_shortest_path("ulqzkmiv"), "DRURDRUDDLLDLUURRDULRLDUUDDDRR")

if __name__ == "__main__":
    unittest.main()
