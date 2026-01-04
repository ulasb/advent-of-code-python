import unittest
import hashlib
import sys

# Maximum int to search up to
SEARCH_MAX = 10000000

def find_smallest_suffix(secret_key:str, num_zeros:int) -> int:
    """
    Given a secret key and number of zeros to consider, returns the lowest
    positive number that produces an MD5 hash that starts with at least
    the given number of zeros.

    Args:
        secret_key: The base string to hash
        num_zeros: Number of leading zeros required in the hash

    Returns:
        The smallest integer suffix that produces the required hash, or -1 if not found
    """
    if not secret_key:
        raise ValueError("secret_key cannot be empty")
    if num_zeros < 1:
        raise ValueError("num_zeros must be at least 1")
    if num_zeros > 32:
        raise ValueError("num_zeros cannot exceed 32 (MD5 hex digest length)")

    # Pre-encode the secret key for efficiency
    secret_key_bytes = secret_key.encode("utf-8")

    for i in range(SEARCH_MAX):
        # Create MD5 hash by combining pre-encoded secret key with current number
        hash_digest = hashlib.md5(secret_key_bytes + str(i).encode("utf-8")).hexdigest()
        if(hash_digest.startswith("0" * num_zeros)):
            return i
    return -1

class TestFindSmallestSuffix(unittest.TestCase):
    def test_abcdef_five_zeros(self):
        """Test that abcdef with 5 zeros gives 609043"""
        result = find_smallest_suffix("abcdef", 5)
        self.assertEqual(result, 609043)

    def test_pqrstuv_five_zeros(self):
        """Test that pqrstuv with 5 zeros gives 1048970"""
        result = find_smallest_suffix("pqrstuv", 5)
        self.assertEqual(result, 1048970)

    def test_simple_case_one_zero(self):
        """Test with 1 zero requirement"""
        result = find_smallest_suffix("test", 1)
        self.assertNotEqual(result, -1)
        self.assertGreaterEqual(result, 0)

    def test_simple_case_two_zeros(self):
        """Test with 2 zeros requirement"""
        result = find_smallest_suffix("test", 2)
        self.assertNotEqual(result, -1)
        self.assertGreaterEqual(result, 0)

    def test_empty_secret_key_raises_error(self):
        """Test that empty secret key raises ValueError"""
        with self.assertRaises(ValueError):
            find_smallest_suffix("", 5)

    def test_zero_zeros_raises_error(self):
        """Test that num_zeros=0 raises ValueError"""
        with self.assertRaises(ValueError):
            find_smallest_suffix("test", 0)

    def test_negative_zeros_raises_error(self):
        """Test that negative num_zeros raises ValueError"""
        with self.assertRaises(ValueError):
            find_smallest_suffix("test", -1)

    def test_too_many_zeros_raises_error(self):
        """Test that num_zeros > 32 raises ValueError"""
        with self.assertRaises(ValueError):
            find_smallest_suffix("test", 33)

    def test_returns_smallest_suffix(self):
        """Test that the function returns the smallest possible suffix"""
        result = find_smallest_suffix("abcdef", 5)
        # Verify this is indeed the smallest by checking that smaller numbers don't work
        for i in range(result):
            hash_digest = hashlib.md5(("abcdef" + str(i)).encode("utf-8")).hexdigest()
            self.assertFalse(hash_digest.startswith("00000"))
        # And verify the result does work
        hash_digest = hashlib.md5(("abcdef" + str(result)).encode("utf-8")).hexdigest()
        self.assertTrue(hash_digest.startswith("00000"))

def main():
    secret_key = "bgvyzdsv"

    smallest_suffix_5 = find_smallest_suffix(secret_key, 5)
    if(smallest_suffix_5 != -1):
        print(f"Smallest_suffix is {smallest_suffix_5}")
    else:
        print("Could not find a suffix that matches the requirements")

    smallest_suffix_6 = find_smallest_suffix(secret_key, 6)
    if(smallest_suffix_6 != -1):
        print(f"Smallest_suffix is {smallest_suffix_6}")
    else:
        print("Could not find a suffix that matches the requirements")

if __name__ == "__main__":
    # Check if tests should be run
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run the main program
        main()