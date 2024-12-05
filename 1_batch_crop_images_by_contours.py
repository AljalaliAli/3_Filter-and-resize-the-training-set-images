# batch_crop_images_by_contours.py

"""
This script loads images from a folder, converts them to grayscale, applies thresholding,
finds contours, and then crops the images vertically based on the topmost and bottommost contours.
The cropped images are saved in a new folder.
"""

import cv2
import numpy as np
import os
import glob
from configparser import ConfigParser

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']

print(f"{GREEN}Configuration loaded successfully.{RESET}")
print(f"{GREEN}Input folder: {input_folder}{RESET}")
print(f"{GREEN}Output folder: {output_folder}{RESET}")

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)
print(f"{GREEN}Output folder '{output_folder}' created or already exists.{RESET}")

# Loop through all images in the input folder
for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
    print(f"{GREEN}Processing image: {img_path}{RESET}")
    # Load the image
    img = cv2.imread(img_path)
    if img is None:
        print(f"{RED}Failed to load image: {img_path}{RESET}")
        continue

    print(f"{GREEN}Image loaded successfully.{RESET}")
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"{GREEN}Image converted to grayscale.{RESET}")

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(f"{GREEN}Thresholding applied.{RESET}")

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"{GREEN}Found {len(contours)} contours.{RESET}")

    # Initialize variables to store the minimum and maximum Y coordinates
    min_y = float('inf')
    max_y = float('-inf')

    # Iterate over the contours
    for contour in contours:
        # Get the bounding rectangle for each contour
        x, y, w, h = cv2.boundingRect(contour)
        print(f"{GREEN}Contour bounding box - x: {x}, y: {y}, w: {w}, h: {h}{RESET}")

        # Update the minimum and maximum Y coordinates
        min_y = min(min_y, y)
        max_y = max(max_y, y + h)

    # If no contours were found, skip cropping
    if min_y == float('inf') or max_y == float('-inf'):
        print(f"{RED}No contours found in image: {img_path}. Skipping cropping.{RESET}")
        cropped_img = img  # Keep the original image
    else:
        # Crop the image vertically using min_y and max_y
        # Keep the entire width of the image
        height, width = img.shape[:2]
        min_y = max(int(min_y), 0)
        max_y = min(int(max_y), height)
        cropped_img = img[min_y:max_y, 0:width]
        print(f"{GREEN}Image cropped vertically from y={min_y} to y={max_y}.{RESET}")

    # Save the cropped image in the output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, cropped_img)
    print(f"{GREEN}Cropped image saved to: {output_path}{RESET}")

print(f"{GREEN}Cropped images saved in '{output_folder}' folder.{RESET}")

# Prevent terminal from closing immediately
input(f"{GREEN}Processing complete. Press Enter to exit...{RESET}")
