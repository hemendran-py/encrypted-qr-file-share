import struct
import hashlib


# Constants for chaotic key generation
LOGISTIC_R = 3.99  # Chaos parameter for Logistic Map


def password_to_seed(password: str) -> float:
    """Convert password to numerical seed using hash."""
    # Create a hash of the password
    password_hash = hashlib.sha256(password.encode()).digest()
    
    # Convert first 8 bytes to a float between 0 and 1
    seed_bytes = password_hash[:8]
    seed_int = struct.unpack('>Q', seed_bytes)[0]  # Big-endian unsigned long long
    seed = (seed_int % 1000000) / 1000000.0  # Normalize to [0, 1)
    
    return seed


def generate_chaotic_key(password: str, key_length: int = 256) -> bytes:
    """
    Generate a chaotic key using the Logistic Map formula.
    
    Logistic Map: x_{n+1} = r * x_n * (1 - x_n)
    where r = 3.99 for chaotic behavior.
    
    Args:
        password (str): Password to generate seed from
        key_length (int): Length of key in bytes (default 256)
    
    Returns:
        bytes: Chaotic key of specified length
    """
    # Convert password to numerical seed
    x = password_to_seed(password)
    
    # Generate key using Logistic Map
    key = bytearray()
    
    for i in range(key_length):
        # Apply Logistic Map formula: x_{n+1} = r * x_n * (1 - x_n)
        x = LOGISTIC_R * x * (1 - x)
        
        # Convert floating point to byte
        # Scale x to [0, 255] and round to integer
        byte_value = int(x * 255) & 0xFF
        key.append(byte_value)
    
    return bytes(key)


def encrypt_file(input_path, output_path, password):
    """
    Encrypts a file using pure XOR with chaotic key generation.
    Uses key repetition with modulo indexing for files larger than key.
    """
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    
    # Generate chaotic key (256 bytes)
    key = generate_chaotic_key(password, 256)
    
    # XOR encryption with key repetition using modulo indexing
    ciphertext = bytearray()
    for i, byte in enumerate(plaintext):
        key_byte = key[i % len(key)]  # Modulo indexing for key repetition
        encrypted_byte = byte ^ key_byte
        ciphertext.append(encrypted_byte)
    
    with open(output_path, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(input_path, output_path, password):
    """
    Decrypts a file using pure XOR with chaotic key generation.
    XOR is symmetric, so decryption is the same as encryption.
    """
    with open(input_path, 'rb') as f:
        ciphertext = f.read()
    
    # Generate same chaotic key (256 bytes)
    key = generate_chaotic_key(password, 256)
    
    # XOR decryption with key repetition using modulo indexing
    plaintext = bytearray()
    for i, byte in enumerate(ciphertext):
        key_byte = key[i % len(key)]  # Modulo indexing for key repetition
        decrypted_byte = byte ^ key_byte
        plaintext.append(decrypted_byte)
    
    with open(output_path, 'wb') as f:
        f.write(plaintext) 