# Image Preprocessing Toolkit

## Overview

This repository contains a collection of scripts designed to preprocess datasets that include both images and ground truth text files. The toolkit is particularly useful for preparing training data for machine learning models.

## Contents

- **1_batch_crop_images_by_contours.py**: Crops images by detecting contours and saves the cropped images.
- **2_resize_images_by_new_height.py**: Resizes images to a specified height while maintaining aspect ratio.
- **3_add_boarders.py**: Adds borders to the resized images.
- **4_filter_bw_images.py**: Filters out images that are not purely black and white.
- **5_cleanup_unmatched_text_files.py**: Cleans up the dataset by removing unmatched image and text files.
- **0_Process and Filter Training Data Set.py**: A unified script that combines all the above tasks into a single, streamlined process.

## Configuration

All scripts use a common configuration file named `config.ini`. This file should contain the necessary paths and parameters for processing your dataset.

### Example `config.ini`:
```ini
[paths]
input_folder = /path/to/input_folder
output_folder = /path/to/output_folder
non_bw_images_folder = /path/to/non_bw_images_folder

[resize]
new_height = 800

[border]
border_size = 10
border_color = white
