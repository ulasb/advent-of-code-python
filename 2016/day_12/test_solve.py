"""
Tests for Advent of Code 2016 - Day 12
"""

import unittest
from solve import run_program


class TestDay12(unittest.TestCase):
    """
    Test cases for Day 12 solution.
    """

    def test_example(self):
        """
        Tests the provided example from the problem description.
        """
        instructions = [
            "cpy 41 a",
            "inc a",
            "inc a",
            "dec a",
            "jnz a 2",
            "dec a",
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["a"], 42)

    def test_cpy_register(self):
        """
        Tests copying from one register to another.
        """
        instructions = [
            "cpy 10 a",
            "cpy a b",
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["b"], 10)

    def test_jnz_zero(self):
        """
        Tests jnz when the value is zero.
        """
        instructions = [
            "jnz 0 2",
            "inc a",
            "inc a",
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["a"], 2)

    def test_jnz_nonzero(self):
        """
        Tests jnz when the value is non-zero.
        """
        instructions = [
            "jnz 1 2",
            "inc a",
            "inc a",
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["a"], 1)

    def test_peephole_add(self):
        """
        Tests the peephole optimization for addition loops.
        """
        instructions = [
            "cpy 5 b",
            "cpy 10 a",
            "inc a",
            "dec b",
            "jnz b -2", # a should be 15, b should be 0
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["a"], 15)
        self.assertEqual(final_registers["b"], 0)

    def test_peephole_add_reversed(self):
        """
        Tests the peephole optimization for addition loops with reversed instructions.
        """
        instructions = [
            "cpy 5 b",
            "cpy 10 a",
            "dec b",
            "inc a",
            "jnz b -2", # a should be 15, b should be 0
        ]
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        final_registers = run_program(instructions, registers)
        self.assertEqual(final_registers["a"], 15)
        self.assertEqual(final_registers["b"], 0)


if __name__ == "__main__":
    unittest.main()
