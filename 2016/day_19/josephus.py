from math import log, floor
from collections import deque

def josephus_part1(n: int) -> int:
    """O(1) solution for Part 1: survivor = 2*(n - 2^⌊log₂n⌋) + 1"""
    if n <= 0:
        raise ValueError("n must be positive")
    l = n - (1 << (n.bit_length() - 1))
    return 2 * l + 1


def josephus_part2(n: int) -> int:
    """O(1) solution for Part 2: Josephus variant with removal across circle"""
    if n <= 0:
        raise ValueError("n must be positive")
    
    # Largest power of 3 <= n
    p = 3 ** floor(log(n, 3))
    
    if n == p:
        return n
    elif n <= 2 * p:
        return n - p
    else:
        return 2 * n - 3 * p


def brute_force_part1(n: int) -> int:
    """Brute-force Part 1 using deque rotation (O(n) time, O(n) space)"""
    elves = deque(range(1, n + 1))
    while len(elves) > 1:
        elves.rotate(-1)
        elves.popleft()
    return elves[0]


def brute_force_part2(n: int) -> int:
    """Brute-force Part 2 using two deques (O(n) time, O(n) space)"""
    if n == 1:
        return 1

    # left: [1..mid], right: [mid+1..n]
    mid = n // 2
    left = deque(range(1, mid + 1))
    right = deque(range(mid + 1, n + 1))

    while left and right:
        # Remove across
        if len(left) > len(right):
            left.pop()
        else:
            right.popleft()

        # Rotate: move front of left → back of right, and front of right → back of left
        if not left or not right:
            break
        right.append(left.popleft())
        left.append(right.popleft())

    return left[0] if left else right[0]
    