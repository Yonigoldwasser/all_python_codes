import os
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import sys

from rasterio.features import geometry_mask

# Specify the directory containing the TIFF files - Y something, take the last Y{num} folder
formatted_str = "{}".format(sys.argv[1])
tiff_directory = rf"{formatted_str}"
# Get a list of all TIFF files in the directory
# tiff_files = [f for f in os.listdir(tiff_directory) if f.endswith('.tif')]
# Get a list of all TIFF files in the directory and subdirectories
tiff_files = []

for root, dirs, files in os.walk(tiff_directory):
    for file in files:
        if file.endswith('.tif'):
            tiff_files.append(os.path.join(root, file))  # get the full path
# Load the GeoPackage\geojson of pushed not pushed clus from CI
geojson_file = sys.argv[2]
df = pd.DataFrame(columns=['cluid', 'majority_value'])

gdf = gpd.read_file(geojson_file)

# find the majority pixels value in each clu in order to decide if clus will be approved despite their tile unapproved
majority_values = []
for tiff_path in tiff_files:
    tiff_file_name = os.path.basename(tiff_path)  # Extracting only the file name
    print(tiff_file_name)
    cluid = tiff_file_name[:-4]

    with rasterio.open(tiff_path) as src:
        # Read the first band of the TIFF (assuming single band, adjust if necessary)
        data = src.read(1)
        # Remove pixels with a value of 241 (no data value in clipping code)
        data = data[data != 241]
        # Count occurrences of each value in the flattened array
        values, counts = np.unique(data, return_counts=True)

        # Find the value with the highest count
        majority_value = int(values[np.argmax(counts)])

        print(majority_value)

        # Append cluid and majority_value to the DataFrame using pandas.concat
        temp_df = pd.DataFrame([{'cluid': cluid, 'majority_value': majority_value}])
        df = pd.concat([df, temp_df], ignore_index=True)

# print(df)
# Mapping cluid and the majority pixels value
name_majority_mapping = dict(zip(df['cluid'], df['majority_value']))
# appending the majority value of each clu to the geojson
gdf['majority_value'] = gdf['CommonLand'].map(name_majority_mapping)
# print(gdf)

# states\tiles list
corn_tiles = ['OKT32', 'TXT134']
cotton_tiles = ['OKT6']
# Find the last column ending with '_CI'
ci_cols = [col for col in gdf.columns if col.startswith('CI')]
last_ci_col = ci_cols[-1] if ci_cols else None
# Iterate over the rows - find last column in order to change if needed
for index, row in gdf.iterrows():

    # if the clu was not approved in validation but is in the state\tiles list and  the majority is corn or cotton, approve the clus (give last CI value "Y{num}"
    if row[last_ci_col] != last_ci_col and row['tile'] in cotton_tiles and row['majority_value'] == 21:
        # Extract the number before 'CI' and append 'Y' to it
        new_value = 'Y' + last_ci_col[-1] + 'c'
        gdf.at[index, last_ci_col] = new_value
    elif row[last_ci_col] != last_ci_col and row['tile'] in corn_tiles and row['majority_value'] == 41:
        new_value = 'Y' + last_ci_col[-1] + 'c'
        gdf.at[index, last_ci_col] = new_value
# print(gdf)
# remove majority_value column in order to continue with geojson as usual.
gdf = gdf.drop('majority_value', axis=1)
# print(gdf)

# Save the modified geojson_file back as a geojson_file
gdf.to_file(geojson_file, driver="GeoJSON")
