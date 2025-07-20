from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os


def encrypt_file(input_path, output_path, password):
    """Encrypts a file using AES and writes the encrypted data to output_path."""
    pass


def decrypt_file(input_path, output_path, password):
    """Decrypts a file using AES and writes the decrypted data to output_path."""
    pass 