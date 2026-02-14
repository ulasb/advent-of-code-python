import unittest
import sys

# swap position X with position Y means that the letters at indexes X and Y 
# (counting from 0) should be swapped.
def swap_x_y(password, x, y):
    password = list(password)
    password[x], password[y] = password[y], password[x]
    return ''.join(password)

# swap letter X with letter Y means that the letters X and Y should be swapped 
# (regardless of where they appear in the string).
def swap_letter_x_y(password, x, y):
    password = list(password)
    for i in range(len(password)):
        if password[i] == x:
            password[i] = y
        elif password[i] == y:
            password[i] = x
    return ''.join(password)

# rotate left/right X steps means that the whole string should be rotated; 
# for example, one right rotation would turn abcd into dabc.
def rotate_left_right_x_steps(password, direction, steps):
    steps = steps % len(password)
    if direction == 'left':
        return password[steps:] + password[:steps]
    else:
        return password[-steps:] + password[:-steps]

# rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as
# follows: rotate the string to the right once, plus a number of times equal to the index of X, plus one additional time if the index of X is at least 4.
def rotate_based_on_position(password, letter):
    index = password.index(letter)
    steps = 1 + index + (1 if index >= 4 else 0)
    return rotate_left_right_x_steps(password, 'right', steps)

# reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
def reverse_positions_x_through_y(password, x, y):
    password = list(password)
    password[x:y+1] = password[x:y+1][::-1]
    return ''.join(password)

# move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
def move_position_x_to_position_y(password, x, y):
    password = list(password)
    char = password.pop(x)
    password.insert(y, char)
    return ''.join(password)


# Read input file and apply transformations
def apply_transformations(password, transformations):
    for transformation in transformations:
        if transformation.startswith('swap position'):
            _, _, x, _, _, y = transformation.split()
            password = swap_x_y(password, int(x), int(y))
        elif transformation.startswith('swap letter'):
            _, _, x, _, _, y = transformation.split()
            password = swap_letter_x_y(password, x, y)
        elif transformation.startswith('rotate left') or transformation.startswith('rotate right'):
            _, direction, steps, _ = transformation.split()
            password = rotate_left_right_x_steps(password, direction, int(steps))
        elif transformation.startswith('rotate based on position of letter'):
            _, _, _, _, _, _, letter = transformation.split()
            password = rotate_based_on_position(password, letter)
        elif transformation.startswith('reverse positions'):
            _, _, x, _, y = transformation.split()
            password = reverse_positions_x_through_y(password, int(x), int(y))
        elif transformation.startswith('move position'):
            _, _, x, _, _, y = transformation.split()
            password = move_position_x_to_position_y(password, int(x), int(y))
    return password

def apply_reverse_transformations(password, transformations):
    for transformation in transformations:
        if transformation.startswith('swap position'):
            _, _, x, _, _, y = transformation.split()
            password = swap_x_y(password, int(y), int(x))  # Swap back
        elif transformation.startswith('swap letter'):
            _, _, x, _, _, y = transformation.split()
            password = swap_letter_x_y(password, y, x)  # Swap back
        elif transformation.startswith('rotate left'):
            _, direction, steps, _ = transformation.split()
            password = rotate_left_right_x_steps(password, 'right', int(steps))
        elif transformation.startswith('rotate right'):
            _, direction, steps, _ = transformation.split()
            password = rotate_left_right_x_steps(password, 'left', int(steps))
        elif transformation.startswith('rotate based on position of letter'):
            # This is a bit tricky to reverse, we need to find the original index of the letter before rotation
            _, _, _, _, _, _, letter = transformation.split()
            # We can try all possible rotations and see which one results in the current password
            for i in range(len(password)):
                if rotate_based_on_position(rotate_left_right_x_steps(password, 'left', i), letter) == password:
                    password = rotate_left_right_x_steps(password, 'left', i)
                    break
        elif transformation.startswith('reverse positions'):
            _, _, x, _, y = transformation.split()
            password = reverse_positions_x_through_y(password, int(x), int(y))
        elif transformation.startswith('move position'):
            _, _, x, _, _, y = transformation.split()
            password = move_position_x_to_position_y(password, int(y), int(x))
    return password

def main(input_file):
    with open(input_file) as f:
        transformations = f.read().strip().split('\n')
    
    # Part 1: Scramble password
    initial_password = 'abcdefgh'
    final_password = apply_transformations(initial_password, transformations)
    print(f'Part 1: Scrambled password - {final_password}')

    # Part 2: Unscramble password
    scrambled_password = 'fbgdceah'
    # To unscramble, we can reverse the transformations and apply the inverse of each transformation
    inverse_transformations = transformations[::-1]
    unscrambled_password = apply_reverse_transformations(scrambled_password, inverse_transformations)
    print(f'Part 2: Unscrambled password - {unscrambled_password}')

# Unittests
class TestFundamentals(unittest.TestCase):
    def test_swap_x_y(self):
        self.assertEqual(swap_x_y('abcde', 4, 0), 'ebcda')

    def test_swap_letter_x_y(self):
        self.assertEqual(swap_letter_x_y('ebcda', 'd', 'b'), 'edcba')

    def test_rotate_left_right_x_steps(self):
        self.assertEqual(rotate_left_right_x_steps('edcba', 'left', 1), 'dcbae')
        self.assertEqual(rotate_left_right_x_steps('dcbae', 'right', 1), 'edcba')
   
    def test_rotate_based_on_position(self):
        self.assertEqual(rotate_based_on_position('abdec', 'b'), 'ecabd')
   
    def test_reverse_positions_x_through_y(self):
        self.assertEqual(reverse_positions_x_through_y('edcba', 0, 4), 'abcde')
    
    def test_move_position_x_to_position_y(self):
        self.assertEqual(move_position_x_to_position_y('bcdea', 1, 4), 'bdeac')


if __name__ == '__main__':
    # Get arguments and see if we are running unittests or the main function
    # Arguments: input_file, test
    input_file = "input.txt"
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            unittest.main()
        elif sys.argv[1] == 'input_file' and len(sys.argv) > 2:
            input_file = sys.argv[2]
    main(input_file)