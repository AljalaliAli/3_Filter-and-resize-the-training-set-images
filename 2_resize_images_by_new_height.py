# resize_images_by_new_height.py

"""
This script loads images from a folder, resizes them to a new height while maintaining 
the aspect ratio, and saves the resized images in a new folder.
"""

import cv2
import os
import glob
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']
new_height = config.getint('resize', 'new_height')

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
    # Load the image
    img = cv2.imread(img_path)

    # Get the original dimensions
    original_height, original_width = img.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the new width to maintain the aspect ratio
    new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height))

    # Save the resized image in the output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, resized_img)

print(f"Resized images saved in '{output_folder}' folder.")
