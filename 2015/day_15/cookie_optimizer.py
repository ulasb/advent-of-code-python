#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 15: Science for Hungry People

This script finds the optimal cookie recipe that maximizes score, with optional calorie constraints.
"""

import argparse
import logging
import math
import os
import re
import sys
import tempfile
import time
import unittest
from typing import Dict, Optional, Tuple

# Constants
DEFAULT_INPUT_FILE = "input.txt"
CALORIE_TARGET_PART2 = 500

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Ingredient:
    """
    Represents an ingredient with its properties.

    Attributes:
        name (str): Name of the ingredient
        capacity (int): Capacity points per teaspoon
        durability (int): Durability points per teaspoon
        flavor (int): Flavor points per teaspoon
        texture (int): Texture points per teaspoon
        calories (int): Calories per teaspoon
    """

    def __init__(self, name: str, capacity: int, durability: int, flavor: int, texture: int, calories: int):
        """
        Initialize an ingredient.

        Args:
            name: Name of the ingredient
            capacity: Capacity points per teaspoon
            durability: Durability points per teaspoon
            flavor: Flavor points per teaspoon
            texture: Texture points per teaspoon
            calories: Calories per teaspoon
        """
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __repr__(self) -> str:
        """Return string representation of the ingredient."""
        return f"{self.name}: capacity {self.capacity}, durability {self.durability}, flavor {self.flavor}, texture {self.texture}, calories {self.calories}"


def parse_ingredients(filename: str) -> Dict[str, Ingredient]:
    """
    Parse ingredients from input file into a dictionary.

    Args:
        filename: Path to the input file containing ingredient data

    Returns:
        Dict[str, Ingredient]: Dictionary mapping ingredient names to Ingredient objects

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the input file format is invalid
    """
    ingredients = {}

    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # Parse line like: "Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2"
                match = re.match(r'(.+?): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
                if match:
                    name = match.group(1)
                    capacity = int(match.group(2))
                    durability = int(match.group(3))
                    flavor = int(match.group(4))
                    texture = int(match.group(5))
                    calories = int(match.group(6))

                    ingredients[name] = Ingredient(name, capacity, durability, flavor, texture, calories)
                else:
                    raise ValueError(f"Invalid input format at line {line_num}: {line}")

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")

    return ingredients


def calculate_score(ingredients: Dict[str, Ingredient], amounts: Dict[str, int]) -> int:
    """
    Calculate the cookie score given amounts of each ingredient.

    The score is calculated by summing each property across ingredients, setting
    negative totals to zero, then multiplying the four property totals together.

    Args:
        ingredients: Dictionary of ingredient objects
        amounts: Dictionary mapping ingredient names to teaspoon amounts

    Returns:
        int: Cookie score (product of capacity, durability, flavor, and texture totals)
    """
    total_capacity = 0
    total_durability = 0
    total_flavor = 0
    total_texture = 0

    for name, ingredient in ingredients.items():
        amount = amounts.get(name, 0)
        total_capacity += ingredient.capacity * amount
        total_durability += ingredient.durability * amount
        total_flavor += ingredient.flavor * amount
        total_texture += ingredient.texture * amount

    # Set negative values to 0 as per problem rules
    total_capacity = max(0, total_capacity)
    total_durability = max(0, total_durability)
    total_flavor = max(0, total_flavor)
    total_texture = max(0, total_texture)

    # Calculate final score
    return total_capacity * total_durability * total_flavor * total_texture


def calculate_calories(ingredients: Dict[str, Ingredient], amounts: Dict[str, int]) -> int:
    """
    Calculate the total calories given amounts of each ingredient.

    Args:
        ingredients: Dictionary of ingredient objects
        amounts: Dictionary mapping ingredient names to teaspoon amounts

    Returns:
        int: Total calories for the recipe
    """
    total_calories = 0
    for name, ingredient in ingredients.items():
        amount = amounts.get(name, 0)
        total_calories += ingredient.calories * amount
    return total_calories


def find_optimal_recipe(ingredients: Dict[str, Ingredient], calorie_target: Optional[int] = None) -> Tuple[Dict[str, int], int]:
    """
    Find the optimal amounts of each ingredient to maximize cookie score.

    Uses brute force search to try all possible combinations of ingredient amounts
    that sum to 100 teaspoons.

    Args:
        ingredients: Dictionary of ingredient objects
        calorie_target: If specified, only consider recipes with exactly this many calories

    Returns:
        Tuple[Dict[str, int], int]: (optimal_amounts, max_score) where optimal_amounts
        maps ingredient names to teaspoon amounts
    """
    ingredient_names = list(ingredients.keys())
    n = len(ingredient_names)

    if n == 0:
        return {}, 0

    best_score = 0
    best_amounts = {}

    # Calculate total combinations for logging (stars and bars formula)
    # Number of ways to distribute 100 teaspoons among n ingredients
    total_combinations = math.comb(100 + n - 1, n - 1) if n > 1 else 1
    logger.info(f"Evaluating {n} ingredients ({total_combinations:,} combinations)")

    start_time = time.time()

    # General case using recursion - works for any number of ingredients
    def try_combinations(current_index: int, remaining: int, current_amounts: Dict[str, int]):
        nonlocal best_score, best_amounts

        if current_index == n - 1:
            # Last ingredient gets all remaining
            current_amounts[ingredient_names[current_index]] = remaining

            # Check calorie constraint if specified
            if calorie_target is not None:
                total_calories = calculate_calories(ingredients, current_amounts)
                if total_calories != calorie_target:
                    return

            score = calculate_score(ingredients, current_amounts)
            if score > best_score:
                best_score = score
                best_amounts = current_amounts.copy()
            return

        # Try different amounts for current ingredient
        for amount in range(remaining + 1):
            current_amounts[ingredient_names[current_index]] = amount
            try_combinations(current_index + 1, remaining - amount, current_amounts)

    try_combinations(0, 100, {})

    elapsed_time = time.time() - start_time
    logger.info(f"Evaluation took {elapsed_time:.2f}s")

    return best_amounts, best_score


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 15: Find optimal cookie recipe",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cookie_optimizer.py                    # Use default input.txt
  python3 cookie_optimizer.py -f custom.txt     # Use custom input file
  python3 cookie_optimizer.py --test           # Run unit tests
        """
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f'Input file containing ingredient data (default: {DEFAULT_INPUT_FILE})'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Run unit tests instead of main program'
    )

    return parser.parse_args()


class TestCookieOptimizer(unittest.TestCase):
    """Unit tests for the cookie optimizer."""

    def test_calculate_score_basic(self):
        """Test basic score calculation."""
        ingredients = {
            'Butterscotch': Ingredient('Butterscotch', -1, -2, 6, 3, 8),
            'Cinnamon': Ingredient('Cinnamon', 2, 3, -2, -1, 3)
        }
        amounts = {'Butterscotch': 44, 'Cinnamon': 56}

        score = calculate_score(ingredients, amounts)
        # Expected: capacity=68, durability=80, flavor=152, texture=76
        # Score = 68 * 80 * 152 * 76 = 62842880
        self.assertEqual(score, 62842880)

    def test_calculate_calories(self):
        """Test calorie calculation."""
        ingredients = {
            'Butterscotch': Ingredient('Butterscotch', -1, -2, 6, 3, 8),
            'Cinnamon': Ingredient('Cinnamon', 2, 3, -2, -1, 3)
        }
        amounts = {'Butterscotch': 40, 'Cinnamon': 60}

        calories = calculate_calories(ingredients, amounts)
        # 40*8 + 60*3 = 320 + 180 = 500
        self.assertEqual(calories, 500)

    def test_find_optimal_recipe_no_calorie_constraint(self):
        """Test finding optimal recipe without calorie constraints."""
        ingredients = {
            'Butterscotch': Ingredient('Butterscotch', -1, -2, 6, 3, 8),
            'Cinnamon': Ingredient('Cinnamon', 2, 3, -2, -1, 3)
        }

        amounts, score = find_optimal_recipe(ingredients)
        self.assertEqual(score, 62842880)
        self.assertEqual(amounts['Butterscotch'], 44)
        self.assertEqual(amounts['Cinnamon'], 56)

    def test_find_optimal_recipe_with_calorie_constraint(self):
        """Test finding optimal recipe with calorie constraints."""
        ingredients = {
            'Butterscotch': Ingredient('Butterscotch', -1, -2, 6, 3, 8),
            'Cinnamon': Ingredient('Cinnamon', 2, 3, -2, -1, 3)
        }

        amounts, score = find_optimal_recipe(ingredients, calorie_target=500)
        self.assertEqual(score, 57600000)
        self.assertEqual(amounts['Butterscotch'], 40)
        self.assertEqual(amounts['Cinnamon'], 60)

        # Verify calories
        total_calories = calculate_calories(ingredients, amounts)
        self.assertEqual(total_calories, 500)

    def test_parse_ingredients(self):
        """Test parsing ingredients from string data."""
        test_data = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            ingredients = parse_ingredients(temp_file)
            self.assertEqual(len(ingredients), 2)
            self.assertIn('Butterscotch', ingredients)
            self.assertIn('Cinnamon', ingredients)
            self.assertEqual(ingredients['Butterscotch'].capacity, -1)
            self.assertEqual(ingredients['Cinnamon'].calories, 3)
        finally:
            os.unlink(temp_file)

    def test_empty_ingredients(self):
        """Test behavior with empty ingredients dictionary."""
        amounts, score = find_optimal_recipe({})
        self.assertEqual(amounts, {})
        self.assertEqual(score, 0)


def main(args: argparse.Namespace) -> None:
    """
    Main function to run the cookie optimization.

    Args:
        args: Parsed command-line arguments
    """
    try:
        logger.info(f"Reading ingredient data from {args.file}")
        ingredients = parse_ingredients(args.file)

        if not ingredients:
            logger.error("No ingredients found in input file")
            sys.exit(1)

        logger.info(f"Found {len(ingredients)} ingredients")
        for ingredient in ingredients.values():
            logger.info(f"  {ingredient}")

        # Part 1: Find optimal recipe without calorie constraint
        logger.info("Finding optimal recipe for Part 1...")
        optimal_amounts, max_score = find_optimal_recipe(ingredients)
        logger.info(f"Part 1 - Maximum score: {max_score}")
        for name, amount in optimal_amounts.items():
            logger.info(f"  {name}: {amount} teaspoons")

        # Part 2: Find optimal recipe with exactly 500 calories
        logger.info(f"Finding optimal recipe for Part 2 (exactly {CALORIE_TARGET_PART2} calories)...")
        optimal_amounts_500, max_score_500 = find_optimal_recipe(ingredients, calorie_target=CALORIE_TARGET_PART2)

        if optimal_amounts_500:
            total_calories = calculate_calories(ingredients, optimal_amounts_500)
            logger.info(f"Part 2 - Maximum score: {max_score_500} (calories: {total_calories})")
            for name, amount in optimal_amounts_500.items():
                logger.info(f"  {name}: {amount} teaspoons")
        else:
            logger.warning(f"No recipe found with exactly {CALORIE_TARGET_PART2} calories")

    except FileNotFoundError:
        logger.error(f"Input file '{args.file}' not found.")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input format: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()

    if args.test:
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        main(args)
