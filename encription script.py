import numpy as np

def hill_cipher_encrypt(plaintext, key_matrix):
    modulus = 26
    n = key_matrix.shape[0]

    plaintext = plaintext.upper().replace(" ", "")
    plaintext_numbers = [ord(char) - ord('A') for char in plaintext]

    while len(plaintext_numbers) % n != 0:
        plaintext_numbers.append(ord('X') - ord('A'))

    ciphertext_numbers = []
    for i in range(0, len(plaintext_numbers), n):
        block = plaintext_numbers[i:i + n]
        block_vector = np.array(block).reshape(-1, 1)
        encrypted_block = np.dot(key_matrix, block_vector) % modulus
        ciphertext_numbers.extend(encrypted_block.flatten())
    

    ciphertext = ''.join(chr(num + ord('A')) for num in ciphertext_numbers)
    return ciphertext

def input_matrix(n):
    print(f"Enter the {n}x{n} key matrix row-wise:")
    key_matrix = []
    for i in range(n):
        row = input().strip().split()
        key_matrix.append([int(num) for num in row])
    return np.array(key_matrix)

# Example usage
n = int(input("Enter the size of the key matrix : "))
key_matrix = input_matrix(n)
plaintext = input("Enter the plaintext: ")

ciphertext = hill_cipher_encrypt(plaintext, key_matrix)
print(f"Encrypted: {ciphertext}")
