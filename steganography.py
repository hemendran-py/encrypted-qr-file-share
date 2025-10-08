from PIL import Image
import struct


def hide_data_in_image(image, data):
    """
    Hide data in the least significant bits of an image.
    Uses LSB steganography to embed data invisibly.
    """
    # Convert image to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert data to bytes if it's a string
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Add length prefix to data
    data_length = len(data)
    data_with_length = struct.pack('>I', data_length) + data
    
    # Convert to binary string
    binary_data = ''.join(format(byte, '08b') for byte in data_with_length)
    
    # Get image pixels
    width, height = image.size
    pixels = list(image.getdata())
    
    # Check if image is large enough
    if len(pixels) * 3 < len(binary_data):
        raise ValueError("Image too small to hide the data")
    
    # Hide data in LSB
    data_index = 0
    new_pixels = []
    
    for pixel in pixels:
        r, g, b = pixel
        
        # Modify LSB of each color channel
        if data_index < len(binary_data):
            r = (r & 0xFE) | int(binary_data[data_index])
            data_index += 1
        
        if data_index < len(binary_data):
            g = (g & 0xFE) | int(binary_data[data_index])
            data_index += 1
        
        if data_index < len(binary_data):
            b = (b & 0xFE) | int(binary_data[data_index])
            data_index += 1
        
        new_pixels.append((r, g, b))
    
    # Create new image
    new_image = Image.new('RGB', (width, height))
    new_image.putdata(new_pixels)
    
    return new_image


def extract_data_from_image(image):
    """
    Extract data hidden in the least significant bits of an image.
    """
    # Convert image to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get image pixels
    pixels = list(image.getdata())
    
    # Extract binary data from LSB
    binary_data = ''
    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)
    
    # Convert binary to bytes
    data_bytes = bytearray()
    for i in range(0, len(binary_data), 8):
        if i + 8 <= len(binary_data):
            byte = binary_data[i:i+8]
            data_bytes.append(int(byte, 2))
    
    # Extract length prefix
    if len(data_bytes) < 4:
        raise ValueError("No hidden data found in image")
    
    data_length = struct.unpack('>I', data_bytes[:4])[0]
    
    # Extract actual data
    if len(data_bytes) < 4 + data_length:
        raise ValueError("Incomplete hidden data in image")
    
    return bytes(data_bytes[4:4 + data_length])
