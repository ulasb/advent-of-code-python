import argparse
import sys
import unittest


def validate_input(parens: str) -> bool:
    """
    Validate that input contains only parentheses characters.
    """
    return all(char in '()' for char in parens)


def simple_paren_count(parens: str) -> int:
    '''
    Part 1:
    Simply count the number of times the parens are opened and closed.
    '''
    if not validate_input(parens):
        raise ValueError("Input must contain only '(' and ')' characters")
    # More efficient: use count() method
    return parens.count('(') - parens.count(')')

def find_first_basement_entry(parens: str) -> int:
    '''
    Part 2:
    Find the first time the floor is -1.
    '''
    if not validate_input(parens):
        raise ValueError("Input must contain only '(' and ')' characters")
    current_floor = 0
    for i, char in enumerate(parens):
        if char == '(':
            current_floor += 1
        elif char == ')':
            current_floor -= 1
        if current_floor == -1:
            return i + 1
    return -1


class TestParenthesesFloorCounter(unittest.TestCase):
    def test_floor_zero(self):
        """Test cases that should result in floor 0"""
        self.assertEqual(simple_paren_count("(())"), 0)
        self.assertEqual(simple_paren_count("()()"), 0)

    def test_floor_three(self):
        """Test cases that should result in floor 3"""
        self.assertEqual(simple_paren_count("((("), 3)
        self.assertEqual(simple_paren_count("(()(()("), 3)
        self.assertEqual(simple_paren_count("))((((("), 3)

    def test_floor_minus_one(self):
        """Test cases that should result in floor -1"""
        self.assertEqual(simple_paren_count("())"), -1)
        self.assertEqual(simple_paren_count("))("), -1)

    def test_floor_minus_three(self):
        """Test cases that should result in floor -3"""
        self.assertEqual(simple_paren_count(")))"), -3)
        self.assertEqual(simple_paren_count(")())())"), -3)

    def test_first_basement_entry(self):
        """Test cases for finding the first time floor reaches -1"""
        self.assertEqual(find_first_basement_entry(")"), 1)
        self.assertEqual(find_first_basement_entry("()())"), 5)

    def test_edge_cases(self):
        """Test edge cases"""
        # Empty string
        self.assertEqual(simple_paren_count(""), 0)
        self.assertEqual(find_first_basement_entry(""), -1)

        # Only opening parentheses
        self.assertEqual(simple_paren_count("((("), 3)
        self.assertEqual(find_first_basement_entry("((("), -1)

        # Only closing parentheses
        self.assertEqual(simple_paren_count(")))"), -3)
        self.assertEqual(find_first_basement_entry(")))"), 1)

    def test_input_validation(self):
        """Test input validation"""
        with self.assertRaises(ValueError):
            simple_paren_count("(()a)")
        with self.assertRaises(ValueError):
            find_first_basement_entry("(1)")


def main():
    parser = argparse.ArgumentParser(description='Advent of Code Day 1: Parentheses Floor Counter')
    parser.add_argument('input_file', nargs='?', default='input.txt',
                       help='Input file containing parentheses (default: input.txt)')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as file:
            parens = file.read().strip()

        # Validate input
        if not validate_input(parens):
            print("Error: Input file must contain only '(' and ')' characters", file=sys.stderr)
            sys.exit(1)

        first_basement_entry = find_first_basement_entry(parens)
        final_floor = simple_paren_count(parens)

        print(f"Final floor: {final_floor}")
        print(f"First basement entry: {first_basement_entry}")

    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    # Run main program
    main()
