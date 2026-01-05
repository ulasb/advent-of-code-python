"""
Advent of Code 2015 - Day 11: Corporate Policy

This script solves the password generation problem where we need to find the next
valid password according to Santa's corporate policy rules.
"""

import sys
import unittest


CURRENT_PWD = "cqjxjnds"

def increment_pwd(pwd: str) -> str:
    """
    Increment a password string like a base-26 number (a=0, b=1, ..., z=25).
    Returns the next password in lexicographical order.
    """
    chars = list(pwd)

    # Start from the rightmost character and increment
    for i in range(len(chars) - 1, -1, -1):
        if chars[i] < 'z':
            chars[i] = chr(ord(chars[i]) + 1)
            # Reset all characters to the right to 'a'
            for j in range(i + 1, len(chars)):
                chars[j] = 'a'
            break
        else:
            chars[i] = 'a'
    else:
        # If all characters were 'z', add a new 'a' at the beginning
        chars.insert(0, 'a')

    return ''.join(chars)


def find_next_valid_password(start_pwd: str) -> str:
    """
    Find the next valid password after the given starting password.
    Increments the password until a valid one is found.
    """
    pwd = increment_pwd(start_pwd)
    while not is_valid_pwd(pwd):
        pwd = increment_pwd(pwd)
    return pwd

def is_valid_pwd(pwd: str) -> bool:
    """
    Check if a password meets all the criteria for Advent of Code 2015 Day 11:
    1. Contains at least one increasing straight of three letters (abc, bcd, etc.)
    2. Does not contain the letters i, o, or l
    3. Contains at least two different, non-overlapping pairs of identical letters
    """
    # 2: Passwords may not contain the letters i, o, or l (check this first as it's fast)
    forbidden = {'i', 'o', 'l'}
    if any(char in forbidden for char in pwd):
        return False

    # 1: Passwords must include one increasing straight of at least three letters
    has_inc_seq = any(
        ord(pwd[i+1]) - ord(pwd[i]) == 1 and ord(pwd[i+2]) - ord(pwd[i+1]) == 1
        for i in range(len(pwd) - 2)
    )
    if not has_inc_seq:
        return False
    
    # 3: Passwords must contain at least two different, non-overlapping pairs of letters
    pairs = set()
    i = 0
    while i < len(pwd) - 1:
        if pwd[i] == pwd[i + 1]:
            pairs.add(pwd[i])
            i += 2  # Skip the next character since pairs don't overlap
        else:
            i += 1

    if len(pairs) < 2:
        return False

    return True

def main():
    """Main function for Advent of Code 2015 Day 11 solution."""
    # Part 1: Find the next valid password after CURRENT_PWD
    part1_pwd = find_next_valid_password(CURRENT_PWD)
    print(f"Part 1: {part1_pwd}")

    # Part 2: Find the next valid password after part1_pwd
    part2_pwd = find_next_valid_password(part1_pwd)
    print(f"Part 2: {part2_pwd}")


class TestSantaPassword(unittest.TestCase):
    """Unit tests for Advent of Code 2015 Day 11 password functions."""

    def test_hijklmmn_invalid(self):
        """hijklmmn meets first requirement but fails second (contains i and l)."""
        self.assertFalse(is_valid_pwd("hijklmmn"))

    def test_abbceffg_invalid(self):
        """abbceffg meets third requirement but fails first (no straight)."""
        self.assertFalse(is_valid_pwd("abbceffg"))

    def test_abbcegjk_invalid(self):
        """abbcegjk fails third requirement (only one double letter bb)."""
        self.assertFalse(is_valid_pwd("abbcegjk"))

    def test_increment_abcdefgh(self):
        """Next password after abcdefgh is abcdffaa."""
        result = find_next_valid_password("abcdefgh")
        self.assertEqual(result, "abcdffaa")

    def test_next_valid_after_ghijklmn(self):
        """Next password after ghijklmn is ghjaabcc (skips ghi... because i not allowed)."""
        result = find_next_valid_password("ghijklmn")
        self.assertEqual(result, "ghjaabcc")

    def test_valid_passwords(self):
        """Test some known valid passwords."""
        self.assertTrue(is_valid_pwd("abcdffaa"))
        self.assertTrue(is_valid_pwd("ghjaabcc"))
        self.assertTrue(is_valid_pwd("cqjxxyzz"))  # Part 1 answer
        self.assertTrue(is_valid_pwd("cqkaabcc"))  # Part 2 answer

    def test_forbidden_characters(self):
        """Test that passwords with forbidden characters are invalid."""
        self.assertFalse(is_valid_pwd("password"))  # contains 'o'
        self.assertFalse(is_valid_pwd("hacker"))    # contains 'a' and 'k', but no straight or pairs
        self.assertFalse(is_valid_pwd("abc"))       # too short, no pairs

    def test_straight_requirement(self):
        """Test the increasing straight requirement."""
        self.assertTrue(is_valid_pwd("abcdffaa"))   # has abc straight + two pairs (ff, aa)
        self.assertTrue(is_valid_pwd("bcdaabcc"))   # has bcd straight + two pairs (aa, cc)
        self.assertFalse(is_valid_pwd("abcdd"))     # has abc straight but only one pair
        self.assertFalse(is_valid_pwd("abcdf"))     # no straight
        self.assertFalse(is_valid_pwd("azz"))       # a,z,z - no consecutive straight

    def test_pair_requirement(self):
        """Test the pair requirement."""
        self.assertTrue(is_valid_pwd("aabcc"))      # two pairs: aa, cc + straight abc
        self.assertFalse(is_valid_pwd("aabb"))      # two pairs but no straight
        self.assertFalse(is_valid_pwd("aaab"))      # only one pair (overlapping)
        self.assertFalse(is_valid_pwd("abcde"))     # no pairs


if __name__ == "__main__":
    # Run tests if called with test argument
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        main()
