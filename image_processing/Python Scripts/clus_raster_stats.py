import geopandas as gpd
import pandas as pd
import rasterio
from rasterio import mask
import numpy as np
import rasterstats as rs

# Read the GeoJSON file
geojson_file = r"C:\Users\User\Documents\FMH_2023_CC\FMH_clus.geojson"
gdf = gpd.read_file(geojson_file)
# Explode the MultiPolygon geometries into separate Polygons
gdf_exploded = gdf.explode()

# Reset the index of the exploded GeoDataFrame
gdf = gdf_exploded.reset_index(drop=True)
# Read the raster file (TIFF)
tif_file = r"C:\Users\User\Documents\Combined_CC_2023_vars\Poria_10m_mosaic.tif"
with rasterio.open(tif_file) as src:
    # Calculate the pixel size in acres
    pixel_area = src.res[0] * src.res[1] * 0.000247105  # Conversion factor from square meters to acres

    # Create a DataFrame to store the statistics
    stats_df = pd.DataFrame(columns=['cluid', 'active_acres', 'not_active_acres', 'active_percent', 'not_active_percent'])

    # Iterate over each geometry in the GeoJSON file
    for idx, geom in gdf.iterrows():
        # Extract the geometry name from the cluid column
        cluid = geom['CommonLand']
        acres = geom['CluCalcula']
        state_abrre = geom['StateAbbre']
        print(cluid)

        geomm = geom['geometry']

        # Mask the raster with the geometry
        masked_data, _ = mask.mask(src, [geom.geometry], crop=True, nodata=10)

        # Change raster values higher than 1 to 1
        masked = np.where((masked_data > 1) & (masked_data < 5),1,masked_data)
        # Calculate the active and not active acres
        active_pixels = (masked == 1).sum()
        not_active_pixels = (masked == 0).sum()



        total_pixels = active_pixels + not_active_pixels

        active_acres_proportion = active_pixels / total_pixels
        active_acres = acres * active_acres_proportion

        not_active_acres_proportion = not_active_pixels / total_pixels
        not_active_acres = acres * not_active_acres_proportion

        # Calculate the percentages
        active_percent = (active_pixels / total_pixels) * 100
        not_active_percent = (not_active_pixels / total_pixels) * 100

        # Append the statistics to the DataFrame
        stats_df = stats_df.append({'StateAbbre': state_abrre,
                                    'CluCalcula': acres,
                                    'cluid': cluid,
                                    'active_pixels' : active_pixels,
                                    'not_active_pixels' : not_active_pixels,
                                    'active_acres': active_acres,
                                    'not_active_acres': not_active_acres,
                                    'active_percent': active_percent,
                                    'not_active_percent': not_active_percent}, ignore_index=True)

# Print the resulting DataFrame
print(stats_df)
# Save the DataFrame to a CSV file
output_csv_file = r"C:\Users\User\Documents\FMH_2023_CC\FMH_2023_clus_acres_stat.csv"
stats_df.to_csv(output_csv_file, index=False)