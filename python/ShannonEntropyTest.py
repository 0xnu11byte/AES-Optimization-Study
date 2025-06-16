import random
import math
from collections import Counter

# --- Entropy Calculation ---
def calculate_entropy(byte_data):
    count = Counter(byte_data)
    total = len(byte_data)
    entropy = -sum((freq / total) * math.log2(freq / total) for freq in count.values())
    return entropy

# --- AES Entropy Tester ---
def test_aes_entropy(aes_encrypt, key, trials=1000):
    ciphertext_bytes = []

    for _ in range(trials):
        plaintext = [random.randint(0, 255) for _ in range(16)]
        ciphertext = aes_encrypt(plaintext, key)
        ciphertext_bytes.extend(ciphertext)

    entropy = calculate_entropy(ciphertext_bytes)
    print(f"Total bytes: {len(ciphertext_bytes)}")
    print(f"Shannon entropy: {entropy:.4f} bits/byte")
    print("Max possible entropy for 8-bit data: 8.0000 bits/byte")

    if entropy >= 7.99:
        print("✅ High entropy: Ciphertext appears strongly random")
    elif entropy >= 7.8:
        print("⚠️ Slightly low entropy: Could be due to weak S-Box or round function")
    else:
        print("❌ Low entropy: Potential structural leakage or poor diffusion")


# --- Example usage ---
if __name__ == "__main__":
    from aes128 import aes_encrypt

    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]

    test_aes_entropy(aes_encrypt, key, trials=1000)
