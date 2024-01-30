import rasterio
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
import time

start_time = time.time()
print(start_time)
# List of your raster files
rasters_folder_path = r"ILT29/ILT29"
raster_files = os.listdir(rasters_folder_path)
raster_files = [file for file in glob.glob(os.path.join(rasters_folder_path, '*')) if file.endswith('.tif')]
print(raster_files)
print("Current working directory:", os.getcwd())
# Open each raster file and read pixel values
raster_data = []

for raster_file in raster_files[:]:
    print(raster_file)
    with rasterio.open(raster_file) as src:
        # Read the entire raster as a numpy array
        band_data = src.read(1)  # Assuming you are working with a single band raster
        raster_data.append(band_data)

# Get the dimensions of the rasters
height, width = raster_data[0].shape

# Initialize a list to store arrays for each pixel
pixel_value_arrays = []

# Iterate through each pixel and create an array of pixel values
for i in range(height):
    for j in range(width):
        pixel_values = [band[i, j] for band in raster_data]
        pixel_value_arrays.append(pixel_values)

# Find unique arrays and their counts
unique_arrays, counts = np.unique(pixel_value_arrays, axis=0, return_counts=True)

# Create a DataFrame to store unique arrays and their counts
df_unique = pd.DataFrame({'Unique_Arrays': list(unique_arrays), 'Count': counts})
df_unique = df_unique.sort_values(by='Count', ascending=False)

# Open each raster file and read pixel values
raster_data1 = []

for raster_file1 in raster_files[1:]:
    with rasterio.open(raster_file1) as src:
        # Read the entire raster as a numpy array
        band_data1 = src.read(1)  # Assuming you are working with a single band raster
        raster_data1.append(band_data1)

# Get the dimensions of the rasters
height1, width1 = raster_data1[0].shape
# Calculate the total number of pixels
num_pixels = width * height
# Print the number of pixels
print(f'Number of pixels in the TIFF image: {num_pixels}')

# Initialize a list to store arrays for each pixel
pixel_value_arrays1 = []

# Iterate through each pixel and create an array of pixel values
for i in range(height1):
    for j in range(width1):
        pixel_values1 = [band[i, j] for band in raster_data1]
        pixel_value_arrays1.append(pixel_values1)

# Given starting array from all pixels in the rasters
given_arrays = pixel_value_arrays1
# Initialize a list to store predicted values for each pixel
predicted_values = []

# Iterate through each given array and predict the last value
for given_array in given_arrays:
    #     print('given_array', given_array)
    # Filter 'df_unique' to find arrays that match the given starting array
    matching_arrays = df_unique[
        df_unique['Unique_Arrays'].apply(lambda x: np.array_equal(x[:len(given_array)], given_array))]
    #     print('matching_arrays', matching_arrays)
    # If matching_arrays is not empty, find the most frequent continuation
    if not matching_arrays.empty:
        most_frequent_continuation = matching_arrays.iloc[0]['Unique_Arrays'][len(given_array):]
        #         print('most_frequent_continuation', most_frequent_continuation)

        # Check if there's a continuation
        if len(most_frequent_continuation) > 0:
            predicted_value = most_frequent_continuation[
                -1]  # Predict the last value based on the most frequent continuation
        else:
            predicted_value = None  # No continuation found
    else:
        predicted_value = None  # No matching arrays found
    #     print('predicted_value',predicted_value)
    predicted_values.append(predicted_value)
    print(len(predicted_values))
print("Done - predicting")
# Reshape the predicted values into a 2D array
predicted_values = np.array(predicted_values).reshape(height, width)

# Create a new raster with the predicted values
output_raster_path = r"ILT29/ILT29/ILT29_predicted_2022.tif"
# Use the profile from the first input raster (assuming all input rasters have similar profiles)
with rasterio.open(raster_files[0]) as src:
    profile = src.profile

profile.update(dtype=np.float32, count=1)

with rasterio.open(output_raster_path, 'w', **profile) as dst:
    dst.write(predicted_values.astype(np.float32), 1)

# print("Predicted raster saved to:", output_raster_path)
# Calculate the elapsed time
end_time = time.time()
elapsed_time = (end_time - start_time) / 60

print(f"Elapsed Time: {elapsed_time:.2f} minutes")