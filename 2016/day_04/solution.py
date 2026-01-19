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
    return "".join(
        [chr((ord(char) - ord("a") + sector_id) % 26 + ord("a")) for char in name]
    )


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
    # Count the frequency of each character in the name using dict.get()
    char_count = {}
    for char in name:
        char_count[char] = char_count.get(char, 0) + 1

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
    tuple (int, str)
        A tuple containing the sector ID and the room name (with dashes removed)
        if the room is valid, or (0, "") otherwise.
    """
    line = line.strip()

    if not line:
        return 0, ""

    parts = line.split("-")
    sector_id_part, checksum_part = parts[-1].split("[")
    sector_id = int(sector_id_part)
    checksum = checksum_part.replace("]", "")
    name = "".join(parts[:-1])

    # Check if the checksum is valid
    if checksum != calculate_checksum(name):
        return 0, ""

    return sector_id, name


def main():
    """
    Main entry point for the script.
    """
    # Get filename from command line argument or default to input.txt
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    sector_id_sum = 0
    try:
        with open(filename, "r") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    sector_id, name = validate(line)
                    if sector_id > 0:
                        sector_id_sum += sector_id

                        # Part 2 logic: check for north pole object storage
                        decrypted_name = decrypt_name(name, sector_id)
                        if "northpole" in decrypted_name:
                            print(
                                f"Room found: {decrypted_name} (Sector ID: {sector_id})"
                            )

                except (ValueError, IndexError) as e:
                    # Specific error handling at the top level
                    print(f"Error processing line {line_num}: {e}")

    except IOError as e:
        print(f"File error: {e}")
        sys.exit(1)

    print(f"Total sector ID sum: {sector_id_sum}")


if __name__ == "__main__":
    main()
