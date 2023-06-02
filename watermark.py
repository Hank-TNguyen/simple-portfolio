import cv2
import numpy as np
import glob
from PIL import Image
import piexif
import os

# Load the watermark image
watermark = cv2.imread('watermark.png', -1)

# Get a list of all jpg images in the directory
image_files = glob.glob('images/*.jpg')

# Define the margins and watermark size as a ratio of the image size
margin = 50
watermark_size_ratio = 0.15

for image_file in image_files:
    # Load the image to be watermarked
    img_pil = Image.open(image_file)
    exif_data = img_pil.info.get('exif', b'')
    
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    # If the image has two channels, convert it to three channels
    if len(img.shape) < 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
    # Make the image 4-channels by adding an alpha channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Resize the watermark to be a certain ratio of the width of the image
    watermark_width = int(img.shape[1] * watermark_size_ratio)
    watermark_height = int(watermark_width * watermark.shape[0] / watermark.shape[1])
    watermark_resized = cv2.resize(watermark, (watermark_width, watermark_height))
    
    # The start coordinates of the watermark (bottom right corner)
    x_start = img.shape[1] - watermark_resized.shape[1] - margin
    y_start = img.shape[0] - watermark_resized.shape[0] - margin

    # Compute the average brightness of the area where the watermark will be placed
    roi = img[y_start: y_start + watermark_resized.shape[0], x_start: x_start + watermark_resized.shape[1], :3]
    avg_brightness = np.mean(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))

    # Change the color of the watermark based on the average brightness
    if avg_brightness > 127:
        watermark_resized[..., :3] = 0  # Change color to black
    else:
        watermark_resized[..., :3] = 255  # Change color to white

    # Create a mask of zeros with the same size as the image
    mask = np.zeros_like(img)

    # Place the watermark at the bottom right corner of the mask
    mask[y_start: y_start + watermark_resized.shape[0], x_start: x_start + watermark_resized.shape[1]] = watermark_resized

    # Split the image and the mask into their RGB and alpha channels
    img_rgb = img[..., :3]
    img_alpha = img[..., 3] / 255
    mask_rgb = mask[..., :3]
    mask_alpha = mask[..., 3] / 255

    # Compute the new RGB values and alpha value for the image
    new_rgb = img_rgb * (1 - mask_alpha[..., None]) + mask_rgb * mask_alpha[..., None]
    new_alpha = np.maximum(img_alpha, mask_alpha)

    # Combine the new RGB and alpha values into a 4-channel image
    watermarked_img = np.concatenate([new_rgb, new_alpha[..., None]], axis=-1).astype(np.uint8)
    watermarked_img_pil = Image.fromarray(cv2.cvtColor(watermarked_img, cv2.COLOR_BGRA2RGBA))
    # Write out the watermarked image
    watermarked_img_pil = watermarked_img_pil.convert('RGB')
    watermarked_img_pil.save('watermarked/watermarked_' + os.path.basename(image_file), exif=exif_data)
