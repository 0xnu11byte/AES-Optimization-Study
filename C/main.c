#include <stdio.h>

int main() {
    uint8_t key[16] = { /* 128-bit key */ };
    uint8_t plaintext[16] = { /* 128-bit block */ };
    uint8_t ciphertext[16];
    uint8_t roundKeys[176]; // 11 * 16 bytes

    KeyExpansion(roundKeys, key);
    Cipher(plaintext, roundKeys, ciphertext);

    printf("Encrypted: ");
    for (int i = 0; i < 16; ++i) printf("%02x ", ciphertext[i]);
    return 0;
}