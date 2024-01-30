import geopandas as gpd
import os
import shutil

# # Load the shapefile
# shapefile_path = r"C:\Users\User\Documents\FMH_2023\FMH_2023_tiles.geojson"
# shapefile = gpd.read_file(shapefile_path)
# Load the GeoJSON file
geojson_path = r"C:\Users\User\Documents\FMH_2023\FMH_2023_tiles.geojson"
geojson = gpd.read_file(geojson_path)
print(geojson['Name'])
# Specify the folder containing TIFF files
tiff_folder = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Proag_FMH_InSeason\C5\Y5_rasters+jsons\meta_Y5"

# Specify the destination folder for the matching TIFF files
destination_folder = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Proag_FMH_InSeason\C5\sarai2"

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# # Iterate through the shapefile rows
# for index, row in shapefile.iterrows():
#     # Extract the name from the name column
#     name = row['Name']
#     numer = 0
#     # Find the TIFF files with the matching name in the folder
#     matching_files = [file for file in os.listdir(tiff_folder) if file.split('_')[1] == name]
#     print(matching_files)
#
#     print(numer + index)
# Iterate through the GeoJSON features
numer = []
for feature in geojson['Name']:
    print(feature)
    # Extract the name from the desired column (replace 'name' with the actual column name)
    name = feature
    print(name)
    numer.append(name)

    # Find the TIFF files with the matching name in the folder
    matching_files = [file for file in os.listdir(tiff_folder) if file.split('_')[1] == name]

    #Move the matching TIFF files to the destination folder
    for file in matching_files:
        file_path = os.path.join(tiff_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.copy(file_path, destination_path)

print('TIFF files moved successfully.')
#
