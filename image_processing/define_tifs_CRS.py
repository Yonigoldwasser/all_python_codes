import os
import sys

import rasterio
from rasterio.crs import CRS
from rasterio.enums import Resampling
import shutil

# Define the path to the folder containing the TIFFs
# folder_path = sys.argv[1]
# new_folder_path = sys.argv[2]
folder_path = r"C:\Users\User\Documents\CropScape\2018_30m_cdls"
new_folder_path = r"C:\Users\User\Documents\CropScape\2018_30m_cdls"
# Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

desired_crs = CRS.from_epsg(4326)  # This is WGS84, change EPSG code as needed

for filename in os.listdir(folder_path):
    if filename.endswith('.tif'):
        print(filename)
        new_filename = filename[:-4] + "_4326.tif"
        file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(new_folder_path, new_filename)

        # Copy the original TIFF to the new folder
        shutil.copy2(file_path, new_file_path)

        # Update the CRS of the TIFF in the new folder
        with rasterio.open(new_file_path, mode='r+') as src:
            src.crs = desired_crs

print("CRS added/updated for all TIFFs in the new folder!")