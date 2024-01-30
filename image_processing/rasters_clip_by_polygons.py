import pandas as pd
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import json
import os
import numpy as np

###############################################################
# change ratser path and geojson path
###############################################################
df = gpd.GeoDataFrame(columns=["cluid", "geom"], crs="EPSG:4326", geometry="geom")
name_list = []
crop_list = []
geom_list = []
######################################################
gdf_main = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\picked_clus.geojson")
print(gdf_main)
######################################################
# Open the raster file
with rasterio.open(r"C:\Users\User\Documents\ProAg_2023_CC\Post_process_2_test\merge_tiles.tif") as src:
    print(src)
    # Load the polygons from the GeoJSON file
    with open(r"C:\Users\User\Documents\ProAg_2023_CC\picked_clus.geojson") as f:
        print(f)
        polygons = json.load(f)['features']
    # Loop through the polygons and clip the raster
    for polygon in polygons:
        #print(polygon)
        name = str(polygon['properties']['PWId'])
        print(name)
        geometry = polygon['geometry']
        # Create a GeoDataFrame with the current polygon
        gdf = gpd.GeoDataFrame.from_features([polygon], crs=src.crs)
        print(gdf)
        # Clip the raster with the polygon geometry
        print(src)
        out_image, out_transform = rasterio.mask.mask(src, gdf.geometry, crop=True)
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
            area = np.sum(mask) * (src.res[0] * 100000) * (src.res[1] * 100000) * 0.000247105  # Convert to acres
            areas.append(area)
        print(areas, 'areas')
        print(unique_classes)
        print(class_counts)
        # Create an array of objects using a list comprehension and zip()
        people = [{'crop_code': int(unique_class), 'identified_acres': float(area)} for unique_class, area in
                  zip(unique_classes, areas)]
        # Print the array of objects
        print(name)
        print(people)
        # Create a pandas Series object containing the array of objects
        series = pd.Series(people)
        # ame_list.append(name)
        crop_list.append(people)
        json_object = json.dumps(crop_list)
print(json_object, 'json_object')
print(len(json_object))
for list in crop_list:
    print(list)
gdf_main['crop'] = json_object
print(gdf_main)
# # Write the updated GeoJSON file to disk
gdf_main.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\geojason_test.csv")
gdf_main.to_file(r"C:\Users\User\Documents\ProAg_2023_CC\geojason_test.geojson", driver='GeoJSON')