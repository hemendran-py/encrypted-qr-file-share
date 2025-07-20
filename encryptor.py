from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# Constants
SALT_SIZE = 16  # 128-bit salt
NONCE_SIZE = 12  # 96-bit nonce for AES-GCM
KEY_SIZE = 32  # 256-bit key
ITERATIONS = 100_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a secret key from the password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_file(input_path, output_path, password):
    """Encrypts a file using AES-GCM and writes salt+nonce+ciphertext+tag to output_path."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    nonce = os.urandom(NONCE_SIZE)

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    with open(output_path, 'wb') as f:
        f.write(salt + nonce + tag + ciphertext)


def decrypt_file(input_path, output_path, password):
    """Decrypts a file using AES-GCM and writes the plaintext to output_path."""
    with open(input_path, 'rb') as f:
        data = f.read()
    salt = data[:SALT_SIZE]
    nonce = data[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
    tag = data[SALT_SIZE+NONCE_SIZE:SALT_SIZE+NONCE_SIZE+16]
    ciphertext = data[SALT_SIZE+NONCE_SIZE+16:]

    key = derive_key(password, salt)
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag),
        backend=default_backend()
    ).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_path, 'wb') as f:
        f.write(plaintext) 