import os
import shutil

# Define directories and file
TIF_DIR = "/home/ubuntu/ci_yoni/rs_ci_AWS_post_process/Y11/tmp/output"  # Replace with the path to your .tif folder
TARGET_DIR = "/home/ubuntu/ci_yoni/rs_ci_AWS_post_process/Y11a"  # Replace with the path where you want the filtered .tif files to be copied to
LIST_FILE = "test_proag23_clus_list.txt"  # Replace with the path to your .txt file containing the list of names

# Ensure target directory exists
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# Read names from the txt file
with open(LIST_FILE, 'r') as f:
    names = f.read().splitlines()

# Copy matching tif files to target directory
for name in names:
    source_file = os.path.join(TIF_DIR, f"{name}.tif")
    if os.path.exists(source_file):
        shutil.copy(source_file, TARGET_DIR)
