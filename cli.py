import argparse
from encryptor import encrypt_file, decrypt_file
from qr_generator import generate_qr_code
from file_qr_workflow import file_to_qr_with_hidden_key, qr_to_file_with_extracted_key, get_file_info_from_qr


def main():
    parser = argparse.ArgumentParser(description='Secure File Sharing CLI - Pure XOR with Chaotic Key Generation')
    subparsers = parser.add_subparsers(dest='command')

    # Encrypt file and create QR code with hidden password
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file and create QR code with hidden password')
    encrypt_parser.add_argument('input', help='Input file path to encrypt')
    encrypt_parser.add_argument('output', help='Output QR code image path (.png)')
    encrypt_parser.add_argument('password', help='Password for encryption (will be hidden in QR)')

    # Decrypt file from QR code
    decrypt_parser = subparsers.add_parser('decrypt', help='Extract and decrypt file from QR code')
    decrypt_parser.add_argument('qr_image', help='Input QR code image path')
    decrypt_parser.add_argument('output', help='Output decrypted file path')


    args = parser.parse_args()

    if args.command == 'encrypt':
        print(f'Encrypting {args.input} and creating QR code: {args.output}...')
        try:
            file_to_qr_with_hidden_key(args.input, args.output, args.password)
            print(f'✅ Success! File encrypted and QR code created: {args.output}')
            print(f'   Password is hidden in the QR code image.')
        except Exception as e:
            print(f'❌ Encryption failed: {e}')
    elif args.command == 'decrypt':
        print(f'Extracting and decrypting file from QR code: {args.qr_image}...')
        try:
            qr_to_file_with_extracted_key(args.qr_image, args.output)
            print(f'✅ Success! File decrypted: {args.output}')
            print(f'   Password was automatically extracted from QR code.')
        except Exception as e:
            print(f'❌ Decryption failed: {e}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 