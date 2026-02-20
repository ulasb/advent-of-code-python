import unittest
from solve import AssembunnyInterpreter, Opcode


class TestAssembunnyDay25(unittest.TestCase):
    """Unit tests for Day 25 Assembunny Interpreter."""

    def test_parsing(self):
        """Test if instructions are parsed correctly."""
        raw_instructions = ["cpy 41 a", "inc a", "dec a", "jnz a 2", "out a"]
        interpreter = AssembunnyInterpreter(raw_instructions)
        self.assertEqual(len(interpreter.instructions), 5)
        self.assertEqual(interpreter.instructions[0].op, Opcode.CPY)
        self.assertEqual(interpreter.instructions[4].op, Opcode.OUT)

    def test_clock_signal_rejection(self):
        """Test that incorrect signals are rejected."""
        # Starts with 1, but should be 0
        raw_instructions = ["out 1"]
        interpreter = AssembunnyInterpreter(raw_instructions)
        self.assertFalse(interpreter.test_clock_signal(0))

        # Correct first bit, but wrong second bit
        raw_instructions = ["out 0", "out 0"]
        interpreter = AssembunnyInterpreter(raw_instructions)
        self.assertFalse(interpreter.test_clock_signal(0))

    def test_clock_signal_detection(self):
        """Test that a valid infinite clock signal is correctly detected."""
        # Simple program that outputs 0, 1 infinitely
        # out 0
        # out 1
        # jnz 1 -2
        raw_instructions = ["out 0", "out 1", "jnz 1 -2"]
        interpreter = AssembunnyInterpreter(raw_instructions)
        # Should return True because it enters a cycle that produces output
        self.assertTrue(interpreter.test_clock_signal(0))


if __name__ == "__main__":
    unittest.main()
