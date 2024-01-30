
# import pandas as pd
# import geopandas as gpd
#
# # Read the CSV file and extract the filter list
# csv_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C6\CI6_nonAgs_list.csv"
# df = pd.read_csv(csv_file_path)
# #print(df)
# filter_list = df[df.columns[1]].tolist()
# #print(filter_list)
# # Upload GeoJSON file
# geojson_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C6\CI6_Proag_clus_geojson.geojson"
# gdf = gpd.read_file(geojson_file_path)
##########################################################################################
# gdf_subset = gdf.head
# for idx, row in gdf_subset.iterrows():
#    # print(idx)
#    # print(row['geometry'])
#     geometry = row.geometry
#     Polygons = list(geometry.geoms)
   # print(Polygons[0])


    #     # Extract the coordinates of the polygon
    #     polygon_coords = polygon.exterior.coords
    #     print(f"Coordinates for Polygon {idx + 1}:")
    #     for coord in polygon_coords:
    #         print(coord)
    #     print("---")

##########################################################################################

# Filter the GeoJSON file
filtered_gdf = gdf[gdf['CommonLand'].isin(filter_list)]
# Iterate over the GeoDataFrame and print the length of each geometry
##########################################################################################
# print('##########################################################################################')
# gdff_subset = filtered_gdf.head(20)
# for idx, row in gdff_subset.iterrows():
#    ## print(idx)
#    # print(row['geometry'])
#     geometry = row.geometry
#     Polygons = list(geometry.geoms)
#    # print(Polygons[0])
# from shapely.validation import explain_validity
# gdff_subset['validity'] = gdff_subset.apply(lambda row: explain_validity(row.geometry), axis=1)
#
# #print(gdff_subset)
##########################################################################################

# Print the filtered GeoJSON data
# print(filtered_gdf)

# # Save the new GeoDataFrame to a GeoJSON file
# output_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C6\CI6_nonag_new_CI.gpkg"
# filtered_gdf.to_file(output_file_path, driver='GPKG')
# print("New GeoJSON file saved successfully.")