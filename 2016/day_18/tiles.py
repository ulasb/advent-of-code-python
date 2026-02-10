"""
Advent of Code Solution
Created by Ulaş Bardak
"""

import sys
from typing import List

INPUT_FILE = "input.txt"

def solve_part(first_row_str: str, total_rows: int) -> int:
    """
    Calculates the number of safe tiles ('.') using bit manipulation.
    Trap rules:
    - (L, C, R) = (1, 1, 0)
    - (L, C, R) = (0, 1, 1)
    - (L, C, R) = (1, 0, 0)
    - (L, C, R) = (0, 0, 1)
    Equivalent to: L != R
    """
    width = len(first_row_str)
    # Convert row to an integer where '^' is 1 and '.' is 0
    # We use bit 0 for the rightmost tile
    row_bits = int(first_row_str.replace('.', '0').replace('^', '1'), 2)
    
    # Mask to keep row within width
    mask = (1 << width) - 1
    safe_count = 0

    for _ in range(total_rows):
        # Count safe tiles: total width minus bits that are set (traps)
        safe_count += width - bin(row_bits).count('1')
        
        # Next row calculation: 
        # Left is (row << 1), Right is (row >> 1)
        # New trap if Left XOR Right is 1
        row_bits = ((row_bits << 1) ^ (row_bits >> 1)) & mask
        
    return safe_count

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            first_row = f.read().strip()
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Part 1: 40 rows
    print(f"Part 1: {solve_part(first_row, 40)}")

    # Part 2: 400,000 rows
    print(f"Part 2: {solve_part(first_row, 400_000)}")

if __name__ == "__main__":
    main()