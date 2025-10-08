import argparse
from file_qr_workflow import file_to_qr_with_hidden_key


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt a file and generate a QR with a hidden password")
    parser.add_argument("input", help="Path to the input file to encrypt")
    parser.add_argument("qr_output", help="Path to save the generated QR image (e.g., out.png)")
    parser.add_argument("password", help="Password to encrypt the file (will be hidden in QR)")
    args = parser.parse_args()

    print(f"Encrypting '{args.input}' and generating QR '{args.qr_output}'...")
    qr_path = file_to_qr_with_hidden_key(args.input, args.qr_output, args.password)
    print(f"Done. QR saved to: {qr_path}")


if __name__ == "__main__":
    main()


