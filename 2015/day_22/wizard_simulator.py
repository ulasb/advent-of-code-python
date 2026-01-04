"""
Wizard Simulator 2015.

This script simulates a turn-based combat between a Wizard player and a Boss.
The goal is to find the minimum mana spent to win the battle.

Created and published by Ulaş Bardak.
Follows Mozilla Public License 2.0.
"""

import heapq
import sys
import argparse
import unittest
from typing import Dict, Tuple, NamedTuple


class GameState(NamedTuple):
    """
    Represents the state of the game at a given point.
    NamedTuple is used to ensure it is hashable for use as a dictionary key.
    """
    player_hp: int
    player_mana: int
    boss_hp: int
    active_effects: Tuple[Tuple[str, int], ...]


class Spell:
    """
    Represents a magic spell with its cost, effects, and duration.

    Attributes:
        name (str): The name of the spell.
        cost (int): Mana cost to cast.
        damage (int): Instant damage dealt.
        heal (int): Instant healing for the player.
        duration (int): Number of rounds the effect lasts.
        effect_armor (int): Armor provided each round the effect is active.
        effect_damage (int): Damage dealt each round the effect is active.
        effect_mana (int): Mana provided each round the effect is active.
    """

    def __init__(
        self,
        name: str,
        cost: int,
        damage: int = 0,
        heal: int = 0,
        duration: int = 0,
        effect_armor: int = 0,
        effect_damage: int = 0,
        effect_mana: int = 0,
    ):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.heal = heal
        self.duration = duration
        self.effect_armor = effect_armor
        self.effect_damage = effect_damage
        self.effect_mana = effect_mana



# Define official spells
MAGIC_MISSILE = Spell("Magic Missile", 53, damage=4)
DRAIN = Spell("Drain", 73, damage=2, heal=2)
SHIELD = Spell("Shield", 113, duration=6, effect_armor=7)
POISON = Spell("Poison", 173, duration=6, effect_damage=3)
RECHARGE = Spell("Recharge", 229, duration=5, effect_mana=101)

SPELLS = [MAGIC_MISSILE, DRAIN, SHIELD, POISON, RECHARGE]
SPELL_MAP = {spell.name: spell for spell in SPELLS}


def apply_effects(state: GameState) -> Tuple[GameState, int]:
    """
    Iterates any active spells effects at the start of each turn.

    Args:
        state: The current GameState.

    Returns:
        Tuple containing updated GameState and current player armor.
    """
    p_hp = state.player_hp
    p_mana = state.player_mana
    b_hp = state.boss_hp
    new_effects_list = []
    p_armor = 0

    for spell_name, timer in state.active_effects:
        spell = SPELL_MAP[spell_name]
        
        # Apply per-turn effects
        p_armor += spell.effect_armor
        b_hp -= spell.effect_damage
        p_mana += spell.effect_mana

        # Decrement timer and keep if active
        if timer > 1:
            new_effects_list.append((spell_name, timer - 1))

    return GameState(p_hp, p_mana, b_hp, tuple(new_effects_list)), p_armor


def simulate_round(
    state: GameState,
    spell: Spell,
    boss_damage: int,
    hard_mode: bool = False,
) -> Tuple[bool, GameState, int]:
    """
    Simulates a player turn and a boss turn.

    Args:
        state: The starting GameState.
        spell: The spell the player chooses to cast.
        boss_damage: The base damage of the boss.
        hard_mode: Whether the simulation is in hard mode.

    Returns:
        Tuple: (win_flag, resulting_state, status)
        status: 0 for continue, -1 for loss.
    """
    # --- PLAYER TURN ---
    p_hp = state.player_hp
    if hard_mode:
        p_hp -= 1
        if p_hp <= 0:
            return False, state, -1

    state = state._replace(player_hp=p_hp)
    state, p_armor = apply_effects(state)
    
    if state.boss_hp <= 0:
        return True, state, 0

    # Cast spell
    p_mana = state.player_mana - spell.cost
    p_hp = state.player_hp + spell.heal
    b_hp = state.boss_hp - spell.damage
    
    new_effects = dict(state.active_effects)
    if spell.duration > 0:
        new_effects[spell.name] = spell.duration

    state = GameState(p_hp, p_mana, b_hp, tuple(sorted(new_effects.items())))

    if state.boss_hp <= 0:
        return True, state, 0

    # --- BOSS TURN ---
    state, b_p_armor = apply_effects(state)
    if state.boss_hp <= 0:
        return True, state, 0

    # Boss attack
    damage = max(1, boss_damage - b_p_armor)
    p_hp = state.player_hp - damage

    state = state._replace(player_hp=p_hp)

    if state.player_hp <= 0:
        return False, state, -1

    return False, state, 0


def find_min_mana(boss_hp: int, boss_damage: int, hard_mode: bool = False) -> int:
    """
    Finds the least amount of mana spent to win using Dijkstra's algorithm.

    Args:
        boss_hp: Initial hit points of the boss.
        boss_damage: Initial damage of the boss.
        hard_mode: Whether hard mode is enabled.

    Returns:
        The minimum mana required to win.
    """
    # Priority Queue: (mana_spent, GameState)
    initial_state = GameState(50, 500, boss_hp, ())
    pq = [(0, initial_state)]
    visited = {}

    while pq:
        mana_spent, current_state = heapq.heappop(pq)

        if current_state in visited and visited[current_state] <= mana_spent:
            continue
        visited[current_state] = mana_spent

        # Peek turn to see what can be cast after start-of-turn effects
        temp_hp = current_state.player_hp
        if hard_mode:
            temp_hp -= 1
            if temp_hp <= 0:
                continue

        peek_state, _ = apply_effects(current_state._replace(player_hp=temp_hp))

        if peek_state.boss_hp <= 0:
            return mana_spent

        active_effect_names = {name for name, _ in peek_state.active_effects}

        for spell in SPELLS:
            if peek_state.player_mana >= spell.cost and spell.name not in active_effect_names:
                win, next_state, status = simulate_round(
                    current_state,
                    spell,
                    boss_damage,
                    hard_mode,
                )

                new_mana_spent = mana_spent + spell.cost
                if win:
                    return new_mana_spent

                if status == 0:
                    if next_state not in visited or visited[next_state] > new_mana_spent:
                        heapq.heappush(pq, (new_mana_spent, next_state))

    return sys.maxsize


class TestWizardSimulator(unittest.TestCase):
    """Unit tests for the Wizard combat simulator."""

    def test_scenario_1(self):
        """Test a simple combat scenario where Poison and Magic Missile are used."""
        p_hp, p_mana = 10, 250
        b_hp, b_damage = 13, 8
        effects = ()

        # Turn 1: Poison
        initial_state = GameState(p_hp, p_mana, b_hp, effects)
        win, next_state, status = simulate_round(
            initial_state, POISON, b_damage
        )
        self.assertFalse(win)
        self.assertEqual(next_state.player_hp, 2)
        self.assertEqual(next_state.player_mana, 77)
        self.assertEqual(next_state.boss_hp, 10)

        # Turn 2: Magic Missile
        win, next_state, status = simulate_round(
            next_state, MAGIC_MISSILE, b_damage
        )
        self.assertTrue(win)
        self.assertEqual(next_state.boss_hp, 0)

    def test_scenario_2(self):
        """Test a complex scenario involving Recharge and Shield."""
        p_hp, p_mana = 10, 250
        b_hp, b_damage = 14, 8
        effects = ()

        # Turn 1: Recharge
        initial_state = GameState(p_hp, p_mana, b_hp, effects)
        win, next_state, status = simulate_round(
            initial_state, RECHARGE, b_damage
        )
        self.assertFalse(win)
        self.assertEqual(next_state.player_hp, 2)
        self.assertEqual(next_state.player_mana, 122)

        # Turn 2: Shield
        win, next_state, status = simulate_round(
            next_state, SHIELD, b_damage
        )
        self.assertFalse(win)
        self.assertEqual(next_state.player_hp, 1)
        self.assertEqual(next_state.player_mana, 211)

        # Turn 3: Drain
        win, next_state, status = simulate_round(
            next_state, DRAIN, b_damage
        )
        self.assertFalse(win)
        self.assertEqual(next_state.player_hp, 2)
        self.assertEqual(next_state.player_mana, 340)


def main():
    """Main execution point for the Wizard Simulator script."""
    parser = argparse.ArgumentParser(description="Advent of Code 2015 Day 22 Solver")
    parser.add_argument(
        "filename",
        nargs="?",
        default="input.txt",
        help="Input file with boss stats",
    )
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    parser.add_argument(
        "--hard",
        action="store_true",
        help="Enable Hard Mode (-1 HP at player turn start)",
    )
    args = parser.parse_args()

    if args.test:
        sys.argv = [sys.argv[0]]
        unittest.main()
        return

    try:
        with open(args.filename, "r", encoding="utf-8") as file:
            stats = {}
            for line in file:
                if ":" in line:
                    key, val = line.split(":")
                    stats[key.strip()] = int(val.strip())
            boss_hp = stats["Hit Points"]
            boss_damage = stats["Damage"]
    except FileNotFoundError:
        print(f"Error: {args.filename} not found.")
        sys.exit(1)
    except (KeyError, ValueError) as error:
        raise ValueError(f"Error parsing file: {error}") from error

    mode = " (HARD MODE)" if args.hard else ""
    print(f"Boss HP: {boss_hp}, Damage: {boss_damage}{mode}")
    result = find_min_mana(boss_hp, boss_damage, args.hard)
    print(f"Least amount of mana to win: {result}")


if __name__ == "__main__":
    main()
