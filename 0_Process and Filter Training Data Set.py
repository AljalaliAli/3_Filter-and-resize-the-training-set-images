"""
Combined Image Processing Script
================================

This script performs multiple image processing tasks in sequence:
1. Batch crop images by contours.
2. Resize images by a new height while maintaining aspect ratio.
3. Add borders to images.
4. Filter out images that are not purely black and white.
5. Clean up unmatched image and text files.

Configuration:
--------------
The script uses a configuration file named 'config.ini' to manage paths and parameters for each task. The relevant sections and keys for each task are described below.

Usage:
------
1. Ensure you have the necessary Python packages installed (e.g., cv2, PIL, numpy, etc.).
2. Configure the 'config.ini' file with appropriate paths and parameters.
3. Run the script.

"""

import os
import glob
import cv2
import numpy as np
from PIL import Image, ImageOps
import shutil
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

def batch_crop_images_by_contours(input_folder, output_folder):
    """
    Batch crop images by contours and save the cropped images.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x + w), max(max_y, y + h)

        cropped_img = img[min_y:max_y, min_x:max_x]
        output_path = os.path.join(output_folder, os.path.basename(img_path))
        cv2.imwrite(output_path, cropped_img)

    print(f"Cropped images saved in '{output_folder}' folder.")

def resize_images_by_new_height(input_folder, output_folder, new_height):
    """
    Resize images to a new height while maintaining the aspect ratio.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
        img = cv2.imread(img_path)
        original_height, original_width = img.shape[:2]
        aspect_ratio = original_width / original_height
        new_width = int(new_height * aspect_ratio)
        resized_img = cv2.resize(img, (new_width, new_height))
        output_path = os.path.join(output_folder, os.path.basename(img_path))
        cv2.imwrite(output_path, resized_img)

    print(f"Resized images saved in '{output_folder}' folder.")

def add_border(input_folder, output_folder, border_size, color):
    """
    Add a border to all images in the input folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.tif', '.gif', '.tiff')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)
            image = Image.open(input_image_path)
            bordered_image = ImageOps.expand(image, border=border_size, fill=color)
            bordered_image.save(output_image_path)

    print(f"Images with borders saved in '{output_folder}' folder.")

def filter_bw_images(input_folder, output_folder):
    """
    Filter out images that are not purely black and white.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for img_path in glob.glob(os.path.join(input_folder, '*.tif')):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        unique_colors = np.unique(img)
        if not np.array_equal(unique_colors, [0, 255]):
            output_path = os.path.join(output_folder, os.path.basename(img_path))
            shutil.move(img_path, output_path)
            print(f"Moved image {img_path} to {output_path}")

    print("Filter process completed.")

def cleanup_unmatched_text_files(folder_path):
    """
    Delete unmatched image and text files in the specified folder.
    """
    all_files = os.listdir(folder_path)
    image_files = {f for f in all_files if f.endswith('.tif')}
    text_files = {f for f in all_files if f.endswith('.gt.txt')}
    image_basenames = {os.path.splitext(f)[0] for f in image_files}
    text_basenames = {os.path.splitext(f)[0].rsplit('.', 1)[0] for f in text_files}
    
    unmatched_images = image_basenames - text_basenames
    unmatched_texts = text_basenames - image_basenames

    for basename in unmatched_images:
        image_path = os.path.join(folder_path, f"{basename}.tif")
        print(f"Deleting unmatched image file: {image_path}")
        os.remove(image_path)

    for basename in unmatched_texts:
        text_path = os.path.join(folder_path, f"{basename}.gt.txt")
        print(f"Deleting unmatched text file: {text_path}")
        os.remove(text_path)

    print("Cleanup process completed.")

# Define paths and parameters
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']  # Single output folder for all steps
non_bw_images_folder = config['paths']['non_bw_images_folder']
new_height = config.getint('resize', 'new_height')
border_size = config.getint('border', 'border_size')
border_color = config['border']['border_color']

# Run all processes in sequence using the same output folder
batch_crop_images_by_contours(input_folder, output_folder)
resize_images_by_new_height(output_folder, output_folder, new_height)
add_border(output_folder, output_folder, border_size, border_color)
filter_bw_images(output_folder, non_bw_images_folder)
cleanup_unmatched_text_files(input_folder)
