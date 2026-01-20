import re

# This code was created and published by Ulaş Bardak.
# It is licensed under the Mozilla Public License 2.0 (MPL 2.0).
# The MPL 2.0 is a permissive "weak copyleft" license that allows the code
# to be used in both open source and proprietary projects, provided that
# any modifications to the original code are also shared under the MPL.


def has_abba(s: str) -> bool:
    """Check if a string contains an ABBA pattern.

    An ABBA is any four-character sequence where the first two characters
    are different, and the sequence is followed by the reverse of those
    two characters (e.g., xyyx or abba).

    Parameters
    ----------
    s : str
        The string to check.

    Returns
    -------
    bool
        True if an ABBA pattern is found, False otherwise.
    """
    for i in range(len(s) - 3):
        if s[i] == s[i + 3] and s[i + 1] == s[i + 2] and s[i] != s[i + 1]:
            return True
    return False


def supports_tls(ip: str) -> bool:
    """Determine if an IP address supports Transport-Layer Snooping (TLS).

    IP supports TLS if it has an ABBA outside square brackets and no
    ABBA inside any square brackets.

    Parameters
    ----------
    ip : str
        The IP address to check.

    Returns
    -------
    bool
        True if the IP supports TLS, False otherwise.
    """
    parts = re.split(r"\[|\]", ip)
    outside = parts[0::2]
    inside = parts[1::2]

    if any(has_abba(p) for p in inside):
        return False
    return any(has_abba(p) for p in outside)


def supports_ssl(ip: str) -> bool:
    """Determine if an IP address supports Super-Secret Listening (SSL).

    An IP supports SSL if it contains an ABA pattern outside square brackets
    and a corresponding BAB pattern inside square brackets.

    Parameters
    ----------
    ip : str
        The IP address to check.

    Returns
    -------
    bool
        True if the IP supports SSL, False otherwise.
    """
    parts = re.split(r"\[|\]", ip)
    outside = parts[0::2]
    inside = parts[1::2]

    # Collect all ABA patterns from supernet segments into a set
    abas = set()
    for segment in outside:
        for i in range(len(segment) - 2):
            if segment[i] == segment[i + 2] and segment[i] != segment[i + 1]:
                abas.add(segment[i : i + 3])

    # If no ABAs found, SSL is not supported
    if not abas:
        return False

    # Check hypernet segments for any corresponding BAB patterns
    for segment in inside:
        for i in range(len(segment) - 2):
            if segment[i] == segment[i + 2] and segment[i] != segment[i + 1]:
                # Construct the ABA that would correspond to this BAB
                target_aba = segment[i + 1] + segment[i] + segment[i + 1]
                if target_aba in abas:
                    return True

    return False


def solve(filename: str = "input.txt") -> tuple[int, int]:
    """Solve the problem using the provided input file.

    Parameters
    ----------
    filename : str, optional
        The path to the input file, by default "input.txt"

    Returns
    -------
    tuple[int, int]
        A tuple containing the results for Part 1 and Part 2.
    """
    with open(filename, "r") as f:
        ips = f.read().splitlines()

    p1 = sum(1 for ip in ips if supports_tls(ip))
    p2 = sum(1 for ip in ips if supports_ssl(ip))

    return p1, p2


if __name__ == "__main__":
    filename = "input.txt"
    try:
        p1, p2 = solve(filename)
        print(f"Part 1: {p1}")
        print(f"Part 2: {p2}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
