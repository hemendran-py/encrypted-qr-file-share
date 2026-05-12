from PIL import Image
import struct
import numpy as np
import math


def calculate_block_entropy(block):
    """
    Calculate entropy of an 8x8 pixel block.
    Higher entropy indicates more complex/detailed regions.
    """
    # Convert block to grayscale for entropy calculation
    if len(block.shape) == 3:  # RGB
        gray_block = np.mean(block, axis=2)
    else:  # Already grayscale
        gray_block = block
    
    # Flatten the block
    pixels = gray_block.flatten()
    
    # Calculate histogram
    hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
    hist = hist[hist > 0]  # Remove zero bins
    
    # Calculate entropy
    prob = hist / np.sum(hist)
    entropy = -np.sum(prob * np.log2(prob))
    
    return entropy


def calculate_block_variance(block):
    """
    Calculate local variance of an 8x8 pixel block.
    Alternative to entropy for selecting embedding blocks.
    """
    # Convert block to grayscale for variance calculation
    if len(block.shape) == 3:  # RGB
        gray_block = np.mean(block, axis=2)
    else:  # Already grayscale
        gray_block = block
    
    # Calculate variance
    variance = np.var(gray_block)
    return variance


def divide_image_into_blocks(image, block_size=8):
    """
    Divide image into blocks of specified size.
    Returns list of (block, row, col) tuples.
    """
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    blocks = []
    for row in range(0, height - block_size + 1, block_size):
        for col in range(0, width - block_size + 1, block_size):
            block = img_array[row:row+block_size, col:col+block_size]
            blocks.append((block, row, col))
    
    return blocks


def select_high_entropy_blocks(blocks, threshold_percentile=70):
    """
    Select blocks with entropy above the threshold percentile.
    Returns list of (block, row, col, entropy) tuples.
    """
    # Calculate entropy for each block
    block_entropies = []
    for block, row, col in blocks:
        entropy = calculate_block_entropy(block)
        block_entropies.append((block, row, col, entropy))
    
    # Sort by entropy
    block_entropies.sort(key=lambda x: x[3], reverse=True)
    
    # Select top percentile blocks
    num_blocks = len(block_entropies)
    num_selected = max(1, int(num_blocks * threshold_percentile / 100))
    
    return block_entropies[:num_selected]


def data_to_bitstream(data):
    """
    Convert data to bitstream with length prefix.
    """
    # Convert data to bytes if it's a string
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Add length prefix to data
    data_length = len(data)
    data_with_length = struct.pack('>I', data_length) + data
    
    # Convert to binary string
    binary_data = ''.join(format(byte, '08b') for byte in data_with_length)
    
    return binary_data


def bitstream_to_data(bitstream):
    """
    Convert bitstream back to data.
    """
    # Convert binary to bytes
    data_bytes = bytearray()
    for i in range(0, len(bitstream), 8):
        if i + 8 <= len(bitstream):
            byte = bitstream[i:i+8]
            data_bytes.append(int(byte, 2))
    
    # Extract length prefix
    if len(data_bytes) < 4:
        raise ValueError("No hidden data found in image")
    
    data_length = struct.unpack('>I', data_bytes[:4])[0]
    
    # Extract actual data
    if len(data_bytes) < 4 + data_length:
        raise ValueError("Incomplete hidden data in image")
    
    return bytes(data_bytes[4:4 + data_length])


def hide_data_in_image(image, data):
    """
    Hide data using block-level entropy-based embedding.
    """
    # Convert image to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert data to bitstream
    bitstream = data_to_bitstream(data)
    
    # Divide image into 8x8 blocks
    blocks = divide_image_into_blocks(image, block_size=8)
    
    # Select high-entropy blocks
    selected_blocks = select_high_entropy_blocks(blocks, threshold_percentile=70)
    
    # Calculate total capacity of selected blocks
    total_capacity = len(selected_blocks) * 8 * 8 * 3  # 8x8 pixels, 3 channels per pixel
    
    if total_capacity < len(bitstream):
        raise ValueError(f"Image capacity ({total_capacity} bits) too small for data ({len(bitstream)} bits)")
    
    # Create copy of image array
    img_array = np.array(image)
    
    # Embed data in selected blocks
    bit_index = 0
    embedding_map = []  # Store which blocks were used for embedding
    
    for block, row, col, entropy in selected_blocks:
        if bit_index >= len(bitstream):
            break
            
        # Embed bits in this block
        for i in range(8):
            for j in range(8):
                if bit_index >= len(bitstream):
                    break
                
                # Get current pixel
                pixel = img_array[row + i, col + j]
                
                # Embed one bit in each color channel (if needed)
                for channel in range(3):
                    if bit_index >= len(bitstream):
                        break
                    
                    # Clear LSB and set new bit
                    img_array[row + i, col + j, channel] = (pixel[channel] & 0xFE) | int(bitstream[bit_index])
                    bit_index += 1
        
        # Record this block was used for embedding
        embedding_map.append((row, col, entropy))
    
    # Create new image
    new_image = Image.fromarray(img_array.astype(np.uint8))
    
    # Store embedding metadata in image (for extraction)
    # We'll use a simple approach: store the number of embedded bits in the first few pixels
    # This is a basic approach - in practice, you might want more sophisticated metadata storage
    
    return new_image


def extract_data_from_image(image):
    """
    Extract data from block-level entropy-based embedding.
    """
    # Convert image to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Divide image into 8x8 blocks
    blocks = divide_image_into_blocks(image, block_size=8)
    
    # Select high-entropy blocks (same selection as embedding)
    selected_blocks = select_high_entropy_blocks(blocks, threshold_percentile=70)
    
    # Extract bits from selected blocks
    extracted_bits = []
    
    for block, row, col, entropy in selected_blocks:
        # Extract bits from this block
        for i in range(8):
            for j in range(8):
                # Get current pixel
                pixel = image.getpixel((col + j, row + i))
                
                # Extract one bit from each color channel
                for channel in range(3):
                    extracted_bits.append(str(pixel[channel] & 1))
    
    # Convert bitstream to data
    bitstream = ''.join(extracted_bits)
    
    try:
        return bitstream_to_data(bitstream)
    except ValueError:
        # Try with different bit lengths if initial extraction fails
        # This handles cases where not all bits were used
        for end_bit in range(len(bitstream), 0, -8):
            try:
                partial_bitstream = bitstream[:end_bit]
                return bitstream_to_data(partial_bitstream)
            except ValueError:
                continue
        
        raise ValueError("Could not extract valid data from image")
