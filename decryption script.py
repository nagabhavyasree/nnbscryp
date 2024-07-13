import numpy as np

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse for {a} under modulus {m}")

def matrix_mod_inverse(matrix, modulus):
    determinant = int(np.round(np.linalg.det(matrix))) % modulus
    determinant_inv = mod_inverse(determinant, modulus)
    
    matrix_modulus_inv = (
        determinant_inv * np.round(determinant * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_modulus_inv

def hill_cipher_decrypt(ciphertext, key_matrix):
    modulus = 26
    n = key_matrix.shape[0]
    
    key_matrix_inv = matrix_mod_inverse(key_matrix, modulus)

    ciphertext = ciphertext.upper().replace(" ", "")
    ciphertext_numbers = [ord(char) - ord('A') for char in ciphertext]

    plaintext_numbers = []
    for i in range(0, len(ciphertext_numbers), n):
        block = ciphertext_numbers[i:i + n]
        block_vector = np.array(block).reshape(-1, 1)
        decrypted_block = np.dot(key_matrix_inv, block_vector) % modulus
        plaintext_numbers.extend(decrypted_block.flatten().astype(int))

    plaintext = ''.join(chr(num + ord('A')) for num in plaintext_numbers)
    return plaintext

def generate_key_matrix(plaintext, ciphertext, n):
    modulus = 26
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = ciphertext.upper().replace(" ", "")

    if len(plaintext) < n * n or len(ciphertext) < n * n:
        raise ValueError(f"Plaintext and ciphertext must each be at least {n*n} characters long for a {n}x{n} matrix")

    plaintext_matrix = np.array([ord(char) - ord('A') for char in plaintext[:n * n]]).reshape(n, n)
    ciphertext_matrix = np.array([ord(char) - ord('A') for char in ciphertext[:n * n]]).reshape(n, n)

    plaintext_matrix_inv = matrix_mod_inverse(plaintext_matrix, modulus)
    key_matrix = np.dot(ciphertext_matrix, plaintext_matrix_inv) % modulus
    return key_matrix

# Prompt user for n
while True:
    try:
        n = int(input("Enter the size of the key matrix : "))
        break
    except ValueError:
        print("Please enter a valid integer.")

# Example usage
plaintext = input("Enter the plaintext: ")
ciphertext = input("Enter the ciphertext: ")

key_matrix = generate_key_matrix(plaintext, ciphertext, n)
print(f"Generated Key Matrix:\n{key_matrix}")

decrypted_text = hill_cipher_decrypt(ciphertext, key_matrix)
print(f"Decrypted: {decrypted_text}")

