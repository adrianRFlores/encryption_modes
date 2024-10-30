import random
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Set the encryption mode (ECB or CBC)
mode = 'CBC'

# Set a seed for reproducibility
seed = 42
random.seed(seed)

# Open the image and convert it to a NumPy array
image = Image.open('tux.bmp')
image_data = np.array(image)

# Reshape the image data to separate color channels (RGBA)
image_data = image_data.reshape((405, 480, 4))
# Convert the image data to bytes for encryption
image_bytes = image_data.tobytes()

# Generate a random 16-byte key for AES encryption
key = random.randbytes(16)

# Set up the cipher object based on the selected mode
if mode == 'CBC':
    # Generate a random initialization vector (IV) for CBC mode
    iv = random.randbytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
else:
    # Use ECB mode (no IV required)
    cipher = AES.new(key, AES.MODE_ECB)

# Pad the image bytes to ensure it's a multiple of the AES block size
padded_image_bytes = pad(image_bytes, AES.block_size)

# Encrypt the padded image bytes
encrypted_bytes = cipher.encrypt(padded_image_bytes)

# Create a new image from the encrypted bytes and save it as a PNG file
output_image = Image.frombytes('RGBA', (405, 480), encrypted_bytes)
output_image.save(f'output_{mode}.png')

# Print a message indicating the output file name
print(f'PNG image saved as "output_{mode}.png"')
