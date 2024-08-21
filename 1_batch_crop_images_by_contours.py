# batch_crop_images_by_contours.py

"""
This script loads images from a folder, converts them to grayscale, applies thresholding,
finds contours, merges the bounding boxes of these contours, and then crops 
the images to the merged bounding box. The cropped images are saved in a new folder.
"""

import cv2
import numpy as np
import os
import glob
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
    # Load the image
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store the minimum and maximum coordinates
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    # Iterate over the contours
    for contour in contours:
        # Get the bounding rectangle for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Update the minimum and maximum coordinates
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    # Crop the image using the merged bounding box coordinates
    cropped_img = img[min_y:max_y, min_x:max_x]

    # Save the cropped image in the output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, cropped_img)

print(f"Cropped images saved in '{output_folder}' folder.")
