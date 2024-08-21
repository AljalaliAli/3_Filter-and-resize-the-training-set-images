# add_border.py

"""
This script adds a border to all images in a folder and saves the bordered images in a new folder.
"""

import os
from PIL import Image, ImageOps
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']
border_size = config.getint('border', 'border_size')
color = config['border']['border_color']

def add_border(input_image_path, output_image_path, border_size=1, color='white'):
    """Add a border to an image."""
    image = Image.open(input_image_path)
    bordered_image = ImageOps.expand(image, border=border_size, fill=color)
    bordered_image.save(output_image_path)

def process_images(input_folder, output_folder):
    """Process all images in the input folder by adding a border."""
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.tif', '.gif', '.tiff')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)
            add_border(input_image_path, output_image_path)

# Process the images
process_images(input_folder, output_folder)
