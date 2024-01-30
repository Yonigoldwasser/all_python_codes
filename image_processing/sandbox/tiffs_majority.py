# import os
# import geopandas as gpd
# import rasterio
# from rasterio.mask import mask
# from shapely.geometry import mapping
# from scipy.stats import mode
# from collections import Counter
#
# geojson_file = r"C:\Users\User\Documents\CI_small_grid_comparison\Proag_2022_5_grid_clus.gpkg"
# gdf = gpd.read_file(geojson_file)
#
# # Path to folder containing TIFFs
# tiff_folder_path = r"C:\Users\User\Documents\CI_small_grid_comparison"
#
# def get_majority_pixel_value(pixels):
#     # Count occurrences of each pixel value
#     counter = Counter(pixels)
#     # Return the pixel value with the highest count
#     return max(counter, key=counter.get, default=None)
#
#
#
#
# # Get a list of all TIFF files in the folder
# # tiff_files = [f for f in os.listdir(tiff_folder_path) if f.endswith('.tif')]
# # tiff_files = [f for f in os.listdir(tiff_folder_path) if f.endswith('.tif') and 'cropid' in f]
# tiff_files = []
# for root, dirs, files in os.walk(tiff_folder_path):
#     for file in files:
#         if file.endswith('.tif') and 'cropid' in file:
#             tiff_files.append(os.path.join(root, file))
# print(tiff_files)
# for tiff_file in tiff_files:
#     tiff_path = os.path.join(tiff_folder_path, tiff_file)
#     column_name = os.path.basename(tiff_path)[:-4]
#     print(column_name)
#     with rasterio.open(tiff_path) as src:
#         majority_values = []
#
#         for _, row in gdf.iterrows():
#             shapes = [mapping(row['geometry'])]
#             out_image, _ = mask(src, shapes, crop=True, all_touched=True, nodata=99, filled=True)
#
#             # Extract pixel values excluding nodata values
#             pixel_values = out_image[out_image != src.nodata]
#
#             # Calculate the majority pixel value using the new function
#             majority_pixel_value = get_majority_pixel_value(pixel_values)
#
#             majority_values.append(majority_pixel_value)
#
#         column_name = os.path.basename(tiff_path)[:-4]
#         gdf[column_name] = majority_values
# #         print(gdf)
# # print(gdf)
# gdf.to_csv(r"C:\Users\User\Documents\CI_small_grid_comparison\Proag_2022_5_grid_clus_majority.csv")

import gdal

# Open the TIFF file
tif_path = r"C:\Users\User\Documents\CS_sequence_check\CI_add_forecast\new_CI\all_MNT11_tile\reg_MNT11_2022_forecast_corrected.tif"
ds = gdal.Open(tif_path)

if ds is None:
    print("Unable to open the TIFF file.")
else:
    # Get the image's width and height (number of columns and rows)
    width = ds.RasterXSize
    height = ds.RasterYSize

    # Define the X and Y coordinates of the pixel you want to find
    x_coord = -93.77407  # Replace with the X coordinate you're interested in
    y_coord = 44.11439
  # Replace with the Y coordinate you're interested in

    # Calculate the index number of the pixel in the TIFF matrix
    pixel_index = y_coord * width + x_coord

    print(f"The index number of the pixel at ({x_coord}, {y_coord}) is: {pixel_index}")

    # Close the TIFF file
    ds = None
