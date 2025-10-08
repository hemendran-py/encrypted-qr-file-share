import qrcode
import base64
from PIL import Image
import io
from steganography import hide_data_in_image, extract_data_from_image


def generate_qr_code(data, output_path):
    """Generate a QR code with the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path


def generate_qr_with_hidden_key(encrypted_data, password, output_path):
    """Generate QR code containing encrypted data with password hidden steganographically."""
    # Convert encrypted data to base64 for QR encoding
    encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    
    # Generate QR code with encrypted data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_b64)
    qr.make(fit=True)
    
    # Create QR image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Hide the password steganographically in the QR image
    img_with_hidden_key = hide_data_in_image(img, password.encode('utf-8'))
    img_with_hidden_key.save(output_path)
    
    return output_path


def read_qr_code(image_path):
    """Read QR code and return the data."""
    from pyzbar import pyzbar
    
    # Load image
    img = Image.open(image_path)
    
    # Decode QR code
    qr_codes = pyzbar.decode(img)
    
    if qr_codes:
        # Return the first QR code data
        return qr_codes[0].data.decode('utf-8')
    else:
        raise ValueError("No QR code found in the image")


def read_qr_with_extracted_key(image_path):
    """Read QR code and extract both the encrypted data and hidden password."""
    from pyzbar import pyzbar
    
    # Load image
    img = Image.open(image_path)
    
    # Extract hidden password
    hidden_password = extract_data_from_image(img).decode('utf-8')
    
    # Decode QR code to get encrypted data
    qr_codes = pyzbar.decode(img)
    
    if qr_codes:
        encrypted_b64 = qr_codes[0].data.decode('utf-8')
        encrypted_data = base64.b64decode(encrypted_b64)
        return encrypted_data, hidden_password
    else:
        raise ValueError("No QR code found in the image") 