import os
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
from datetime import date
import rasterio
import json
import datetime
import pandas as pd

# Add the current date to the filename
today = date.today().strftime('%Y-%m-%d')

# Set the folder path where the GeoJSON file is present
geojson_folder_path = r'C:\Users\User\Desktop\test1'

# Set the folder path where the TIFF files are present
tiff_folder_path = r'C:\Users\User\Desktop\test1\PoPr_rasters'

# Set the folder path where the clipped TIFF files will be saved
clipped_tiff_folder_path = r"C:\Users\User\Desktop\test1\clipped_rasters"

# Set the name of the input GeoJSON file
input_file_name = 'main_json_test.geojson'

# Set the name of the output GeoJSON file
output_file_name = 'pushed_json_test_' + today + '.geojson'

# Read the GeoJSON file as a GeoDataFrame
gdf = gpd.read_file(os.path.join(geojson_folder_path, input_file_name))
#print(gdf)
last_column_name = gdf.columns[-2]
# Create a new GeoDataFrame with only the rows that have a value of 1 in the last column
new_gdf = gdf[gdf[last_column_name] == 1]
#print(new_gdf)
# Get a list of unique tile names from the "tile" column of the new GeoDataFrame
tile_names = new_gdf['tile'].unique()
#print(tile_names)
# Loop through the tile names
jsons_list = []
for tile_name in tile_names:
    print(tile_name)

    # Find the TIFF files with matching names in the TIFF folder
    matching_tiffs = [f for f in os.listdir(tiff_folder_path) if tile_name in f and 'res' in f]

    # Loop through the matching TIFF files
    for matching_tiff in matching_tiffs:
        # Construct the full path of the matching TIFF file
        matching_tiff_path = os.path.join(tiff_folder_path, matching_tiff)
        #print(matching_tiff_path)
        # Clip the geometries from the new GeoDataFrame that are relevant to the tile
        clipped_gdf = new_gdf[new_gdf['tile'] == tile_name]
        #print(clipped_gdf, 'clipped_gdf')
        # # Get the bounds of the clipping extent
        # bounds = clipped_gdf.bounds
        # print(bounds, 'bounds')
        # Open the matching TIFF file with Rasterio
        with rasterio.open(matching_tiff_path) as src:
            # print(src, 'src')
            for index, row in clipped_gdf.iterrows():
                # print(index)
                # print(row)
                # Get polygon geometry
                geometry = row['geometry']
                # print(geometry)
                tile_name = row['tile']
                name = str(row['CommonLand'])
                tile_score = row['cdlHsL']
                location = row['location']
                ml_model_code = row['model']
                CluCalcula = row['CluCalcula']
                out_image, out_transform = rasterio.mask.mask(src, [geometry], crop=True, nodata=0, pad=True)
                out_meta = src.meta.copy()
                # Update the metadata with the new transform and dimensions
                out_meta.update({
                    'driver': 'GTiff',
                    'height': out_image.shape[1],
                    'width': out_image.shape[2],
                    'transform': out_transform
                })
                # Construct the output path for the clipped TIFF file
                output_path = os.path.join(clipped_tiff_folder_path, name + today +'_clip.tif')

                # Save the clipped TIFF file
                with rasterio.open(output_path, 'w', **out_meta) as dst:
                    # print(out_image)
                    dst.write(out_image)
                    # Calculate the unique classes and their counts
                    unique_classes, class_counts = np.unique(out_image[out_image != 0], return_counts=True)
                    # Calculate the area of each class in the polygon
                    sum_polygon_counts = np.sum(out_image != 0)
                    areas = []
                    for class_value in unique_classes:
                        mask = out_image == class_value
                        pix_count = np.sum(out_image == class_value)
                        area_proportion = pix_count/sum_polygon_counts
                        acres = area_proportion*CluCalcula
                        areas.append(acres)
                    # print(acres, 'acres')
                    # print(unique_classes)
                    # print(class_counts)
                    # Create an array of objects using a list comprehension and zip()
                    stats = [{'crop_code': int(unique_class), 'identified_acres': float(area)} for unique_class, area in
                             zip(unique_classes, areas)]
                    # Print the array of objects
                    stats_sorted = sorted(stats, key=lambda x: x['identified_acres'], reverse=True)
                    # Create json object containing the array of objects
                    stats_sorted_list = [stats_sorted]
                    json_object = json.dumps(stats_sorted_list)
                    ###############################################################################################
                    crop_majority = stats_sorted[0]['crop_code']
                    # calculate conf
                    if tile_score == 3:
                        tile_score = 0.3
                    elif tile_score == 2:
                        tile_score = 0.2
                    else:
                        tile_score = 0.1
                    if location == 'CornBelt':
                        location = 0.2
                    else:
                        location = 0.05
                    if crop_majority == 41:
                        crop_majority = 0.25
                    elif crop_majority == 81:
                        crop_majority = 0.15
                    else:
                        crop_majority = 0.1
                    if today < str(datetime.date(2023, 6, 25)):
                        classification = 0.05
                    else:
                        classification = 0.2

                    conf_value = location + classification + tile_score + crop_majority
                    #print(conf_value)

                    ##############################################################################################
                clipped_gdf.at[index, 'results'] = json_object
                clipped_gdf.at[index, 'confidence'] = conf_value
                clipped_gdf.at[index, 'execution_date'] = today
                clipped_gdf.at[index, 'tile'] = tile_name
            jsons_list.append(clipped_gdf)
# merge tiles final dataframes
merged_df = pd.concat(jsons_list)
# Merge the original GeoDataFrame with tile final merged dataframe
merged_gdf = gdf.merge(merged_df, how='left')
print(merged_gdf)
# merged_gdf.to_file(os.path.join(geojson_folder_path, output_file_name), driver='GeoJSON')
