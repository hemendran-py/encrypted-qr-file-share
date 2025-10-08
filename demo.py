#!/usr/bin/env python3
"""
Demo script to showcase the secure file sharing with steganographic QR codes.
"""
import os
from file_qr_workflow import file_to_qr_with_hidden_key, qr_to_file_with_extracted_key, get_file_info_from_qr


def demo_workflow():
    """Demonstrate the complete file-to-QR-to-file workflow."""
    
    # Test file content
    test_content = "This is a secret message that will be encrypted and hidden in a QR code!"
    test_file = "demo_secret.txt"
    qr_file = "secret_qr.png"
    output_file = "decrypted_secret.txt"
    password = "MySecretPassword123"
    
    print("=== Secure File Sharing Demo ===")
    print()
    
    # Step 1: Create test file
    print("1. Creating test file...")
    with open(test_file, 'w') as f:
        f.write(test_content)
    print(f"   Created: {test_file}")
    print()
    
    # Step 2: Convert file to QR with hidden password
    print("2. Encrypting file and generating QR code with hidden password...")
    try:
        file_to_qr_with_hidden_key(test_file, qr_file, password)
        print(f"   Success! QR code generated: {qr_file}")
        print(f"   - File encrypted with AES-GCM")
        print(f"   - Password hidden steganographically in QR image")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 3: Get info about the QR code
    print("3. Getting information from QR code...")
    try:
        info = get_file_info_from_qr(qr_file)
        if 'error' not in info:
            print(f"   Encrypted file size: {info['encrypted_size']} bytes")
            print(f"   Password hidden: {info['has_hidden_password']}")
            print(f"   Password length: {info['password_length']} characters")
        else:
            print(f"   Error getting info: {info['error']}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 4: Extract and decrypt file from QR
    print("4. Extracting and decrypting file from QR code...")
    try:
        qr_to_file_with_extracted_key(qr_file, output_file)
        print(f"   Success! File decrypted: {output_file}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 5: Verify the result
    print("5. Verifying decrypted content...")
    try:
        with open(output_file, 'r') as f:
            decrypted_content = f.read()
        
        if decrypted_content == test_content:
            print("   ✓ Content matches perfectly!")
            print(f"   Original:  {test_content}")
            print(f"   Decrypted: {decrypted_content}")
        else:
            print("   ✗ Content mismatch!")
        print()
    except Exception as e:
        print(f"   Error: {e}")
    
    # Cleanup
    
    
    print()
    print("=== Demo Complete ===")
    print(f"Your QR code with hidden password is saved as: {qr_file}")
    print("You can now share this QR code securely!")


if __name__ == "__main__":
    demo_workflow()
