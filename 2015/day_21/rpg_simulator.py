#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 21: RPG Simulator 20XX

This script simulates a turn-based RPG battle to find the most efficient 
and least efficient equipment sets for defeating a boss.

Published by: Ulaş Bardak
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import argparse
import sys
import unittest
from enum import Enum
from typing import List, Optional, Tuple
import itertools


class ItemType(Enum):
    """Enumeration of item types."""

    WEAPON = 1
    ARMOR = 2
    RING = 3


class EquipmentSlots(Enum):
    """Enumeration of equipment slots."""

    WEAPON = 1
    ARMOR = 2
    RING1 = 3
    RING2 = 4


class Item:
    """
    Represents an item that can be equipped.

    Attributes:
        name (str): The name of the item.
        cost (int): The cost in gold.
        damage (int): The damage bonus.
        armor (int): The armor bonus.
        item_type (ItemType): The category of the item.
    """

    def __init__(self, name: str, cost: int, damage: int, armor: int, item_type: ItemType):
        """
        Initialize an Item.

        Args:
            name: Item name.
            cost: Gold cost.
            damage: Damage value.
            armor: Armor value.
            item_type: Category (Weapon, Armor, or Ring).
        """
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor
        self.item_type = item_type

    def __repr__(self) -> str:
        return f"{self.name} (Cost: {self.cost}, Damage: {self.damage}, Armor: {self.armor})"


class Character:
    """
    Represents a character in the game (Player or Boss).

    Attributes:
        name (str): Character name.
        hp (int): Current hit points.
        max_hp (int): Starting hit points.
        base_damage (int): Innate damage.
        base_armor (int): Innate armor.
        weapon (Optional[Item]): Equipped weapon.
        equipped_armor (Optional[Item]): Equipped armor.
        ring1 (Optional[Item]): First ring.
        ring2 (Optional[Item]): Second ring.
    """

    def __init__(self, name: str, hp: int, damage: int = 0, armor: int = 0):
        """
        Initialize a Character.

        Args:
            name: Name of character.
            hp: Initial hit points.
            damage: Base damage.
            armor: Base armor.
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.base_damage = damage
        self.base_armor = armor

        self.weapon: Optional[Item] = None
        self.equipped_armor: Optional[Item] = None
        self.ring1: Optional[Item] = None
        self.ring2: Optional[Item] = None

    def rejuvenate(self):
        """Restore HP to maximum."""
        self.hp = self.max_hp

    def get_total_damage(self) -> int:
        """
        Calculate total damage from base and items.

        Returns:
            int: Calculated damage value.
        """
        damage = self.base_damage
        if self.weapon:
            damage += self.weapon.damage
        if self.ring1:
            damage += self.ring1.damage
        if self.ring2:
            damage += self.ring2.damage
        return damage

    def get_total_armor(self) -> int:
        """
        Calculate total armor from base and items.

        Returns:
            int: Calculated armor value.
        """
        armor = self.base_armor
        if self.equipped_armor:
            armor += self.equipped_armor.armor
        if self.ring1:
            armor += self.ring1.armor
        if self.ring2:
            armor += self.ring2.armor
        return armor

    def equip_weapon(self, item: Item):
        """Equip a weapon."""
        self.weapon = item

    def equip_armor(self, item: Item):
        """Equip armor."""
        self.equipped_armor = item

    def equip_ring1(self, item: Item):
        """Equip first ring."""
        self.ring1 = item

    def equip_ring2(self, item: Item):
        """Equip second ring."""
        self.ring2 = item

    def unequip(self, slot: EquipmentSlots):
        """
        Unequip an item from a specific slot.

        Args:
            slot: The slot to clear.
        """
        if slot == EquipmentSlots.WEAPON:
            self.weapon = None
        elif slot == EquipmentSlots.ARMOR:
            self.equipped_armor = None
        elif slot == EquipmentSlots.RING1:
            self.ring1 = None
        elif slot == EquipmentSlots.RING2:
            self.ring2 = None

    def unequip_all(self):
        """Clear all equipment."""
        self.weapon = None
        self.equipped_armor = None
        self.ring1 = None
        self.ring2 = None

    def show_summary(self):
        """Print character equipment and current stats."""
        print(f"--- {self.name} Summary ---")
        print(f"HP: {self.hp}")
        print(f"Weapon: {self.weapon.name if self.weapon else 'None'}")
        print(f"Armor: {self.equipped_armor.name if self.equipped_armor else 'None'}")
        rings = [r.name for r in [self.ring1, self.ring2] if r]
        print(f"Rings: {', '.join(rings) if rings else 'None'}")
        print(f"Total Damage: {self.get_total_damage()}")
        print(f"Total Armor: {self.get_total_armor()}")
        print("-" * (len(self.name) + 18))

    def attack(self, target: "Character"):
        """
        Conduct a single attack turn.

        Args:
            target: The character being attacked.
        """
        damage = max(self.get_total_damage() - target.get_total_armor(), 1)
        target.hp -= damage


# Item List Definitions
WEAPONS = [
    Item("Dagger", 8, 4, 0, ItemType.WEAPON),
    Item("Shortsword", 10, 5, 0, ItemType.WEAPON),
    Item("Warhammer", 25, 6, 0, ItemType.WEAPON),
    Item("Longsword", 40, 7, 0, ItemType.WEAPON),
    Item("Greataxe", 74, 8, 0, ItemType.WEAPON),
]

ARMOR = [
    Item("None", 0, 0, 0, ItemType.ARMOR),
    Item("Leather", 13, 0, 1, ItemType.ARMOR),
    Item("Chainmail", 31, 0, 2, ItemType.ARMOR),
    Item("Splintmail", 53, 0, 3, ItemType.ARMOR),
    Item("Bandedmail", 75, 0, 4, ItemType.ARMOR),
    Item("Platemail", 102, 0, 5, ItemType.ARMOR),
]

RINGS = [
    Item("None1", 0, 0, 0, ItemType.RING),
    Item("None2", 0, 0, 0, ItemType.RING),
    Item("Damage +1", 25, 1, 0, ItemType.RING),
    Item("Damage +2", 50, 2, 0, ItemType.RING),
    Item("Damage +3", 100, 3, 0, ItemType.RING),
    Item("Defense +1", 20, 0, 1, ItemType.RING),
    Item("Defense +2", 40, 0, 2, ItemType.RING),
    Item("Defense +3", 80, 0, 3, ItemType.RING),
]


def simulate_battle(player: Character, boss: Character) -> str:
    """
    Simulate a battle until death.

    Args:
        player: The player character.
        boss: The boss character.

    Returns:
        str: "Player" if player wins, "Boss" otherwise.
    """
    # Use localized clones for simulation
    p = Character(player.name, player.hp, player.base_damage, player.base_armor)
    p.weapon, p.equipped_armor, p.ring1, p.ring2 = (
        player.weapon,
        player.equipped_armor,
        player.ring1,
        player.ring2,
    )

    b = Character(boss.name, boss.hp, boss.base_damage, boss.base_armor)
    b.weapon, b.equipped_armor, b.ring1, b.ring2 = (
        boss.weapon,
        boss.equipped_armor,
        boss.ring1,
        boss.ring2,
    )

    while p.hp > 0 and b.hp > 0:
        p.attack(b)
        if b.hp <= 0:
            return "Player"
        b.attack(p)
    return "Player" if p.hp > 0 else "Boss"


def parse_boss_stats(filename: str) -> Character:
    """
    Parse boss stats from a file.

    Args:
        filename: Path to the puzzle input.

    Returns:
        Character: Initialized Boss object.

    Raises:
        FileNotFoundError: If file is missing.
        ValueError: If file data is malformed.
    """
    stats = {}
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":")
                stats[key.strip()] = int(val.strip())

    if not all(k in stats for k in ["Hit Points", "Damage", "Armor"]):
        missing = [k for k in ["Hit Points", "Damage", "Armor"] if k not in stats]
        raise ValueError(f"Missing required boss stats: {', '.join(missing)}")

    return Character("Boss", stats["Hit Points"], stats["Damage"], stats["Armor"])


class TestRPGBattle(unittest.TestCase):
    """Unit tests for the battle simulation."""

    def test_example_scenario(self):
        """Test the specific scenario provided in the puzzle description."""
        player = Character("Player", 8, 5, 5)
        boss = Character("Boss", 12, 7, 2)
        winner = simulate_battle(player, boss)
        self.assertEqual(winner, "Player")


def main():
    """Main execution entry point."""
    parser = argparse.ArgumentParser(description="AoC 2015 Day 21 Simulator")
    parser.add_argument(
        "input", nargs="?", default="input.txt", help="Puzzle input file"
    )
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    args = parser.parse_args()

    if args.test:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestRPGBattle)
        unittest.TextTestRunner().run(suite)
        return

    try:
        boss = parse_boss_stats(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    player = Character("Player", 100, 0, 0)

    min_cost = float("inf")
    max_cost = 0
    best_setup = None
    worst_setup = None

    for w in WEAPONS:
        for a in ARMOR:
            for r1, r2 in itertools.combinations(RINGS, 2):

                    player.unequip_all()
                    player.equip_weapon(w)
                    player.equip_armor(a)
                    player.equip_ring1(r1)
                    player.equip_ring2(r2)

                    cost = w.cost + a.cost + r1.cost + r2.cost
                    winner = simulate_battle(player, boss)

                    # Part 1: Minimum gold to win
                    if winner == "Player":
                        if cost < min_cost:
                            min_cost = cost
                            best_setup = (w, a, r1, r2)

                    # Part 2: Maximum gold to lose
                    else:
                        if cost > max_cost:
                            max_cost = cost
                            worst_setup = (w, a, r1, r2)

    print("\n--- Part 1: Cheapest Winning Setup ---")
    if best_setup:
        for item in best_setup:
            if item.cost > 0:
                print(item)
        print(f"Total Gold Cost: {min_cost}")

    print("\n--- Part 2: Most Expensive Losing Setup ---")
    if worst_setup:
        for item in worst_setup:
            if item.cost > 0:
                print(item)
        print(f"Total Gold Cost: {max_cost}")


if __name__ == "__main__":
    main()
