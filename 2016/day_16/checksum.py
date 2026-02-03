"""
Dragon Checksum - Advent of Code 2016 Day 16

This code was created and published by Ulaş Bardak.
This project follows the Mozilla Public License 2.0 (MPL 2.0).
MPL 2.0 is a weak copyleft license that allows you to use the code in
larger works as long as you make the source code of the MPL-licensed
files available under the MPL as well.

The algorithm fills a disk of a given size starting from an initial state
using a modified dragon curve and calculates a checksum until the checksum
is of odd length.
"""

import sys


def generate(data: str) -> str:
    """
    Generate more data using a modified dragon curve.

    The process follows:
    1. Call the data you have 'a'.
    2. Create a copy of 'a' and call it 'b'.
    3. Reverse the order of the characters in 'b'.
    4. In 'b', replace all instances of 0 with 1 and all 1s with 0.
    5. The resulting data is 'a', then a single 0, then 'b'.

    Parameters
    ----------
    data : str
        The initial binary string.

    Returns
    -------
    str
        The expanded binary string.
    """
    # Using translate for faster bit flipping
    trans = str.maketrans("01", "10")
    b = data[::-1].translate(trans)
    return data + "0" + b


def checksum(data: str) -> str:
    """
    Calculate the checksum of a binary string.

    The checksum is calculated by considering pairs of characters:
    - If the two characters are the same (00 or 11), the next checksum character is 1.
    - If the two characters are different (01 or 10), the next checksum character is 0.

    Parameters
    ----------
    data : str
        The binary string to calculate the checksum for.

    Returns
    -------
    str
        The calculated checksum.
    """
    return "".join("1" if data[i] == data[i + 1] else "0" for i in range(0, len(data), 2))


def calculate_disk_checksum(initial_state: str, disk_size: int) -> str:
    """
    Fill a disk to the required size and calculate its final checksum.

    Parameters
    ----------
    initial_state : str
        The initial binary string to start with.
    disk_size : int
        The size of the disk to fill.

    Returns
    -------
    str
        The final checksum of the disk.
    """
    data = initial_state
    while len(data) < disk_size:
        data = generate(data)

    data = data[:disk_size]

    current_checksum = checksum(data)
    while len(current_checksum) % 2 == 0:
        current_checksum = checksum(current_checksum)

    return current_checksum


def main(filename: str = "input.txt"):
    """
    Run Part 1 and Part 2 of the Day 16 challenge.

    Parameters
    ----------
    filename : str, optional
        The path to the input file containing the initial state, by default "input.txt".
    """
    try:
        with open(filename, "r") as f:
            initial_state = f.read().strip()
    except FileNotFoundError:
        # Fallback for convenience if file is missing during quick runs
        initial_state = "01111010110010011"

    # Part 1: Disk size 272
    part1_result = calculate_disk_checksum(initial_state, PART1_DISK_SIZE)
    print(f"Part 1 (Disk {PART1_DISK_SIZE}): {part1_result}")

    # Part 2: Disk size 35651584
    part2_result = calculate_disk_checksum(initial_state, PART2_DISK_SIZE)
    print(f"Part 2 (Disk {PART2_DISK_SIZE}): {part2_result}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    main(input_file)
