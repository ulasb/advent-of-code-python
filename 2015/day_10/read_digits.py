from itertools import groupby
from string import digits
from typing import Dict
import sys

START_NUMBER = "1113122113"
PART_1_STEPS = 40
PART_2_STEPS = 50

def get_reading(input_num: str) -> str:
    """Generate the next look-and-say sequence iteration."""
    if not input_num:
        return ""
    if not input_num.isdigit():
        raise ValueError("Input must contain only digits")

    # Group consecutive identical digits and create the next sequence
    groups = []
    for digit, group in groupby(input_num):
        # Count how many times this digit appears consecutively
        count = sum(1 for _ in group)
        # Format as "count + digit"
        groups.append(f"{count}{digit}")

    return "".join(groups)


def run_sequence(start: str, steps: int) -> str:
    """Run the look-and-say sequence for specified steps."""
    result = start
    for _ in range(steps):
        result = get_reading(result)
    return result

parts_and_steps: Dict[str, int] = {
    "Part 1": PART_1_STEPS,
    "Part 2": PART_2_STEPS
}

def run_tests():
    """Run unit tests for the look-and-say sequence."""
    test_cases = [
        ("1", "11", "1 becomes 11 (1 copy of digit 1)"),
        ("11", "21", "11 becomes 21 (2 copies of digit 1)"),
        ("21", "1211", "21 becomes 1211 (one 2 followed by one 1)"),
        ("1211", "111221", "1211 becomes 111221 (one 1, one 2, and two 1s)"),
        ("111221", "312211", "111221 becomes 312211 (three 1s, two 2s, and one 1)")
    ]

    print("Running unit tests...")
    all_passed = True

    for input_str, expected, description in test_cases:
        result = get_reading(input_str)
        passed = result == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {description}")
        if not passed:
            print(f"      Expected: {expected}")
            print(f"      Got:      {result}")
            all_passed = False

    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")

    return all_passed


if __name__ == "__main__":
    # Run tests first
    if not run_tests():
        sys.exit(1)
    print("\n" + "="*50 + "\n")

    # Run the main program
    for part_name, step_count in parts_and_steps.items():
        result = run_sequence(START_NUMBER, step_count)
        print(f"Total length after {step_count} steps in {part_name}: {len(result)}")