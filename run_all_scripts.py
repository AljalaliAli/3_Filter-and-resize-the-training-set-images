import subprocess

# List of scripts to run
scripts = [
    "1_batch_crop_images_by_contours.py",
    "2_resize_images_by_new_height.py",
    "3_add_boarders.py",
    "4_filter_bw_images.py",
    "5_cleanup_unmatched_text_files.py"
]

# Run each script sequentially
for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}:\n{result.stderr}")
    else:
        print(f"Output of {script}:\n{result.stdout}")
    print("-" * 40)

print("All scripts have been executed.")
