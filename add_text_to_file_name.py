# batch_rename_files.py

"""
This script loads images from a folder, adds specified text to the filenames as a prefix or suffix,
and saves the renamed images in the same folder.
"""

import os
from configparser import ConfigParser

def add_text_to_filenames(folder_path, text_to_add, position='prefix'):
    """
    Adds specified text to all filenames in the given folder.

    Parameters:
    - folder_path (str): Path to the target folder.
    - text_to_add (str): Text to add to each filename.
    - position (str): 'prefix' to add text at the beginning, 'suffix' to add at the end.
    """
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Loop through all items in the folder
    for filename in os.listdir(folder_path):
        # Construct full file path
        file_path = os.path.join(folder_path, filename)

        # Proceed only if it's a file (ignore subfolders)
        if os.path.isfile(file_path):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)

            # Determine the new filename based on the desired position
            if position.lower() == 'prefix':
                new_name = f"{text_to_add}_{name}{ext}"
            elif position.lower() == 'suffix':
                new_name = f"{name}_{text_to_add}{ext}"
            else:
                print("Invalid position argument. Use 'prefix' or 'suffix'.")
                return

            # Construct the new full file path
            new_file_path = os.path.join(folder_path, new_name)

            # Rename the file
            try:
                os.rename(file_path, new_file_path)
                print(f"Renamed: '{filename}' -> '{new_name}'")
            except Exception as e:
                print(f"Failed to rename '{filename}': {e}")

if __name__ == "__main__":
    # Initialize ConfigParser
    config = ConfigParser()

    # Read the config.ini file
    config.read('config.ini')

    # Retrieve configuration parameters
    try:
        folder = config.get('paths', 'output_folder')
        text = config.get('rename', 'text_to_add')
        position = config.get('rename', 'position')
    except Exception as e:
        print(f"Error reading configuration: {e}")
        exit(1)

    # Validate the 'position' parameter
    if position.lower() not in ['prefix', 'suffix']:
        print("Invalid 'position' value in config.ini. Use 'prefix' or 'suffix'.")
        exit(1)

    # Call the function to add text to filenames
    add_text_to_filenames(folder, text, position)
