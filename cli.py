import argparse
from encryptor import encrypt_file, decrypt_file
from qr_generator import generate_qr_code
from file_qr_workflow import file_to_qr_with_hidden_key, qr_to_file_with_extracted_key, get_file_info_from_qr


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

    # File to QR with hidden key command
    file_to_qr_parser = subparsers.add_parser('file-to-qr', help='Encrypt file and generate QR with hidden password')
    file_to_qr_parser.add_argument('input', help='Input file path to encrypt')
    file_to_qr_parser.add_argument('output', help='Output QR code image path')
    file_to_qr_parser.add_argument('password', help='Password for encryption (will be hidden in QR)')

    # QR to file with extracted key command
    qr_to_file_parser = subparsers.add_parser('qr-to-file', help='Extract and decrypt file from QR with hidden password')
    qr_to_file_parser.add_argument('input', help='Input QR code image path')
    qr_to_file_parser.add_argument('output', help='Output decrypted file path')

    # QR info command
    qr_info_parser = subparsers.add_parser('qr-info', help='Get information about encrypted file in QR code')
    qr_info_parser.add_argument('input', help='Input QR code image path')

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
    elif args.command == 'file-to-qr':
        print(f'Converting {args.input} to QR code with hidden password...')
        try:
            file_to_qr_with_hidden_key(args.input, args.output, args.password)
            print(f'File encrypted and QR code generated: {args.output}')
        except Exception as e:
            print(f'File to QR conversion failed: {e}')
    elif args.command == 'qr-to-file':
        print(f'Extracting and decrypting file from QR code...')
        try:
            qr_to_file_with_extracted_key(args.input, args.output)
            print(f'File extracted and decrypted: {args.output}')
        except Exception as e:
            print(f'QR to file conversion failed: {e}')
    elif args.command == 'qr-info':
        print(f'Getting information from QR code...')
        try:
            info = get_file_info_from_qr(args.input)
            if 'error' in info:
                print(f'Failed to get QR info: {info["error"]}')
            else:
                print(f'QR Code Information:')
                print(f'  Encrypted file size: {info["encrypted_size"]} bytes')
                print(f'  Ciphertext size: {info["ciphertext_size"]} bytes')
                print(f'  Has hidden password: {info["has_hidden_password"]}')
                print(f'  Password length: {info["password_length"]} characters')
                print(f'  Salt: {info["salt_hex"]}')
                print(f'  Nonce: {info["nonce_hex"]}')
        except Exception as e:
            print(f'QR info extraction failed: {e}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 