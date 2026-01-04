#!/usr/bin/env python3
"""
Unit tests for the Advent of Code 2015 Day 23 Instruction Processor.
"""

import unittest
from instruction_processor import execute


class TestInstructionProcessor(unittest.TestCase):
    """Unit tests for the instruction processor."""

    def test_hlf(self):
        """Test the hlf (half) instruction."""
        instructions = ["hlf a"]
        regs = {"a": 10}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 5)

    def test_tpl(self):
        """Test the tpl (triple) instruction."""
        instructions = ["tpl a"]
        regs = {"a": 7}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 21)

    def test_inc(self):
        """Test the inc (increment) instruction."""
        instructions = ["inc a"]
        regs = {"a": 0}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 1)

    def test_jmp(self):
        """Test the jmp (jump) instruction."""
        instructions = ["jmp +2", "inc a", "inc b"]
        regs = {"a": 0, "b": 0}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 0)
        self.assertEqual(regs["b"], 1)

    def test_jie_even(self):
        """Test the jie (jump if even) instruction with an even value."""
        instructions = ["jie a, +2", "inc a"]
        regs = {"a": 2}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 2)

    def test_jie_odd(self):
        """Test the jie (jump if even) instruction with an odd value."""
        instructions = ["jie a, +2", "inc a"]
        regs = {"a": 3}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 4)

    def test_jio_one(self):
        """Test the jio (jump if one) instruction with value 1."""
        instructions = ["jio a, +2", "inc a"]
        regs = {"a": 1}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 1)

    def test_jio_not_one(self):
        """Test the jio (jump if one) instruction with value other than 1."""
        instructions = ["jio a, +2", "inc a"]
        regs = {"a": 3}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 4)

    def test_example_program(self):
        """
        Test the specific example program provided:
        inc a
        jio a, +2
        tpl a
        inc a
        Expected result: a = 2
        """
        instructions = ["inc a", "jio a, +2", "tpl a", "inc a"]
        regs = {"a": 0}
        execute(instructions, regs)
        self.assertEqual(regs["a"], 2)

    def test_invalid_register(self):
        """Test handling of an invalid register name."""
        instructions = ["inc x"]
        regs = {"a": 0}
        # This should log an error and break, but the registers should remain as they are
        execute(instructions, regs)
        self.assertEqual(regs["a"], 0)


if __name__ == "__main__":
    unittest.main()
