import itertools
import string
import time
import sys

# Define a wider character set to include uppercase, lowercase, digits, and symbols
charset = string.ascii_letters + string.digits + "!@#"

# Function to simulate checking if the guess is correct
def is_correct_password(guess, actual_password):
    return guess == actual_password

# Brute‑force function to try all possible combinations
def brute_force_password(charset, actual_password):
    # 1) Ensure we can actually generate the target password…
    missing = set(actual_password) - set(charset)
    if missing:
        print(f"❌ ERROR: charset is missing these characters: {missing}")
        sys.exit(1)
    
    max_length = len(actual_password)
    print(f"🔍 Using charset: {charset}")
    print(f"🔍 Target password length: {max_length}\n")
    
    attempts = 0
    start_time = time.time()

    # Try passwords of increasing length up to exactly the length we need
    for length in range(1, max_length + 1):
        print(f"Trying length {length}…")
        for guess_tuple in itertools.product(charset, repeat=length):
            guess = ''.join(guess_tuple)
            attempts += 1

            if attempts % 100_000 == 0:
                print(f"  Checked {attempts} guesses so far… latest: {guess}")

            if is_correct_password(guess, actual_password):
                elapsed = time.time() - start_time
                print(f"\n✅ Password found: {guess}")
                print(f"🔁 Attempts: {attempts}")
                print(f"⏱️ Time taken: {elapsed:.4f} seconds")
                return guess

    elapsed = time.time() - start_time
    print("\n❌ Password not found.")
    print(f"🔁 Total attempts: {attempts}")
    print(f"⏱️ Time taken: {elapsed:.4f} seconds")
    return None

# ===========================
# 🔧 Test the brute‑force program
# ===========================
if __name__ == "__main__":
    correct_password = "JO32"   # short for fast testing
    brute_force_password(charset, correct_password)
