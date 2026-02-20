import unittest
from solve import AssembunnyInterpreter


class TestAssembunnyDay25(unittest.TestCase):
    """Unit tests for Day 25 Assembunny Interpreter."""

    def test_parsing(self):
        """Test if instructions are parsed correctly."""
        raw_instructions = ["cpy 41 a", "inc a", "dec a", "jnz a 2", "out a"]
        interpreter = AssembunnyInterpreter(raw_instructions)
        self.assertEqual(len(interpreter.instructions), 5)
        self.assertEqual(interpreter.instructions[0].op, 0)  # CPY
        self.assertEqual(interpreter.instructions[4].op, 5)  # OUT

    def test_clock_signal_logic(self):
        """Test the output logic for the clock signal."""
        # Simple program that outputs 0, 1 and then halts or loops
        # This is a bit hard to test without a full cycle, 
        # but we can test if it rejects wrong signals.
        raw_instructions = ["out 1"] # Starts with 1, should be 0
        interpreter = AssembunnyInterpreter(raw_instructions)
        self.assertFalse(interpreter.test_clock_signal(0))


if __name__ == "__main__":
    unittest.main()
