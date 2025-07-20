# Secure File Sharing

A Python app for safely sharing sensitive files using AES encryption and QR codes. Encrypt files, generate QR codes for sharing, and allow recipients to decrypt files using a shared password.

## Features
- AES file encryption/decryption
- QR code generation (link or embedded data)
- Optional web server for file hosting
- Password-protected access

## Usage Outline
1. Encrypt a file with a password.
2. Generate a QR code linking to or containing the encrypted file.
3. Share the QR code with the recipient.
4. Recipient scans the QR code and decrypts the file using the password.

## Requirements
- Python 3.7+
- See `requirements.txt` 