# Image Preprocessing Toolkit

## Overview

This repository contains a collection of scripts designed to preprocess datasets that include both images and ground truth text files. The toolkit is particularly useful for preparing training data for machine learning models.

## Contents

- **1_batch_crop_images_by_contours.py**: Crops images by detecting contours and saves the cropped images.
- **2_resize_images_by_new_height.py**: Resizes images to a specified height while maintaining aspect ratio.
- **3_add_boarders.py**: Adds borders to the resized images.
- **4_filter_bw_images.py**: Filters out images that are not purely black and white.
- **5_cleanup_unmatched_text_files.py**: Cleans up the dataset by removing unmatched image and text files.

