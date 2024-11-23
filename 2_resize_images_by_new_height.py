# resize_images_by_new_height.py

"""
This script loads images from a folder, resizes them to a new height while maintaining 
the aspect ratio, and saves the resized images in a new folder.
"""

import cv2
import os
import glob
from configparser import ConfigParser

from math import gcd, ceil

def adjust_dimensions(h, w, h1_initial):
    """
    Adjusts the height (h1) minimally to ensure both h1 and the corresponding width (w1)
    are integers without rounding.

    Parameters:
    - h (int): Original height.
    - w (int): Original width.
    - h1_initial (int): Desired initial height.

    Returns:
    - tuple: (h1, w1) where both are integers.
    """
    # Step 1: Calculate the Greatest Common Divisor of h and w
    d = gcd(h, w)
    
    # Step 2: Determine the smallest step to adjust h1
    step = h // d
    
    # Step 3: Find the smallest multiple of 'step' that is >= h1_initial
    multiple = ceil(h1_initial / step)
    h1 = multiple * step
    
    # Step 4: Calculate w1 to ensure it's an integer
    w1 = (w // d) * multiple
    
    return h1, w1



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

    ##############
    # Adjust dimensions
    h1, w1 = adjust_dimensions(original_height, original_width, new_height)
    
    #print(f"Adjusted Dimensions:")
    #print(f"h1 = {h1}")
    #print(f"w1 = {w1}")

    ##############

    # Calculate the aspect ratio
    #aspect_ratio = original_width / original_height

    # Calculate the new width to maintain the aspect ratio
    #new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_img = cv2.resize(img, (w1, h1))

    # Save the resized image in the output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, resized_img)

print(f"Resized images saved in '{output_folder}' folder.")


