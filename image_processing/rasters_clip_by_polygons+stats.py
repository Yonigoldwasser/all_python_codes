import pandas as pd
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import json
import os
import numpy as np
from datetime import date
import datetime

###############################################################
# change ratser path and geojson path
###############################################################

######################################################
gdf_main = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\picked_clus_new_extra_data.geojson")
print(gdf_main)
# Add the current date to the filename
today = date.today().strftime('%Y-%m-%d')
######################################################
# Open the raster file
with rasterio.open(r"C:\Users\User\Documents\ProAg_2023_CC\Post_process_2_test\merge_tiles.tif") as src:
    print(src)
# Load the polygons from the GeoJSON file

    for index, row in gdf_main.iterrows():
        print(index)
        print(row)
        # Get polygon geometry
        geometry = row['geometry']
        print(geometry)
        tile_name = row['tile']
        name = str(row['CommonLand'])
        tile_score = row['cdlHsL']
        location = row['location']
        ml_model_code = row['ml_model_code']
        out_image, out_transform = rasterio.mask.mask(src, [geometry], crop=True)
        out_meta = src.meta.copy()
        # Update the metadata with the new transform and dimensions
        out_meta.update({
            'driver': 'GTiff',
            'height': out_image.shape[1],
            'width': out_image.shape[2],
            'transform': out_transform
        })
        # Write the clipped raster to a file
        with rasterio.open(r"C:\Users\User\Documents\ProAg_2023_CC\Post_process_2_test\clip_rasters\clu_" + name + '_clip.tif', 'w', **out_meta) as dest:
            dest.write(out_image)
        # Calculate the unique classes and their counts
        unique_classes, class_counts = np.unique(out_image, return_counts=True)
        # Calculate the area of each class in the polygon
        areas = []
        for class_value in unique_classes:
            #print(class_value, 'class_value')
            mask = out_image == class_value
            print(mask)
            area = np.sum(mask) * (src.res[0]*100000) * (src.res[1]*100000) * 0.000247105  # Convert to acres
            print(np.sum(mask))
            areas.append(area)
        print(areas,'areas')
        print(unique_classes)
        print(class_counts)
        # Create an array of objects using a list comprehension and zip()
        stats = [{'crop_code': int(unique_class), 'identified_acres': float(area)} for unique_class, area in
                  zip(unique_classes, areas)]
        # Print the array of objects
        print(name)
        print(stats)
        stats_sorted = sorted(stats, key=lambda x: x['identified_acres'], reverse=True)
        # Create json object containing the array of objects
        stats_sorted_list = [stats_sorted]
        json_object = json.dumps(stats_sorted_list)
        ###############################################################################################
        crop_majority = stats_sorted[0]['crop_code']
        print(crop_majority)
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
        if today < datetime.date(2023, 6, 25):
            classification = 0.05
        else:
            classification = 0.2

        conf_value = location + classification + tile_score + crop_majority

        print(conf_value)

        ###############################################################################################
        gdf_main.at[index, 'results'] = json_object
        gdf_main.at[index, 'confidence'] = conf_value
        gdf_main.at[index, 'execution_date'] = today
        gdf_main.at[index, 'tile'] = tile_name

#
print(gdf_main.info())
keep_cols = ['CommonLand', 'results', 'confidence', 'execution_date', 'tile', 'ml_model_code'] # add tile, confidence, excution date, ml model, s3 link
gdf_main = gdf_main[keep_cols]
print(gdf_main.head())
# # # Write the updated GeoJSON file to disk
gdf_main.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\geojason_test.csv")
gdf_main.to_json(r"C:\Users\User\Documents\ProAg_2023_CC\geojason_test_" + today +".geojson", orient='records')