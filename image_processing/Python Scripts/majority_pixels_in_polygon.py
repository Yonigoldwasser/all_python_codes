import geopandas as gpd
import os
from rasterstats import zonal_stats
import glob

# Read the geopackage
geojson_file = r"C:\Users\User\Documents\CS_sequence_check\CI_add_forecast\new_CI\2023_Y6_all_OK_SD\OK_SD_tiles_2023_PA_clus.shp"
gdf = gpd.read_file(geojson_file)

# Path to folder containing TIFFs
tiff_folder_path = r"C:\Users\User\Documents\CS_sequence_check\CI_add_forecast\new_CI\2023_Y6_all_OK_SD\forecast_corrected_tiffs"

tiff_files = []
for root, dirs, files in os.walk(tiff_folder_path):
    for file in files:
        if file.endswith('.tif'):#and 'cropid' in file:
            tiff_files.append(os.path.join(root, file))
print(tiff_files)
print(len(tiff_files))
Y6 = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\Y6_10m_cropid.tif"
tiff_files.append(Y6)
# Extract the majority pixel value for each TIFF
for tif_path in tiff_files:#[:-1]:
    print(os.path.basename(tif_path)[:-4])
    # Calculate zonal statistics for the current TIFF
    stats = zonal_stats(gdf, tif_path, stats="majority")

    # Extract the 'majority' value from the zonal_stats output and add it as a new column
    column_name = os.path.basename(tif_path)[:-4]
    gdf[column_name] = [s['majority'] for s in stats]
# print(gdf)
# gdf['reg_ci_OKT14_2022_1_5_15_6'] = gdf['reg_ci_OKT14_2022_1_5_15_6'] .replace({0: 'Nonag', 1: 'Corn', 2: 'Cotton', 3: 'Soybeans', 4: 'Spring wheat', 5: 'Soybeans', 7: 'Other'})
# gdf['reg_OKT14_2022_forecast_corrected'] = gdf['reg_OKT14_2022_forecast_corrected'] .replace({41: 'Corn', 21: 'Cotton', 81: 'Soybeans', 11: 'Spring wheat', 101: 'Other', 102: 'Nonag'})
# Define your replacement dictionary
replacement_dict = {41: 'Corn', 21: 'Cotton', 81: 'Soybeans', 11: 'Spring wheat', 101: 'Other', 102: 'Nonag'}

# Apply the replacement to each column in the DataFrame
for column in gdf.columns[22:]:
    gdf[column] = gdf[column].replace(replacement_dict)
# print(gdf)
# Save results to the output geopackage
gdf.to_csv(r"C:\Users\User\Documents\CS_sequence_check\CI_add_forecast\new_CI\2023_Y6_all_OK_SD\2023_Y6_OK_SD_clus_majority.csv")