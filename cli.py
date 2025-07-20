import argparse


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
        print('Encrypting file...')
        # Call encrypt_file here
    elif args.command == 'decrypt':
        print('Decrypting file...')
        # Call decrypt_file here
    elif args.command == 'qr':
        print('Generating QR code...')
        # Call generate_qr_code here
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 