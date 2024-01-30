
import os
import geopandas as gpd
import pandas as pd
from datetime import date

# Set the folder path where all GeoJSON files are present
folder_path = r"C:\Users\User\Desktop\test1\Rasters_jsons"

# Get a list of all GeoJSON files in the folder
geojson_files = [f for f in os.listdir(folder_path) if f.endswith('.geojson')]

# Create an empty list to store all the GeoDataFrames
geodataframes = []

# Loop through each GeoJSON file and read it as a GeoDataFrame, remove the column and append it to the list
for file in geojson_files:
    gdf = gpd.read_file(os.path.join(folder_path, file))
    gdf.drop(columns=['matrix'], inplace=True)
    geodataframes.append(gdf)

# Merge all the GeoDataFrames into a single GeoDataFrame
final_gdf = gpd.GeoDataFrame(pd.concat(geodataframes, ignore_index=True), crs=geodataframes[0].crs)
# Add the current date to the filename
today = date.today().strftime('%Y-%m-%d')
# Save the final GeoDataFrame as a GeoJSON file
final_gdf.to_file(folder_path +'\merged_geojson_' +today + ".geojson", driver='GeoJSON')
