# Secure File Sharing System

A Python-based secure communication system designed for protected file transfer using XOR-Shift chaotic-key encryption and entropy-based QR steganography. The project focuses on combining cryptographic randomness with covert QR-based data embedding to improve confidentiality and secure transmission.

## Core Features

* XOR-Shift chaotic key generation for encryption
* Entropy-based QR steganography for hidden payload embedding
* Secure file encryption and decryption workflow
* QR code generation for encoded file transfer
* Lightweight and efficient implementation for real-world usage

## Workflow

1. Select a file for secure transfer.
2. Generate chaotic encryption keys using the XOR-Shift algorithm.
3. Encrypt the file and embed the encrypted payload into QR structures using entropy-driven steganographic techniques.
4. Share the generated QR code securely.
5. Recipient extracts and decrypts the payload using the corresponding key.

## Technical Highlights

* Chaotic-system-based cryptographic key generation
* Entropy optimization for secure QR embedding
* Resistance against statistical extraction attacks
* Optimized balance between security, randomness, and QR readability

## Requirements

* Python 3.7+
* Dependencies listed in `requirements.txt`

## Installation

```bash id="izytjc"
pip install -r requirements.txt
```

## Applications

* Secure document exchange
* Covert communication systems
* Research in cryptography and steganography
* QR-based secure data transmission
