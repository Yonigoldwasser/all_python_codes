import os
import pandas as pd
import geopandas as gpd
import numpy as np
import pandas as pd

# # Step 1: Read the first CSV file containing the name-value pairs
# file1 = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_yoni_logic.csv"
# df1 = pd.read_csv(file1)
#
# # Step 2: Read the second CSV file containing the name-value pairs
# file2 = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\forecast_2023_delivery.csv"
# df2 = pd.read_csv(file2)
#
# # Step 3: Create a mapping dictionary from the second DataFrame
# name_value_mapping = dict(zip(df2["CommonLand"], df2["crop_name"]))
#
# # Step 4: Create a new column in the first DataFrame and fill it with values from the mapping
# df1["value_from_file2"] = df1["logic non ags"].map(name_value_mapping)
#
# # Step 5: Display the updated DataFrame with the new column
# print(df1)
# output_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_yoni_logic_forecast.csv"
# df1.to_csv(output_file)

#proag
cdl=pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\All_proag_clus_PWid_for_CS_forecast_no_commo_cdl_21.csv")
# vec=pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\ProAg_data.csv")

cdl['crop_code']=cdl['cdl'].map({1:41, 2:21, 5:81,12:41, 13:41, 23:11,26:81, 225:41, 226:41, 237:41,  238:21, 239:21, 241:81, 254:81})
cdl['crop_code']=cdl['crop_code'].fillna(101)
cdl.loc[cdl['cdl'].isin([61,63,64,65,82,83,87,88,
                                  111,112,121,122,123,124,131,
                                  141,142,143,152,176,190,195]), 'crop_code']=102

cdl['crop_name']=cdl['crop_code'].map({41:'Corn', 21:'Cotton', 81:'Soybeans', 11:'Wheat'})
cdl['crop_name']=cdl['crop_name'].fillna('Other')
cdl.loc[cdl['cdl'].isin([61,63,64,65,82,83,87,88,
                                  111,112,121,122,123,124,131,
                                  141,142,143,152,176,190,195]), 'crop_name']='NonAg'

print(cdl)
cdl.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\All_proag_clus_PWid_for_CS_forecast_no_commo_cdl_21.csv")

# # Step 3: Create a mapping dictionary from the second DataFrame
# name_value_mapping = dict(zip(cdl["PWid"], cdl["crop_name"]))
#
# # Step 4: Create a new column in the first DataFrame and fill it with values from the mapping
# vec["cropscape_forecast"] = vec["CommonLand"].map(name_value_mapping)
# print(vec)

#####################################################################################################################
# data = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\crops_acres_df_20230725.csv")
#
# def get_crop_name2(row):
#     crop_list = eval(row["crop_identification"])  # Convert the string representation of list of dictionaries to a Python list
#     if len(crop_list) >= 2:  # Check if there are at least two dictionaries in the list
#         return crop_list[0].get("crop_code") # Return the value of "crop name" in the second dictionary
#     else:
#         return None
#
# # Step 3: Apply the function to create a new column with the values of "crop name" from the second dictionary
# data["Second_Crop_Name"] = data.apply(get_crop_name2, axis=1)
# old_values = [101, 102, 81, 11, 41, 21]  # Replace these old values
# new_values = ['Other', 'NonAg', 'Soybeans', 'Wheat', 'Corn', 'Cotton']  # With these new values
# replacement_dict = {'101': "Other", '102': "NonAg", '81': "Soybeans",'11': 'Wheat', '41': 'Corn', '21': 'Cotton'}
# # Step 3: Use the replace method to replace the old values with the new values
# data["Second_Crop_Name"].replace(replacement_dict, inplace=True)
# # Step 4: Display the updated DataFrame with the new column
#
# #####################################################################################################################
# name_value_mapping = dict(zip(data["clu_id"], data["Second_Crop_Name"]))
#
# # Step 4: Create a new column in the first DataFrame and fill it with values from the mapping
# vec["CI7_crop_name_2"] = vec["logic non ags"].map(name_value_mapping)
# print(vec)

# vec.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C7\CI7_proag_nonags_yoni_logic_forecast_forecast.csv")
#####################################################################################################################

