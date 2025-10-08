"""
Integrated workflow for file encryption/decryption with QR code generation and steganographic key hiding.
"""
import tempfile
import os
from encryptor import encrypt_file, decrypt_file
from qr_generator import generate_qr_with_hidden_key, read_qr_with_extracted_key


def file_to_qr_with_hidden_key(input_file_path, qr_output_path, password):
    """
    Complete workflow: Encrypt file and generate QR code with hidden password.
    
    Args:
        input_file_path (str): Path to the file to encrypt
        qr_output_path (str): Path where the QR code image will be saved
        password (str): Password for encryption (will be hidden in QR)
    
    Returns:
        str: Path to the generated QR code image
    """
    # Create temporary file for encrypted data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as temp_enc_file:
        temp_enc_path = temp_enc_file.name
    
    try:
        # Step 1: Encrypt the file
        print(f"Encrypting {input_file_path}...")
        encrypt_file(input_file_path, temp_enc_path, password)
        
        # Step 2: Read encrypted data
        with open(temp_enc_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Step 3: Generate QR code with encrypted data and hidden password
        print(f"Generating QR code with hidden key...")
        qr_path = generate_qr_with_hidden_key(encrypted_data, password, qr_output_path)
        
        print(f"QR code generated successfully: {qr_path}")
        return qr_path
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_enc_path):
            os.unlink(temp_enc_path)


def qr_to_file_with_extracted_key(qr_image_path, output_file_path):
    """
    Complete workflow: Extract encrypted data and password from QR, then decrypt file.
    
    Args:
        qr_image_path (str): Path to the QR code image
        output_file_path (str): Path where the decrypted file will be saved
    
    Returns:
        str: Path to the decrypted file
    """
    # Step 1: Extract encrypted data and password from QR
    print(f"Reading QR code and extracting hidden key...")
    encrypted_data, password = read_qr_with_extracted_key(qr_image_path)
    
    # Create temporary file for encrypted data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as temp_enc_file:
        temp_enc_path = temp_enc_file.name
    
    try:
        # Step 2: Write encrypted data to temporary file
        with open(temp_enc_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Step 3: Decrypt the file
        print(f"Decrypting file...")
        decrypt_file(temp_enc_path, output_file_path, password)
        
        print(f"File decrypted successfully: {output_file_path}")
        return output_file_path
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_enc_path):
            os.unlink(temp_enc_path)


def get_file_info_from_qr(qr_image_path):
    """
    Extract and display information about the encrypted file in QR code without decrypting.
    
    Args:
        qr_image_path (str): Path to the QR code image
    
    Returns:
        dict: Information about the encrypted file
    """
    try:
        encrypted_data, password = read_qr_with_extracted_key(qr_image_path)
        
        # Parse encrypted file structure (salt + nonce + tag + ciphertext)
        SALT_SIZE = 16
        NONCE_SIZE = 12
        TAG_SIZE = 16
        
        salt = encrypted_data[:SALT_SIZE]
        nonce = encrypted_data[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
        tag = encrypted_data[SALT_SIZE+NONCE_SIZE:SALT_SIZE+NONCE_SIZE+TAG_SIZE]
        ciphertext = encrypted_data[SALT_SIZE+NONCE_SIZE+TAG_SIZE:]
        
        info = {
            'encrypted_size': len(encrypted_data),
            'ciphertext_size': len(ciphertext),
            'salt_hex': salt.hex(),
            'nonce_hex': nonce.hex(),
            'tag_hex': tag.hex(),
            'has_hidden_password': True,
            'password_length': len(password)
        }
        
        return info
        
    except Exception as e:
        return {'error': str(e)}
