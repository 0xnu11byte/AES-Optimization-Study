import random

def bytes_to_bits(byte_list):
    return [((b >> i) & 1) for b in byte_list for i in reversed(range(8))]

def hamming_distance(a, b):
    bits_a = bytes_to_bits(a)
    bits_b = bytes_to_bits(b)
    return sum(x != y for x, y in zip(bits_a, bits_b))

def flip_bit(byte_list, bit_index):
    byte_list = byte_list[:]
    byte_pos = bit_index // 8
    bit_pos = 7 - (bit_index % 8)
    byte_list[byte_pos] ^= (1 << bit_pos)
    return byte_list

def test_avalanche_effect(aes_func, original_key, flip_target='key', trials=10):
    total_bit_diff = 0
    for t in range(trials):
        plaintext = [random.randint(0, 255) for _ in range(16)]
        key1 = original_key[:]  # Always use the unmodified key
        key2 = key1[:]

        if flip_target == 'key':
            key2 = flip_bit(key2, random.randint(0, 127))
        elif flip_target == 'plaintext':
            plaintext2 = flip_bit(plaintext[:], random.randint(0, 127))
        else:
            raise ValueError("flip_target must be 'key' or 'plaintext'")

        cipher1 = aes_func(plaintext, key1)
        cipher2 = aes_func(plaintext if flip_target == 'key' else plaintext2, key2 if flip_target == 'key' else key1)
        bit_diff = hamming_distance(cipher1, cipher2)
        total_bit_diff += bit_diff
        print(f"Trial {t+1}: {bit_diff} bits changed out of 128")

    avg = total_bit_diff / trials
    print(f"\nAverage bit difference: {avg:.2f} / 128 bits ({avg / 128 * 100:.2f}%)")

    if avg >= 60:
        print("✅ Strong avalanche effect: Bit diffusion is excellent")
    elif avg >= 50:
        print("⚠️ Moderate avalanche effect: Acceptable but could be stronger")
    else:
        print("❌ Weak avalanche effect: Cipher may be leaking structure or has poor diffusion")


# ---------------------
# Plug in your AES function
# ---------------------
if __name__ == "__main__":
    from aes128 import aes_encrypt
    fixed_key = [0x2b, 0x7e, 0x15, 0x16,
                 0x28, 0xae, 0xd2, 0xa6,
                 0xab, 0xf7, 0x15, 0x88,
                 0x09, 0xcf, 0x4f, 0x3c]

    print("Testing Avalanche Effect with bit flip in plaintext:")
    test_avalanche_effect(aes_encrypt, fixed_key, flip_target='plaintext', trials=10)

    print("\nTesting Avalanche Effect with bit flip in key:")
    test_avalanche_effect(aes_encrypt, fixed_key, flip_target='key', trials=10)
