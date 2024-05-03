# Filename: m3p1.py
# Author: Chasham Teja
# Course: ITSC203
"""Details: Generate a non-repeating sequence of either 4 or 8 bytes. You can use any combination of alphanumeric
and punctuation characters"""
"""Resources:
https://www.w3schools.com/python/default.asp"""

import random
import string

# Function to generate a random sequence of characters
def generate_sequence(length):
    characters = string.ascii_letters + string.digits + r'?/:;()!_'
    sequence = ''
    for _ in range(length):
        sequence += random.choice(characters)
    return sequence

# Main program
def main():
    print("Welcome to the Random Sequence Generator!")

    # Get the length of the sequence from the user
    sequence_length = int(input("Enter a sequence length (between 100 and 1024): "))
    if sequence_length < 100 or sequence_length > 1024:
        print("Oops! Sequence length not good. Enter between 100 and 1024.")
        return

    # Get the address size (4 or 8 bytes) from the user
    address_size = int(input("Enter address size (4 or 8): "))
    if address_size not in [4, 8]:
        print("Oops! Address size not right. Please enter 4 or 8.")
        return

    # Generate a random sequence of characters
    random_sequence = generate_sequence(sequence_length)

    print("\n---------------------------------------------")
    print(f"Here is your random sequence of length {sequence_length}:")
    print("---------------------------------------------")
    print(random_sequence)

    # Ask the user to choose to enter a sample string or auto choose
    choice = input("\nPress 'E' to enter a sample string or 'A' to auto choose: ").lower()

    # If the user chooses to enter a sample string
    if choice == 'e':
        sample_string = input("Please enter your sample string: ")
        offset = random_sequence.find(sample_string)
        if offset != -1:
            print(f"Your sample '{sample_string}' starts at position {offset + 1}.")
            count = random_sequence.count(sample_string)
            print(f"Your pattern was found {count} time(s).")
        else:
            print("Sorry, your sample string was not found in the generated sequence.")
    # If the user chooses to auto choose
    elif choice == 'a':
        random_offset = random.randint(0, len(random_sequence) - address_size)
        sample_string = random_sequence[random_offset:random_offset + address_size]
        print(f"Auto-chosen sample: {sample_string}")
        count = random_sequence.count(sample_string)
        print(f"Your pattern was found {count} time(s).")

# Run the main program
if __name__ == "__main__":
    main()
