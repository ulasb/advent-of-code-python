"""
Advent of Code 2016 - Day 25: Clock Signal

This code was created and published by Ulaş Bardak.
License: Mozilla Public License 2.0
The Mozilla Public License 2.0 is a free and open-source software license
that allows for the use, modification, and distribution of the software,
provided that any modifications to the licensed code are also made available
under the same license.
"""

import sys
from typing import Dict, List, Tuple, Set, Any
from dataclasses import dataclass
from enum import Enum, auto


class Opcode(Enum):
    """Enumeration of Assembunny opcodes."""

    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()
    TGL = auto()
    OUT = auto()


@dataclass
class Argument:
    """
    Represents an instruction argument.

    Attributes
    ----------
    is_reg : bool
        True if the argument is a register, False if it is a literal value.
    val : int
        The value or register index.
    """

    is_reg: bool
    val: int


@dataclass
class Instruction:
    """
    Represents a single Assembunny instruction.

    Attributes
    ----------
    op : Opcode
        The opcode for the instruction.
    args : List[Argument]
        The list of arguments for the instruction.
    """

    op: Opcode
    args: List[Argument]


class AssembunnyInterpreter:
    """
    An interpreter for the Assembunny assembly language used in Day 25.

    Includes dynamic optimization and infinite loop detection for clock signals.
    """

    def __init__(self, instructions_raw: List[str]):
        """
        Initialize the interpreter with raw instruction strings.

        Parameters
        ----------
        instructions_raw : List[str]
            A list of raw instruction strings from the input file.
        """
        self.reg_map = {"a": 0, "b": 1, "c": 2, "d": 3}
        self.instructions = self._parse(instructions_raw)
        self.regs = [0] * 4
        self.pc = 0
        self.n = len(self.instructions)
        # Store optimizations as {pc: (length_to_skip, macro_type, args)}
        self.optimizations: Dict[int, Tuple[int, str, Tuple[Any, ...]]] = {}
        self.find_optimizations()

    def _parse(self, raw: List[str]) -> List[Instruction]:
        """
        Parse raw instruction strings into a structured format.

        Parameters
        ----------
        raw : List[str]
            The raw string instructions.

        Returns
        -------
        List[Instruction]
            A list of parsed Instruction objects.
        """

        op_map = {
            "cpy": Opcode.CPY,
            "inc": Opcode.INC,
            "dec": Opcode.DEC,
            "jnz": Opcode.JNZ,
            "tgl": Opcode.TGL,
            "out": Opcode.OUT,
        }
        parsed = []
        for line in raw:
            parts = line.split()
            if not parts or parts[0] not in op_map:
                continue
            cmd = op_map[parts[0]]
            args = []
            for p in parts[1:]:
                if p in self.reg_map:
                    args.append(Argument(True, self.reg_map[p]))
                else:
                    try:
                        args.append(Argument(False, int(p)))
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid argument '{p}' in line '{line.strip()}'"
                        ) from e
            parsed.append(Instruction(cmd, args))
        return parsed

    def find_optimizations(self) -> None:
        """
        Scan the program for arithmetic idioms and populate the optimization cache.

        Detects loops like 'a += b' (ADD) or 'a += b * d' (MUL).
        """
        self.optimizations = {}
        i = 0
        while i < self.n:
            # 1. Detect MULTIPLICATION idiom (6 lines)
            # Pattern: cpy b c, inc a, dec c, jnz c -2, dec d, jnz d -5
            if i + 5 < self.n:
                p = self.instructions[i : i + 6]
                if (
                    p[0].op == Opcode.CPY
                    and p[1].op == Opcode.INC
                    and p[2].op == Opcode.DEC
                    and p[3].op == Opcode.JNZ
                    and p[4].op == Opcode.DEC
                    and p[5].op == Opcode.JNZ
                    and not p[3].args[1].is_reg
                    and p[3].args[1].val == -2
                    and not p[5].args[1].is_reg
                    and p[5].args[1].val == -5
                ):
                    temp_reg = p[0].args[1].val
                    target_reg = p[1].args[0].val
                    src_arg = p[0].args[0]
                    outer_reg = p[4].args[0].val

                    if (
                        p[2].args[0].val == temp_reg
                        and p[3].args[0].val == temp_reg
                        and p[4].args[0].val == outer_reg
                        and p[5].args[0].val == outer_reg
                    ):
                        self.optimizations[i] = (
                            6,
                            "MUL",
                            (target_reg, src_arg, outer_reg, temp_reg),
                        )
                        i += 6
                        continue

            # 2. Detect ADDITION idiom (3 lines)
            # Pattern: inc/dec x, dec/inc y, jnz y -2
            if i + 2 < self.n:
                p = self.instructions[i : i + 3]
                if (
                    p[2].op == Opcode.JNZ
                    and not p[2].args[1].is_reg
                    and p[2].args[1].val == -2
                ):
                    # inc x, dec y, jnz y -2
                    if (
                        p[0].op == Opcode.INC
                        and p[1].op == Opcode.DEC
                        and p[2].args[0].val == p[1].args[0].val
                    ):
                        self.optimizations[i] = (
                            3,
                            "ADD",
                            (p[0].args[0].val, p[1].args[0].val),
                        )
                        i += 3
                        continue
                    # dec y, inc x, jnz y -2
                    if (
                        p[0].op == Opcode.DEC
                        and p[1].op == Opcode.INC
                        and p[2].args[0].val == p[0].args[0].val
                    ):
                        self.optimizations[i] = (
                            3,
                            "ADD",
                            (p[1].args[0].val, p[0].args[0].val),
                        )
                        i += 3
                        continue
            i += 1

    def test_clock_signal(self, initial_a: int) -> bool:
        """
        Test if the given initial 'a' produces an infinite clock signal.

        A clock signal is defined as a sequence of 0, 1, 0, 1, ...
        Uses state tracking for cycle detection.

        Parameters
        ----------
        initial_a : int
            The starting value for register 'a'.

        Returns
        -------
        bool
            True if the initial value produces a valid infinite clock signal,
            False otherwise.
        """
        self.regs = [0, 0, 0, 0]
        self.regs[0] = initial_a
        self.pc = 0

        seen_states: Dict[Tuple[int, Tuple[int, ...], int], int] = {}
        next_expected = 0
        output_count = 0

        while self.pc < self.n:
            state = (self.pc, tuple(self.regs), next_expected)
            if state in seen_states:
                # If we've seen this state before AND at least one output was produced
                # since the last time we saw this state, it's a valid infinite signal.
                return output_count > seen_states[state]
            seen_states[state] = output_count

            if self.pc in self.optimizations:
                skip, op, args = self.optimizations[self.pc]
                if op == "MUL":
                    target, src_arg, outer, temp = args
                    val = self.regs[src_arg.val] if src_arg.is_reg else src_arg.val
                    self.regs[target] += val * self.regs[outer]
                    self.regs[temp] = 0
                    self.regs[outer] = 0
                    self.pc += skip
                    continue
                elif op == "ADD":
                    target, source = args
                    self.regs[target] += self.regs[source]
                    self.regs[source] = 0
                    self.pc += skip
                    continue

            instr = self.instructions[self.pc]
            cmd = instr.op
            args = instr.args

            if cmd == Opcode.CPY:
                if args[1].is_reg:
                    val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                    self.regs[args[1].val] = val
                self.pc += 1
            elif cmd == Opcode.INC:
                if args[0].is_reg:
                    self.regs[args[0].val] += 1
                self.pc += 1
            elif cmd == Opcode.DEC:
                if args[0].is_reg:
                    self.regs[args[0].val] -= 1
                self.pc += 1
            elif cmd == Opcode.JNZ:
                val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                if val != 0:
                    offset = self.regs[args[1].val] if args[1].is_reg else args[1].val
                    self.pc += offset
                else:
                    self.pc += 1
            elif cmd == Opcode.OUT:
                val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                if val != next_expected:
                    return False
                next_expected = 1 - next_expected
                output_count += 1
                self.pc += 1
            elif cmd == Opcode.TGL:
                # Should not be present in Day 25 but kept for compatibility
                val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                target_idx = self.pc + val
                if 0 <= target_idx < self.n:
                    target_instr = self.instructions[target_idx]
                    t_cmd = target_instr.op
                    t_args = target_instr.args
                    if len(t_args) == 1:
                        target_instr.op = (
                            Opcode.DEC if t_cmd == Opcode.INC else Opcode.INC
                        )
                    else:
                        target_instr.op = (
                            Opcode.CPY if t_cmd == Opcode.JNZ else Opcode.JNZ
                        )
                    self.find_optimizations()
                self.pc += 1
            else:
                self.pc += 1

        return False


def solve(instructions: List[str]) -> int:
    """
    Find the smallest non-negative integer for register 'a'.

    The value must result in a clock signal (0, 1, 0, 1, ...).

    Parameters
    ----------
    instructions : List[str]
        The raw input instructions.

    Returns
    -------
    int
        The smallest value for 'a' that works, or -1 if none found.
    """
    interpreter = AssembunnyInterpreter(instructions)
    a = 0
    while True:
        if interpreter.test_clock_signal(a):
            return a
        a += 1
        if a > 10000:  # Safety break
            break
    return -1


def main() -> int:
    """
    Main entry point for the script.

    Returns
    -------
    int
        Exit code: 0 for success, 1 for errors.
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found.", file=sys.stderr)
        return 1

    print("Searching for the lowest value of 'a'...")
    result = solve(lines)
    print(f"Result: {result}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
