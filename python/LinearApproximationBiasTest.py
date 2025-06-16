import random

def test_linear_approximation_bias(aes_encrypt, key, trials=10000):
    biased_count = 0

    for _ in range(trials):
        plaintext = [random.randint(0, 255) for _ in range(16)]
        ciphertext = aes_encrypt(plaintext, key)

        # Simple linear approximation:
        # (P[0] xor P[5] xor C[2]) should be 0 half of the time for ideal cipher
        p_bit = (plaintext[0] ^ plaintext[5]) & 1
        c_bit = (ciphertext[2]) & 1
        parity = p_bit ^ c_bit

        if parity == 0:
            biased_count += 1

    bias = abs((biased_count / trials) - 0.5)
    print(f"Linear bias: {bias:.5f}")
    print("Ideal bias ≈ 0.0 (i.e., 50% parity == 0)")

    if bias > 0.01:
        print("⚠️ Potential bias detected (not secure)")
    else:
        print("✅ No significant bias (secure)")

if __name__ == "__main__":
    from aes128 import aes_encrypt

    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]

    print("== Linear Cryptanalysis Test ==")
    test_linear_approximation_bias(aes_encrypt, key, trials=10000)
