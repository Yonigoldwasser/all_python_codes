import os
import geopandas as gpd
from datetime import date

# Set the folder path where the TIFF files are present
tiff_folder_path = '/path/to/tiff/folder'

# Set the folder path where the GeoJSON file is present
folder_path = '/path/to/geojson/folder'

# Set the column name to filter the data by ones and zeros
column_name = 'column_name_with_ones_and_zeros'

# Read the GeoJSON file as a GeoDataFrame
gdf = gpd.read_file(os.path.join(folder_path, 'input_file.geojson'))

# Filter the data by ones and zeros in the specified column
filtered_data = gdf[gdf[column_name] == 1]

# Create a new GeoDataFrame from the filtered data
new_gdf = gpd.GeoDataFrame(filtered_data, crs=gdf.crs)

# Add the current date to the filename
today = date.today().strftime('%Y-%m-%d')

# Save the new GeoDataFrame as a GeoJSON file
new_gdf.to_file(os.path.join(folder_path, 'Only_pushed_tile_' + today + '.geojson'), driver='GeoJSON')

# Get a list of unique tile names from the "tile" column
tile_names = new_gdf['tile'].unique()
# Create an empty list to store the paths of matching TIFF files
matching_tiff_paths = []

# Loop through the tile names
for tile_name in tile_names:

    # Find the TIFF files with matching names in the TIFF folder
    matching_tiffs = [f for f in os.listdir(tiff_folder_path) if tile_name in f]

    # Add the paths of the matching TIFF files to the list
    for matching_tiff in matching_tiffs:
        matching_tiff_path = os.path.join(tiff_folder_path, matching_tiff)
        matching_tiff_paths.append(matching_tiff_path)

# Print the list of matching TIFF file paths
print(matching_tiff_paths)