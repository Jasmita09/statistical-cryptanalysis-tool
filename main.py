import string
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

POSSIBLE_CHARS = "".join(chr(i) for i in range(32, 127)) 
NUM_CHARS = len(POSSIBLE_CHARS)

try:
    freq_df = pd.read_csv("english_frequencies.csv")
    freq_df["Letter"] = freq_df["Letter"].str.upper()
    ENGLISH_FREQS = freq_df.set_index("Letter")["Frequency"].to_dict()
except FileNotFoundError:
    print("[!] Warning: 'english_frequencies.csv' not found. Auto-crack (Option 4) will use uniform backup.")
    ENGLISH_FREQS = {letter: 4.0 for letter in string.ascii_uppercase}

def shift_message(message, key, mode):
    """
    Encrypts or decrypts a message by shifting characters across the 
    entire printable ASCII space. Punctuation and symbols ARE now encrypted.
    """
    shifted_message = ""
    key = key % NUM_CHARS
    
    for character in message:
        if character in POSSIBLE_CHARS:
            initial_position = POSSIBLE_CHARS.find(character)
            if mode == "encrypt":
                shifted_position = (initial_position + key) % NUM_CHARS
            else:
                shifted_position = (initial_position - key) % NUM_CHARS
            shifted_message += POSSIBLE_CHARS[shifted_position]
        else:
            shifted_message += character
            
    return shifted_message

def clean_text(text: str) -> str:
    return "".join(char.upper() for char in text if char.isalpha())

def get_observed_counts(cleaned_text: str) -> dict:
    counts = Counter(cleaned_text)
    return {letter: counts.get(letter, 0) for letter in string.ascii_uppercase}

def calculate_chi_squared(text: str) -> float:
    cleaned_text = clean_text(text)
    total_letters = len(cleaned_text)
    
    # Need at least 3 letters to perform a valid statistical comparison
    if total_letters < 3:
        return float('nan')  # NaN allows Matplotlib to skip invalid points cleanly
        
    observed_counts = get_observed_counts(cleaned_text)
    
    chi_squared = 0.0
    for letter in string.ascii_uppercase:
        # Compare proportions (percentages) instead of raw counts
        observed_prop = observed_counts[letter] / total_letters
        expected_prop = ENGLISH_FREQS.get(letter, 1.0) / 100.0
        
        chi_squared += ((observed_prop - expected_prop) ** 2) / expected_prop
        
    return chi_squared
    
def auto_crack(encrypted_message):
    results = []
    for key in range(NUM_CHARS):
        decrypted = shift_message(encrypted_message, key, "decrypt")
        score = calculate_chi_squared(decrypted)
        results.append((key, decrypted, score))
    df = pd.DataFrame(results, columns=["Key", "Decrypted Message", "Chi-Squared Score"])
    
    # .idxmin() automatically ignores NaN values
    best_row_idx = df["Chi-Squared Score"].idxmin()
    best_match = df.loc[best_row_idx]
    return best_match["Key"], best_match["Decrypted Message"], df

def plot_scores(df: pd.DataFrame) -> None:
    best_row_idx = df["Chi-Squared Score"].idxmin()
    best_match = df.loc[best_row_idx]
    best_key = best_match["Key"]
    best_score = best_match["Chi-Squared Score"]
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["Key"], df["Chi-Squared Score"], color="#2c3e50", marker='o', label="Candidate Keys")
    plt.plot(best_key, best_score, 'ro', markersize=10, label=f"Predicted Key (Key #{best_key})")
    plt.xlabel("Key Shift")
    plt.ylabel("Chi-Squared Score (Lower is Better)")
    plt.title("Cryptanalysis Statistical Divergence (95-Char Set)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 60)
    print("         EXTENDED ASCII CAESAR CIPHER TOOL (95 KEYS)        ")
    print("=" * 60)
    print("Please choose an option:")
    print(" [1] Encrypt a message")
    print(" [2] Decrypt a message (with a known key)")
    print(" [3] Brute-force crack a message (show all possibilities)")
    print(" [4] Auto-crack using Data Science (Chi-Squared Analysis)")
    print("-" * 60)
    
    choice = input("Enter choice (1, 2, 3, or 4): ").strip()
    
    if choice == "1":
        message = input("\nWhat is the message to encrypt? ")
        key = int(input(f"Enter key (0-{NUM_CHARS - 1}): "))
        encrypted = shift_message(message, key, "encrypt")
        print(f"\n[+] Your encrypted message is: {encrypted}")
        
    elif choice == "2":
        message = input("\nWhat is the message to decrypt? ").strip()
        key = int(input(f"Enter key (0-{NUM_CHARS - 1}): "))
        decrypted = shift_message(message, key, "decrypt")
        print(f"\n[+] Your decrypted message is: {decrypted}")
        
    elif choice == "3":
        message = input("\nWhat is the encrypted message to crack? ")
        input(f"\nPress enter to generate all {NUM_CHARS} key possibilities...\n")
        for key in range(NUM_CHARS):
            decrypted = shift_message(message, key, "decrypt")
            print(f"Key #{key:02d}: {decrypted}")
        print("\nScroll through the options above to find the readable plaintext message.")
        
    elif choice == "4":
        message = input("\nEnter encrypted message to crack: ").strip()
        key, decrypted, df = auto_crack(message)
        print(f"\n[+] Predicted Key: {key}")
        print(f"[+] Decrypted Message: {decrypted}\n")
        plot_scores(df)
    else:
        print("\n[!] Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
