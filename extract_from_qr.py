import argparse
from file_qr_workflow import qr_to_file_with_extracted_key
from qr_generator import read_qr_with_extracted_key


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract encrypted data (and hidden key) from a QR. Optionally decrypt to a file.")
    parser.add_argument("qr_image", help="Path to the QR image containing the encrypted data and hidden key")
    parser.add_argument("--save-encrypted", dest="enc_output", help="Path to save the raw encrypted blob (.enc)")
    parser.add_argument("--decrypt-to", dest="dec_output", help="Path to save the decrypted file")
    args = parser.parse_args()

    if not args.enc_output and not args.dec_output:
        parser.error("Provide at least one of --save-encrypted or --decrypt-to")

    if args.enc_output:
        encrypted_data, _ = read_qr_with_extracted_key(args.qr_image)
        with open(args.enc_output, "wb") as f:
            f.write(encrypted_data)
        print(f"Encrypted blob saved to: {args.enc_output}")

    if args.dec_output:
        output_path = qr_to_file_with_extracted_key(args.qr_image, args.dec_output)
        print(f"Decrypted file saved to: {output_path}")


if __name__ == "__main__":
    main()


