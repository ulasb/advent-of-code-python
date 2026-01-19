# Created and published by Ulaş Bardak.
# This code is licensed under the Mozilla Public License 2.0 (MPL-2.0).
# The MPL 2.0 is a "weak" copyleft license that allows you to use this
# code in your own projects, while requiring that any modifications to
# the licensed files be shared under the same license terms.

import sys
import os


def decrypt_name(name: str, sector_id: int) -> str:
    """
    Decrypts the name using the sector ID.

    Parameters
    ----------
    name : str
        The room name with dashes removed.
    sector_id : int
        The sector ID.

    Returns
    -------
    str
        The decrypted name.
    """
    return "".join([chr((ord(char) - ord("a") + sector_id) % 26 + ord("a")) for char in name])


def calculate_checksum(name):
    """
    Calculates the checksum for a given name.

    Parameters
    ----------
    name : str
        The room name with dashes removed.

    Returns
    -------
    str
        The 5-character checksum.
    """
    # Count the frequency of each character in the name
    char_count = {}
    for char in name:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    # Sort the characters by frequency and then alphabetically
    sorted_chars = sorted(char_count.items(), key=lambda x: (-x[1], x[0]))

    # Take the first 5 characters as the checksum
    return "".join([x[0] for x in sorted_chars[:5]])


def validate(line):
    """
    Validates a single line from the input file.

    Parameters
    ----------
    line : str
        A single line from the room list.

    Returns
    -------
    int
        The sector ID if the room is valid, 0 otherwise.
    """
    line = line.strip()

    if not line:
        return 0

    try:
        parts = line.split("-")
        sector_id_part, checksum_part = parts[-1].split("[")
        sector_id = int(sector_id_part)
        checksum = checksum_part.replace("]", "")
        name = "".join(parts[:-1])

        # We will also decrypt the name
        decrypted_name = decrypt_name(name, sector_id)
        if decrypted_name == "northpoleobjectstorage":
            print("Sector ID for Storage:", sector_id)

        # Check if the checksum is valid
        if checksum != calculate_checksum(name):
            return 0

        return sector_id
    except (ValueError, IndexError):
        # Specific exception handling as per AGENTS.md
        return 0


def main():
    """
    Main entry point for the script.
    """
    # Get filename from command line argument or default to input.txt
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    valid_count = 0
    with open(filename, "r") as f:
        for line in f:
            valid_count += validate(line)

    print(f"Total sector ID sum: {valid_count}")


if __name__ == "__main__":
    main()
