import pytest
from josephus import (
    josephus_part1, josephus_part2,
    brute_force_part1, brute_force_part2
)


# Test basic examples
@pytest.mark.parametrize("n,expected", [
    (1, 1),
    (2, 1),
    (3, 3),
    (4, 1),
    (5, 3),  # given in AoC
    (6, 5),
    (7, 7),
    (8, 1),
    (9, 3),
    (10, 5),
])
def test_part1_small(n: int, expected: int):
    assert josephus_part1(n) == expected
    assert brute_force_part1(n) == expected


# Part 2 AoC examples
@pytest.mark.parametrize("n,expected", [
    (1, 1),
    (2, 1),
    (3, 3),
    (4, 1),
    (5, 2),  # given in AoC
    (6, 3),
    (7, 5),
    (8, 7),
    (9, 9),
    (10, 1),
    (11, 2),
    (12, 3),
])
def test_part2_small(n: int, expected: int):
    assert josephus_part2(n) == expected
    # Brute-force only for n ≤ 10 (slow beyond)
    if n <= 10:
        assert brute_force_part2(n) == expected


# Edge cases
def test_part1_edge_cases():
    assert josephus_part1(1) == 1
    with pytest.raises(ValueError):
        josephus_part1(0)
    with pytest.raises(ValueError):
        josephus_part1(-1)


def test_part2_edge_cases():
    assert josephus_part2(1) == 1
    with pytest.raises(ValueError):
        josephus_part2(0)
    with pytest.raises(ValueError):
        josephus_part2(-1)


# Stress test correctness vs brute-force for n ≤ 100
@pytest.mark.parametrize("n", list(range(1, 101)))
def test_formulas_match_brute_force(n: int):
    assert josephus_part1(n) == brute_force_part1(n)
    if n <= 20:
        assert josephus_part2(n) == brute_force_part2(n)