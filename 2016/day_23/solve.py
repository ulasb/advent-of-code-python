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

# Opcode constants
CPY, INC, DEC, JNZ, TGL = 0, 1, 2, 3, 4


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

    def _parse(self, raw: List[str]) -> List[List[Any]]:
        """
        Parse raw instruction strings into a structured format.

        Parameters
        ----------
        raw : List[str]
            The raw string instructions.

        Returns
        -------
        List[List[Any]]
            A list of parsed instructions where each instruction is represented
            as a list [opcode, [args]].
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
                    args.append([True, self.reg_map[p]])
                else:
                    try:
                        args.append([False, int(p)])
                    except ValueError as e:
                        raise ValueError(f"Invalid argument '{p}' in line '{line.strip()}'") from e
            parsed.append([cmd, args])
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
                p = [self.instructions[i + j] for j in range(6)]
                if (
                    p[0][0] == CPY
                    and p[1][0] == INC
                    and p[2][0] == DEC
                    and p[3][0] == JNZ
                    and p[4][0] == DEC
                    and p[5][0] == JNZ
                    and p[3][1][1] == [False, -2]
                    and p[5][1][1] == [False, -5]
                ):
                    # Ensure register consistency
                    temp_reg = p[0][1][1][1]  # 'c'
                    target_reg = p[1][1][0][1]  # 'a'
                    src_val_data = p[0][1][0]  # 'b' (as value or reg)
                    outer_reg = p[4][1][0][1]  # 'd'

                    if (
                        p[2][1][0][1] == temp_reg
                        and p[3][1][0][1] == temp_reg
                        and p[4][1][0][1] == outer_reg
                        and p[5][1][0][1] == outer_reg
                    ):
                        self.optimizations[i] = (
                            6,
                            "MUL",
                            (target_reg, src_val_data, outer_reg, temp_reg),
                        )
                        i += 6
                        continue

            # 2. Detect ADDITION idiom (3 lines)
            # Pattern: inc/dec x, dec/inc y, jnz y -2
            if i + 2 < self.n:
                p = [self.instructions[i + j] for j in range(3)]
                if p[2][0] == JNZ and p[2][1][1] == [False, -2]:
                    # inc x, dec y, jnz y -2
                    if p[0][0] == INC and p[1][0] == DEC and p[2][1][0] == p[1][1][0]:
                        self.optimizations[i] = (
                            3,
                            "ADD",
                            (p[0][1][0][1], p[1][1][0][1]),
                        )
                        i += 3
                        continue
                    # dec y, inc x, jnz y -2
                    if p[0][0] == DEC and p[1][0] == INC and p[2][1][0] == p[0][1][0]:
                        self.optimizations[i] = (
                            3,
                            "ADD",
                            (p[1][1][0][1], p[0][1][0][1]),
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
                    target, (src_is_reg, src_val), outer, temp = args
                    val = self.regs[src_val] if src_is_reg else src_val
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

            cmd, args = self.instructions[self.pc]

            if cmd == CPY:
                if args[1][0]:  # Target must be a register
                    is_reg, val = args[0]
                    self.regs[args[1][1]] = self.regs[val] if is_reg else val
                self.pc += 1
            elif cmd == INC:
                if args[0][0]:
                    self.regs[args[0][1]] += 1
                self.pc += 1
            elif cmd == DEC:
                if args[0][0]:
                    self.regs[args[0][1]] -= 1
                self.pc += 1
            elif cmd == JNZ:
                is_reg, val = args[0]
                val = self.regs[val] if is_reg else val
                if val != 0:
                    is_reg2, val2 = args[1]
                    offset = self.regs[val2] if is_reg2 else val2
                    self.pc += offset
                else:
                    self.pc += 1
            elif cmd == TGL:
                is_reg, val = args[0]
                val = self.regs[val] if is_reg else val
                target_idx = self.pc + val
                if 0 <= target_idx < self.n:
                    t_cmd, t_args = self.instructions[target_idx]
                    if len(t_args) == 1:
                        self.instructions[target_idx][0] = DEC if t_cmd == INC else INC
                    else:
                        self.instructions[target_idx][0] = CPY if t_cmd == JNZ else JNZ
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


def main() -> None:
    """
    Main entry point for the script.
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found.", file=sys.stderr)
        sys.exit(1)

    print("Running Part 1 (a=7)...")
    print(f"[Part 1] Result: {solve_part_1(lines)}")

    print("\nRunning Part 2 (a=12)...")
    print(f"[Part 2] Result: {solve_part_2(lines)}")


if __name__ == "__main__":
    main()
