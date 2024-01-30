import pandas as pd
import geopandas as gpd
#
# # Read the CSV files
# csv1 = pd.read_csv(r"C:\Users\User\Downloads\delv_compare_logic_proag_0.2.csv")
#
# # Get the column values as lists
# list1 = csv1['final_del_0.1_clus'].tolist()
# list2 = csv1['logic_0.1'].tolist()
# names_not_in_list2 = [name for name in list1 if name not in list2 and isinstance(name, str) and name.strip() != ""]
#
# if names_not_in_list2:
#     print("Names not in List 2:")
#     for name in names_not_in_list2:
#         print(name)
# else:
#     print("All valid names in List 1 are present in List 2")
#################################################################################################
# import pandas as pd
#
# # Read the first CSV file
# df1 = pd.read_csv(r"C:\Users\User\Documents\Elkin_non_ag_check.csv")
#
# # Read the second CSV file
# df2 = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\zonal_stats_CI5_poria_rasters1.csv")
#
# # Merge the two dataframes based on the "name" column
# merged_df = pd.merge(df1, df2[['CommonLand', '0=0 sum', '0=0 major' ]], on='CommonLand', how='left')
# print(merged_df)
# # Rename the 'crop' column to 'new_column'
# #merged_df.rename(columns={'crop_name': 'crop_name'}, inplace=True)
#
# # # Save the merged dataframe back to the first CSV file
# merged_df.to_csv(r"C:\Users\User\Documents\Elkin_non_ag_check_merged_poria_ras.csv", index=False)
################################################################################################# - gpkg from f labeled
# import geopandas as gpd
#
# # Read the GeoJSON file into a GeoDataFrame
# gdf = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\New_all_proag_2023_clus_V5a.gpkg")
#
# # Filter the GeoDataFrame based on the column condition
# filtered_gdf = gdf[gdf['CI8'] == 'f']
# print(len(filtered_gdf))
# # Save the filtered GeoDataFrame to a new GeoJSON file
# filtered_gdf.to_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C8\CI8_proag_f_file.gpkg", driver='GPKG')
#################################################################################################
# import geopandas as gpd
# 
# # Read the first GeoJSON file into a GeoDataFrame
# gdf1 = gpd.read_file(r"C:\Users\User\Documents\FMH_2023\FMH_clus.geojson")
# 
# # Read the second GeoJSON file into a GeoDataFrame
# gdf2 = gpd.read_file(r"C:\Users\User\Documents\FMH_2023\FMH_InSeason\CI3\filtered_CI3_f_file_manual_shva.gpkg")
# # Filter the GeoDataFrame based on the condition CI6 == 'Y6'
# filtered_gdf2 = gdf2[gdf2['CI6'] == 'Y6']
# # Update the value in gdf1 based on matching names
# gdf1.loc[gdf1['CommonLand'].isin(filtered_gdf2['CommonLand']), 'CI6'] = 'Y6'
# 
# 
# # Save the updated GeoDataFrame to a new GeoJSON file
# gdf1.to_file(r"C:\Users\User\Documents\FMH_2023\FMH_clus_V2.gpkg", driver='GPKG')
#################################################################################################
# import geopandas as gpd
#
# # Read the first GeoJSON file
# data1 = gpd.read_file(r"C:\Users\User\Documents\FMH_2023\FMH_clus_V2.gpkg")
#
# # Read the second GeoJSON file
# data2 = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\New_all_proag_2023_clus_V2.gpkg")
#
# # Extract the 'name' column from both datasets
# names1 = data1['CommonLand']
# names2 = data2['CommonLand']
#
# # Find the duplicates based on the 'name' column
# duplicates = names1[names1.isin(names2)]
#
# # Print the duplicate names
# print(duplicates)
# print(len(duplicates))
#
# #################################################################################################
# import pandas as pd
# import geopandas as gpd
#
# # Read the CSV file
# csv_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_yoni_logic.csv"
# df = pd.read_csv(csv_file)
#
# # # Filter rows based on cropid column
# # filtered_df = df[df['crop_id_confidence_text'] == 'Do not Push']
#
# # Create a list of values from the name column
# name_list = df['logic non ags'].tolist()
#
# # Read the GeoJSON file
# geojson_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\New_all_proag_2023_clus_V3.gpkg"
# gdf = gpd.read_file(geojson_file)
# print(len(gdf))
#
# # Filter GeoJSON rows based on the name_list
# filtered_gdf = gdf[gdf['CommonLand'].isin(name_list)]
# print(len(filtered_gdf))
#
#
# # Save filtered data to GeoPackage file
# output_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_non_ags_clus.gpkg"
# filtered_gdf.to_file(output_file, driver='GPKG')
#
# # Extract the first two characters from the "tile" column
# filtered_gdf['tile_prefix'] = filtered_gdf['tile'].str[:2]
#
# # Count the occurrences of each unique value
# tile_counts = filtered_gdf['tile_prefix'].value_counts()
#
# # Print the unique values and their counts
# for tile_prefix, count in tile_counts.items():
#     print(f"{tile_prefix}: {count}")
# # Calculate the sum of all counts
# total_count = tile_counts.sum()
#
# # Print the total count
# print("Total count:", total_count)
# #################################################################################################
# import pandas as pd
#
# # Read the Excel file
# excel_file = r"C:\Users\User\Downloads\CI6_proAg_delVSlogic.csv"
# df = pd.read_csv(excel_file)
#
# # Get unique values from column 1 and column 2
# column1_values = set(df['del'])
# column2_values = df['logic']
#
# # Find names in column 2 that are not in column 1
# names_not_in_column1 = column2_values[~column2_values.isin(column1_values)]
# print(len(names_not_in_column1))
# # Print the names not in column 1
# for name in names_not_in_column1:
#     print(name)
# #################################################################################################

# import geopandas as gpd
#
# # Step 1: Read the GeoPackage file
# file_path = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\tiles_approved_until_CI7.gpkg"
# gdf = gpd.read_file(file_path)
# print(len(gdf))
# # Step 2: Extract unique names from the "name" column and store them in a list
# names_list = list(set(gdf["Name"].tolist()))
# print("Unique Names:", names_list)
# print("Number of Unique Names:", len(names_list))
#
# # Step 4: Save the filtered GeoDataFrame to a new shapefile
# filtered_shapefile_path = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\Combined_us_grid_clus_2023\us_grid_proag_FMH_2023.shp"
# gdf2 = gpd.read_file(filtered_shapefile_path)
# print(gdf2)
# filtered_gdf = gdf2[~gdf2["Name"].isin(names_list)]
# print(filtered_gdf)
# print(len(filtered_gdf))
# names_list2 = list(set(filtered_gdf["Name"].tolist()))
# print(names_list2)
# filtered_gdf.to_file(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\Combined_us_grid_clus_2023\tile_not_approved_until_CI7.gpkg", driver='GPKG')
# #################################################################################################
# import pandas as pd
# import numpy as np
# # Step 1: Read the DataFrame from the CSV file
#data = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\crops_acres_df_20230725.csv")
# Step 2: Define a function to extract the value of "crop name" from the second dictionary
# def get_crop_name(row):
#     crop_list = eval(row["crop_identification"])  # Convert the string representation of list of dictionaries to a Python list
#     if len(crop_list) >= 2:  # Check if there are at least two dictionaries in the list
#         return crop_list[0].get("crop_code") # Return the value of "crop name" in the second dictionary
#     else:
#         return None
#
# # Step 3: Apply the function to create a new column with the values of "crop name" from the second dictionary
# data["CDL_forecast"] = data.apply(get_crop_name, axis=1)
# old_values = [101, 102, 81, 11, 41, 21]  # Replace these old values
# new_values = ['Other', 'NonAg', 'Soybeans', 'Wheat', 'Corn', 'Cotton']  # With these new values
# replacement_dict = {'101': "Other", '102': "NonAg", '81': "Soybeans",'11': 'Wheat', '41': 'Corn', '21': 'Cotton'}
# # Step 3: Use the replace method to replace the old values with the new values
# data["CDL_forecast"].replace(replacement_dict, inplace=True)
# # Step 4: Display the updated DataFrame with the new column
# print(data["CDL_forecast"])
# # #####################################################################################################################
#
forecast=pd.read_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\ProAg\ProAg_AR\ProAg AR\ProAg's AR data - MpciPolicyCluSummary_2023_Planted_09112023.csv")
size= gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_Proag_clus_geojson.geojson")
report =pd.read_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\ProAg\ProAg_AR\ProAg AR\ProAg's PW AR data.csv")
name_size_mapping = dict(zip(forecast["CommonLandUnitId"], forecast['ml_model_code']))
forecast["ml_model"] = forecast["logic non ags"].map(name_size_mapping)
print(forecast)
print(forecast.info())
forecast.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_yoni_logic_forecast_forecast_V2.csv")
# #
# # Define the columns you want to map from 'size' GeoDataFrame to 'forecast' DataFrame
# columns_to_map = ['CommonLand', 'CI1', 'CI2', 'CI3', 'CI4', 'CI5', 'CI6', 'CI7']
#
# # Create a dictionary with multiple columns as keys and their corresponding mapping as values
# mapping_dict = {}
# for column in columns_to_map:
#     mapping_dict[column] = dict(zip(size["CommonLand"], size[column]))
#
# # Apply the mapping to the 'forecast' DataFrame for each column in 'columns_to_map'
# for column in columns_to_map:
#     forecast[column + "_ml_model"] = forecast['logic non ags'].map(mapping_dict[column])
#
# columns_to_map2 = ['cluid', 'crops_acres_df_20230529', 'crops_acres_df_20230612', 'crops_acres_df_20230619', 'crops_acres_df_20230627', 'crops_acres_df_20230704', 'crops_acres_df_20230711', 'crops_acres_df_20230725']
# mapping_dict2 = {}
# for column2 in columns_to_map2:
#     mapping_dict2[column2] = dict(zip(report["cluid"], report[column2]))
#
# # Apply the mapping to the 'forecast' DataFrame for each column in 'columns_to_map'
# for column2 in columns_to_map2:
#     forecast[column2 + "_main_crop"] = forecast['logic non ags'].map(mapping_dict2[column2])
# # Display the updated 'forecast' DataFrame
# print(forecast)
# print(forecast.info())
# forecast.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_to_sarai.csv")
# # #####################################################################################################################
# import pandas as pd
# import geopandas as gpd
#
# # Step 1: Read the CSV file and filter by model and date
# data = pd.read_csv(r"C:\Users\User\Downloads\proag_pre_deliver_logic_2023-07-27.csv")
# filtered_data = data[(data["ci_ml_model_code"] == "f")]
# print(len(filtered_data))
# filtered_data = filtered_data[(filtered_data["match_flag"] == "no forecast") | (filtered_data["match_flag"] == "no match")]
# # Step 2: Create a list from the "name" column of the filtered CSV data
# names_list = filtered_data["clu_id"].tolist()
# print(len(names_list))
# # Step 3: Read the GeoJSON file as a GeoDataFrame
# gdf = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_Proag_clus_geojson.geojson")
#
# # Step 4: Filter the GeoDataFrame using the names list
# filtered_gdf = gdf[gdf["CommonLand"].isin(names_list)]
#
# # Step 5: Display the filtered GeoDataFrame
# print(filtered_gdf)
# filtered_gdf.to_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\f_clus_no_match.gpkg", driver='GPKG')
# # #####################################################################################################################

# import csv
# import random
#
# def random_names_from_csv(csv_file, column_name, num_names=20):
#     with open(csv_file, 'r') as file:
#         csv_reader = csv.DictReader(file)
#         names = [row[column_name] for row in csv_reader]
#         random_names = random.sample(names, num_names)
#     return random_names
#
# # Usage example
# csv_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C8\B8_clus_clips.csv"
# column_to_pick_names_from = 'name'  # Replace with the column name from your CSV file
# random_names = random_names_from_csv(csv_file_path, 'clu_id', num_names=20)
#
# print(random_names)
# print(len(random_names))
# import geopandas as gpd
# import random
#
# def random_names_from_geopackage(geopackage_file, num_names=20):
#     gdf = gpd.read_file(geopackage_file)
#     names = gdf['CommonLand'].tolist()
#     random_names2 = random.sample(names, num_names)
#     return random_names2
#
# # Usage example
# geopackage_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\New_all_proag_2023_clus_V3.gpkg"
# random_names2 = random_names_from_geopackage(geopackage_file_path, num_names=20)
#
# print(random_names2)
# print(len(random_names2))
# gdf = gpd.read_file(geopackage_file_path)
# gdf.loc[gdf['CommonLand'].isin(random_names), 'CI7'] = 'B8'
# name_list = random_names+random_names2
# print(name_list)
# print(len(name_list))
#
#
# filtered_gdf = gdf[gdf['CommonLand'].isin(name_list)]
# print(filtered_gdf)
# print(len(filtered_gdf))
# filtered_gdf.to_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C8\B8_test.gpkg", driver='GPKG')
# # #####################################################################################################################

#
# import pandas as pd
#
# # Example usage
# csv_file_path = r"C:\Users\User\Downloads\crops_acres_df_20230803.csv"
#
# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv(csv_file_path)
#
# # Function to extract crop code and acres from the list of dictionaries
# def extract_values(crop_id_list):
#     if pd.notna(crop_id_list):
#         crop_data = eval(crop_id_list)
#         crop_codes = [d['crop_code'] for d in crop_data]
#         acres_values = [d['identified_acres'] for d in crop_data]
#     else:
#         crop_codes = []
#         acres_values = []
#     return crop_codes, acres_values
#
# # Split the dictionaries and add new columns
# df[['crop_code']] = pd.DataFrame(df['crop_identification'].apply(extract_values).tolist(), index=df.index)
# df[['acres']] = pd.DataFrame(df['crop_identification'].apply(extract_values).tolist(), index=df.index)
#
# # Drop the original 'crop_id' column
# df.drop(columns=['crop_id'], inplace=True)
#
# # Split the lists in each cell into separate columns
# df = df.join(df['crop_code'].apply(pd.Series).add_prefix('crop_code_'))
# df = df.join(df['crop_identification'].apply(pd.Series).add_prefix('crop_identification_'))
#
# # Drop the temporary 'crop_code' and 'acres' columns
# df.drop(columns=['crop_code', 'acres'], inplace=True)
#
# print(df)


#
# data = pd.read_csv(r"C:\Users\User\Downloads\crops_acres_df_20230803.csv")
# def get_crop_name2(row):
#     crop_list = eval(row["crop_identification"])  # Convert the string representation of list of dictionaries to a Python list
#     if len(crop_list) >= 2:  # Check if there are at least two dictionaries in the list
#         return crop_list[1].get("crop_code") # Return the value of "crop name" in the second dictionary
#     else:
#         return None
#
# # Step 3: Apply the function to create a new column with the values of "crop name" from the second dictionary
# data["Second_Crop_code"] = data.apply(get_crop_name2, axis=1)
#
# def get_crop_name2(row):
#     crop_list = eval(row["crop_identification"])  # Convert the string representation of list of dictionaries to a Python list
#     if len(crop_list) >= 2:  # Check if there are at least two dictionaries in the list
#         return crop_list[1].get("identified_acres") # Return the value of "crop name" in the second dictionary
#     else:
#         return None
#
# # Step 3: Apply the function to create a new column with the values of "crop name" from the second dictionary
# data["Second_identified_acres"] = data.apply(get_crop_name2, axis=1)
# print(data)
# data.to_csv(r"C:\Users\User\Downloads\crops_acres_df_20230803_V2.csv")
# # #####################################################################################################################
#
# # Read the GeoJSON file into a GeoDataFrame
# gdf = gpd.read_file(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\New_all_proag_2023_clus_V5a.gpkg")
#
# # Filter the GeoDataFrame based on the column condition
# print('f: ', len(gdf[gdf['CI8'] == 'f']))
# print('CI1: ', len(gdf[gdf['CI8'] == 'Y1']))
# print('CI2: ', len(gdf[gdf['CI8'] == 'Y2']))
# print('CI3: ', len(gdf[gdf['CI8'] == 'Y3']))
# print('CI4: ', len(gdf[gdf['CI8'] == 'Y4']))
# print('CI5: ', len(gdf[gdf['CI8'] == 'Y5']))
# print('CI6: ', len(gdf[gdf['CI8'] == 'Y6']))
# print('CI7: ', len(gdf[gdf['CI8'] == 'Y7a']))
# print('CI8: ', len(gdf[gdf['CI8'] == 'Y8a']))
# # #####################################################################################################################

# import geopandas as gpd
#
# #Replace 'input.geojson' with the path to your GeoJSON file
# input_geojson = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C8\CI8_proag_clus_v1_geojson.geojson"
#
# # Read GeoJSON data using GeoPandas
# gdf = gpd.read_file(input_geojson)
#
# csv_file_path = r"C:\Users\User\Desktop\sorted\40_clus_sorted_non_ag_forecast.csv"
# #
# # # Read the CSV file into a pandas DataFrame
# df = pd.read_csv(csv_file_path)
# names_to_filter = df['CommonLand'].tolist()
# print(len(names_to_filter))
# filtered_gdf = gdf[gdf['CommonLand'].isin(names_to_filter)]
# print(len(filtered_gdf))
#
# # Save to GeoJSON
# filtered_gdf.to_file(r"C:\Users\User\Desktop\sorted\40clus_sorted_nonags.geojson", driver='GeoJSON')
#
# csv_file2_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\All_proag_clus_PWid_CommonLand_cdl_21_forecast.csv"
# df2 = pd.read_csv(csv_file2_path)
# filtered_df2 = df2[df2['CommonLand'].isin(names_to_filter)]
# print(len(filtered_df2))
# filtered_df2.to_csv(r"C:\Users\User\Desktop\sorted\sorted_non_ag_forecast.csv")
# import os
# import shutil
#
# source_folder = r"C:\Users\User\Desktop\sorted\sorted_all\sorted"  # Replace with the path to your source folder
# destination_folder = r"C:\Users\User\Desktop\sorted\sorted1\sorted_nonags"  # Replace with the path to your destination folder
#
# # Ensure the destination folder exists
# os.makedirs(destination_folder, exist_ok=True)
#
# for file_name in names_to_filter:
#     source_path = os.path.join(source_folder, file_name+'.tif')
#     destination_path = os.path.join(destination_folder, file_name+'.tif')
#
#     if os.path.exists(source_path):
#         shutil.copy2(source_path, destination_path)
#         print(f"Copied: {file_name}")
#     else:
#         print(f"File not found: {file_name}")
#
# print("Copying complete.")
# # #####################################################################################################################
#
# file_path = r"C:\Users\User\Desktop\sorted\40clus_sorted_nonags_geojson.geojson"
#
# # Find the position of the substring '_geojson' in the file path
# index = file_path.find('_geojson')
#
# if index != -1:
#     # Insert '_updated' before the substring '_geojson'
#     new_file_path = file_path[:index] + '_updated' + file_path[index:]
#
#     print("Original File Path:", file_path)
#     print("Modified File Path:", new_file_path)
# else:
#     print("'_geojson' not found in the file path.")

# for feature in geojson_data['features']:
#     print(feature)
#     properties = feature['properties']
#     print(properties)
#     clu_name = properties['CommonLand']
#     last_key = list(properties.keys())[-1]
#     last_value = properties[last_key]
#     print(last_key)
#     print(last_value)

# CS_forecast = r"C:\Users\User\Desktop\sorted\nonags_sorted_no_nonag_as_forecast.csv"
# df = pd.read_csv(CS_forecast)
# list1 = df['CommonLand'].to_list()
# print(list1, 'list1')
# non_ag_after_code = r"C:\Users\User\Desktop\sorted\csv_nonags_nomatch_from_stat_code.csv"
# df2 = pd.read_csv(non_ag_after_code)
# list2 = df2['CommonLand'].to_list()
# print(list2 ,'list2')
# print(len(list1))
# print(len(list2))
#
# # Find names that are unique to each list
# unique_names_list1 = [name for name in list1 if name not in list2]
# unique_names_list2 = [name for name in list2 if name not in list1]
#
# # Print the unique names
# print("Unique names in list1:", unique_names_list1)
# print(len(unique_names_list1))
# print("Unique names in list2:", unique_names_list2)