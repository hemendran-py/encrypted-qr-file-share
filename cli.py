import argparse
from encryptor import encrypt_file, decrypt_file
from qr_generator import generate_qr_code


def main():
    parser = argparse.ArgumentParser(description='Secure File Sharing CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('input', help='Input file path')
    encrypt_parser.add_argument('output', help='Output encrypted file path')
    encrypt_parser.add_argument('password', help='Password for encryption')

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('input', help='Input encrypted file path')
    decrypt_parser.add_argument('output', help='Output decrypted file path')
    decrypt_parser.add_argument('password', help='Password for decryption')

    # QR code command
    qr_parser = subparsers.add_parser('qr', help='Generate QR code for data')
    qr_parser.add_argument('data', help='Data to encode in QR code')
    qr_parser.add_argument('output', help='Output QR code image path')

    args = parser.parse_args()

    if args.command == 'encrypt':
        print(f'Encrypting {args.input} to {args.output}...')
        try:
            encrypt_file(args.input, args.output, args.password)
            print('Encryption successful.')
        except Exception as e:
            print(f'Encryption failed: {e}')
    elif args.command == 'decrypt':
        print(f'Decrypting {args.input} to {args.output}...')
        try:
            decrypt_file(args.input, args.output, args.password)
            print('Decryption successful.')
        except Exception as e:
            print(f'Decryption failed: {e}')
    elif args.command == 'qr':
        print(f'Generating QR code to {args.output}...')
        try:
            generate_qr_code(args.data, args.output)
            print('QR code generated successfully.')
        except Exception as e:
            print(f'QR code generation failed: {e}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 