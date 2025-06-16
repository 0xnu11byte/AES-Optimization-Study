import random

def hamming_distance_bytes(a, b):
    return sum(bin(x ^ y).count('1') for x, y in zip(a, b))

def test_differential_uniformity(aes_encrypt, key, trials=1000, diff_pos=0):
    distances = []

    for _ in range(trials):
        p1 = [random.randint(0, 255) for _ in range(16)]
        p2 = p1[:]
        p2[diff_pos] ^= 0x01  # Flip 1 bit in byte `diff_pos`

        c1 = aes_encrypt(p1, key)
        c2 = aes_encrypt(p2, key)

        dist = hamming_distance_bytes(c1, c2)
        distances.append(dist)

    avg = sum(distances) / len(distances)
    print(f"Average Hamming distance in ciphertexts: {avg:.2f} bits")
    print("Expected: ~64 bits for good diffusion")

    if avg < 50:
        print("⚠️ Weak diffusion — vulnerable to differential cryptanalysis")
    else:
        print("✅ Good diffusion — resistant to differential cryptanalysis")

if __name__ == "__main__":
    from aes128 import aes_encrypt

    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]

    print("\n== Differential Cryptanalysis Test ==")
    test_differential_uniformity(aes_encrypt, key, trials=1000, diff_pos=0)
