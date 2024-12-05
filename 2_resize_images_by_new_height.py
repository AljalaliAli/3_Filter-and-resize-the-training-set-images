# resize_images_by_new_height.py

"""
This script loads BW images from a folder, resizes them to a new height while maintaining 
the aspect ratio, and adds side padding if necessary to ensure integer dimensions without cutting any part of the image.
"""

import cv2
import os
import glob
from configparser import ConfigParser
from math import ceil, floor


def adjust_dimensions_with_padding(h, w, h1_initial):
    """
    Calculates the new width after scaling to h1_initial height and determines
    the necessary side padding to ensure the new width is an integer and no pixels are lost.

    Parameters:
    - h (int): Original height.
    - w (int): Original width.
    - h1_initial (int): Desired height.

    Returns:
    - tuple: (new_width, left_padding_pixels, right_padding_pixels)
    """
    # Calculate the scaling factor to adjust the height to h1_initial
    scaling_factor = h1_initial / h

    # Compute the scaled width as a float
    scaled_width_float = w * scaling_factor

    # Round up to ensure the width is large enough to contain the entire image
    new_width = ceil(scaled_width_float)

    # Calculate the difference between new_width and scaled_width_float
    total_padding = new_width - scaled_width_float

    # Distribute the total padding equally on both sides
    left_padding = total_padding / 2
    right_padding = total_padding / 2

    # Convert padding to integer number of pixels
    left_padding_pixels = int(floor(left_padding))
    right_padding_pixels = int(ceil(right_padding))

    return new_width, left_padding_pixels, right_padding_pixels


# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']
new_height = config.getint('resize', 'new_height')

# Set padding color to match image background
padding_color = 255  # White background

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
    # Load the image in grayscale mode
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded successfully
    if img is None:
        print(f"Failed to load image: {img_path}")
        continue

    # Get the original dimensions
    original_height, original_width = img.shape[:2]

    # Adjust dimensions
    new_width, left_padding, right_padding = adjust_dimensions_with_padding(
        original_height, original_width, new_height)

    # Calculate the width for resizing (without padding)
    resize_width = new_width - left_padding - right_padding

    # Ensure resize_width is not greater than original width scaled
    resize_width = max(int(round(original_width * (new_height / original_height))), 1)

    # Resize the image to the desired height and calculated width using INTER_NEAREST
    resized_img = cv2.resize(img, (resize_width, new_height), interpolation=cv2.INTER_NEAREST)

    # Add side padding to ensure integer dimensions without rotation
    padded_img = cv2.copyMakeBorder(
        resized_img,
        top=0,
        bottom=0,
        left=left_padding,
        right=right_padding,
        borderType=cv2.BORDER_CONSTANT,
        value=padding_color  # Match the image background color
    )

    # Apply binary threshold to ensure image is strictly black and white
    _, binary_img = cv2.threshold(padded_img, 127, 255, cv2.THRESH_BINARY)

    # Save the final image in the output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, binary_img)

    # Debugging information
    print(f"Processed image: {os.path.basename(img_path)}")
    print(f"Original Dimensions: {original_width}x{original_height}")
    print(f"New Dimensions: {binary_img.shape[1]}x{binary_img.shape[0]}")
    print(f"Left Padding: {left_padding}, Right Padding: {right_padding}")
    print("-" * 50)

print(f"Resized and padded images saved in '{output_folder}' folder.")
