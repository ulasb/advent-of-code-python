"""
Advent of Code 2016 - Day 23: Safe Cracking

This code was created and published by Ulaş Bardak.
License: Mozilla Public License 2.0
The Mozilla Public License 2.0 is a free and open-source software license
that allows for the use, modification, and distribution of the software,
provided that any modifications to the licensed code are also made available
under the same license.
"""

import sys
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# Opcode constants
CPY, INC, DEC, JNZ, TGL = 0, 1, 2, 3, 4


@dataclass
class Argument:
    """Represents an instruction argument, which can be a register or a literal value."""

    is_reg: bool
    val: int


@dataclass
class Instruction:
    """Represents a single Assembunny instruction."""

    op: int
    args: List[Argument]


class AssembunnyInterpreter:
    """
    An interpreter for the Assembunny assembly language used in Day 23.

    This interpreter includes dynamic peephole optimization features to
    detect and accelerate arithmetic patterns like addition and multiplication.
    Compared to Day 12, there is a new instruction 'tgl' that toggles
    instructions, which can be used to create loops. This makes the program
    much harder to optimize manually. This is part of the reason why this
    class was necessary to create with dynamic optimization.
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
        self.optimizations: Dict[int, Tuple[int, str, Tuple]] = {}

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
        op_map = {"cpy": CPY, "inc": INC, "dec": DEC, "jnz": JNZ, "tgl": TGL}
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
                    p[0].op == CPY
                    and p[1].op == INC
                    and p[2].op == DEC
                    and p[3].op == JNZ
                    and p[4].op == DEC
                    and p[5].op == JNZ
                    and not p[3].args[1].is_reg
                    and p[3].args[1].val == -2
                    and not p[5].args[1].is_reg
                    and p[5].args[1].val == -5
                ):
                    # Ensure register consistency
                    temp_reg = p[0].args[1].val  # 'c'
                    target_reg = p[1].args[0].val  # 'a'
                    src_arg = p[0].args[0]  # 'b' (as Argument)
                    outer_reg = p[4].args[0].val  # 'd'

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
                    p[2].op == JNZ
                    and not p[2].args[1].is_reg
                    and p[2].args[1].val == -2
                ):
                    # inc x, dec y, jnz y -2
                    if (
                        p[0].op == INC
                        and p[1].op == DEC
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
                        p[0].op == DEC
                        and p[1].op == INC
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

    def run(self, initial_a: int) -> int:
        """
        Execute the stored program with a given initial value in register 'a'.

        Parameters
        ----------
        initial_a : int
            The starting value for register 'a'.

        Returns
        -------
        int
            The final value in register 'a' after the program halts.
        """
        self.regs = [0, 0, 0, 0]
        self.regs[0] = initial_a
        self.pc = 0
        self.find_optimizations()

        while self.pc < self.n:
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

            if cmd == CPY:
                if args[1].is_reg:  # Target must be a register
                    val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                    self.regs[args[1].val] = val
                self.pc += 1
            elif cmd == INC:
                if args[0].is_reg:
                    self.regs[args[0].val] += 1
                self.pc += 1
            elif cmd == DEC:
                if args[0].is_reg:
                    self.regs[args[0].val] -= 1
                self.pc += 1
            elif cmd == JNZ:
                val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                if val != 0:
                    offset = self.regs[args[1].val] if args[1].is_reg else args[1].val
                    self.pc += offset
                else:
                    self.pc += 1
            elif cmd == TGL:
                val = self.regs[args[0].val] if args[0].is_reg else args[0].val
                target_idx = self.pc + val
                if 0 <= target_idx < self.n:
                    target_instr = self.instructions[target_idx]
                    t_cmd = target_instr.op
                    t_args = target_instr.args
                    if len(t_args) == 1:
                        target_instr.op = DEC if t_cmd == INC else INC
                    else:
                        target_instr.op = CPY if t_cmd == JNZ else JNZ
                    self.find_optimizations()
                self.pc += 1

        return self.regs[0]


def solve_part_1(instructions: List[str]) -> int:
    """
    Solve Part 1 of the challenge.

    Parameters
    ----------
    instructions : List[str]
        The raw input instructions.

    Returns
    -------
    int
        The final value in register 'a'.
    """
    interpreter = AssembunnyInterpreter(instructions)
    return interpreter.run(7)


def solve_part_2(instructions: List[str]) -> int:
    """
    Solve Part 2 of the challenge.

    Parameters
    ----------
    instructions : List[str]
        The raw input instructions.

    Returns
    -------
    int
        The final value in register 'a'.
    """
    interpreter = AssembunnyInterpreter(instructions)
    return interpreter.run(12)


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

    print("Running Part 1 (a=7)...")
    print(f"[Part 1] Result: {solve_part_1(lines)}")

    print("\nRunning Part 2 (a=12)...")
    print(f"[Part 2] Result: {solve_part_2(lines)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
