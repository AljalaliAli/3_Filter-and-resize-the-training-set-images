# filter_bw_images.py

"""
This script filters out images that are not purely black and white from a folder
and moves them to a new folder.
"""

import os
import glob
import cv2
import shutil
import numpy as np
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['non_bw_images_folder']

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
    # Load the image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded correctly
    if img is None:
        print(f"Failed to load image: {img_path}")
        continue

    # Get the unique colors in the image
    unique_colors = np.unique(img)

    # Check if the image has only black (0) and white (255)
    if not np.array_equal(unique_colors, [0, 255]):
        # Move the image to the output folder
        output_path = os.path.join(output_folder, os.path.basename(img_path))
        shutil.move(img_path, output_path)
        print(f"Moved image {img_path} to {output_path}")

print("Process completed.")
