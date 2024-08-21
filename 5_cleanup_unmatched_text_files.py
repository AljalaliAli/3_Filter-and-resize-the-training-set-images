# cleanup_unmatched_text_files.py

"""
This script deletes unmatched image and text files in a folder.
"""

import os
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')
folder_path = config['paths']['input_folder']

def delete_unmatched_files(folder_path):
    """Delete unmatched image and text files in the specified folder."""
    # List all files in the directory
    all_files = os.listdir(folder_path)
    
    # Separate image files and text files
    image_files = {f for f in all_files if f.endswith('.tif')}
    text_files = {f for f in all_files if f.endswith('.gt.txt')}
    
    # Get the base names of the files (without extensions)
    image_basenames = {os.path.splitext(f)[0] for f in image_files}
    text_basenames = {os.path.splitext(f)[0].rsplit('.', 1)[0] for f in text_files}
     
    print('image_basenames ', image_basenames)
    print('text_basenames  ', text_basenames)
    
    # Find unmatched image files and text files
    unmatched_images = image_basenames - text_basenames
    unmatched_texts = text_basenames - image_basenames
 
    # Delete unmatched image files
    for basename in unmatched_images:
        image_path = os.path.join(folder_path, f"{basename}.tif")
        print(f"Deleting unmatched image file: {image_path}")
        os.remove(image_path)
    
    # Delete unmatched text files
    for basename in unmatched_texts:
        text_path = os.path.join(folder_path, f"{basename}.gt.txt")
        print(f"Deleting unmatched text file: {text_path}")
        os.remove(text_path)

# Delete unmatched files
delete_unmatched_files(folder_path)
