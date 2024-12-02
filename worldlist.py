"""
WorldList Generator
Author: IIBladeII
GitHub: https://github.com/IIBladeII
"""

import itertools
import os
import time
from typing import Callable, Any

def get_numeric_input(message: str, type_: Callable = int, 
                     condition: Callable[[Any], bool] = lambda x: x > 0,
                     error_message: str = "Please enter a valid value.") -> Any:
    while True:
        try:
            value = type_(input(message))
            if condition(value):
                return value
            print(error_message)
        except ValueError:
            print(f"Please enter a valid value of type {type_.__name__}.")

def validate_characters(text: str) -> str:
    """Validates and cleans the input character string."""
    if not text:
        raise ValueError("The character list cannot be empty.")
    # Remove spaces and duplicate characters
    characters = ''.join(dict.fromkeys(text.replace(' ', '')))
    return characters

def create_filename(name: str) -> str:
    """Creates a valid filename with .txt extension"""
    if not name.endswith('.txt'):
        name += '.txt'
    return name

def show_progress(current: int, total: int, prefix: str = '', bar_length: int = 50):
    """Shows a progress bar in the console."""
    percentage = float(current) * 100 / total
    filled = int(bar_length * current / total)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(f'\r{prefix} |{bar}| {percentage:.1f}% Complete', end='')
    if current == total:
        print()

def calculate_estimated_size(num_chars: int, length: int) -> int:
    """Calculates the estimated size of the list in bytes."""
    word_size = length + 1  # +1 for newline character
    total_words = num_chars ** length
    return total_words * word_size

def generate_wordlist():
    print("\n=== Word List Generator ===\n")
    
    try:
        # Request word length
        word_length = get_numeric_input(
            "How many characters do you want in each word? ",
            error_message="Length must be greater than 0."
        )

        # Request characters
        while True:
            try:
                characters = validate_characters(input("Enter the characters for the list (no spaces): "))
                break
            except ValueError as e:
                print(str(e))

        # Calculate and show estimates
        num_words = len(characters) ** word_length
        size_mb = calculate_estimated_size(len(characters), word_length) / (1024 * 1024)
        
        print(f"\nEstimated statistics:")
        print(f"- Total words to be generated: {num_words:,}")
        print(f"- Approximate file size: {size_mb:.1f} MB")
        
        if size_mb > 100:  # Warning for large files
            continue_ = input("\nWARNING: The file will be very large. Continue? (y/n): ").lower()
            if continue_ != 'y':
                print("Operation cancelled by user.")
                return

        # Request filename
        while True:
            try:
                filename = create_filename(input("\nFilename to save (e.g., wordlist.txt): "))
                file_path = os.path.abspath(filename)
                
                # Check if file already exists
                if os.path.exists(file_path):
                    overwrite = input("File already exists. Overwrite? (y/n): ").lower()
                    if overwrite != 'y':
                        continue
                break
            except Exception as e:
                print(f"Error creating file: {str(e)}")

        print("\nGenerating word list...")
        start = time.time()
        
        # Generate and save words with progress indicator
        with open(file_path, 'w') as file:
            total_words = len(characters) ** word_length
            for i, combination in enumerate(itertools.product(characters, repeat=word_length), 1):
                file.write(''.join(combination) + '\n')
                if i % max(1, total_words // 100) == 0:  # Update progress every 1%
                    show_progress(i, total_words, 'Progress:')

        total_time = time.time() - start
        
        print(f"\nCompleted!")
        print(f"Word list saved to: {file_path}")
        print(f"Total words generated: {num_words:,}")
        print(f"Execution time: {total_time:.1f} seconds")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")

if __name__ == "__main__":
    generate_wordlist()
