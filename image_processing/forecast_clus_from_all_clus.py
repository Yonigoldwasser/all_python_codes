import pandas as pd

# Read the CSV files
main_file = pd.read_csv(r"C:\Users\User\Downloads\proag_final_delivery1.csv")
filter_file = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C5\CI5_difference_forecast_clus.csv")

# Get the list of rows from the filter file where column 'x' is empty
#filtered_rows = filter_file[filter_file['crops_acres_df_20230704'].isnull()]
filtered_rows = filter_file['cluid']
print(filtered_rows)
# Filter the main file based on the filtered rows
filtered_data = main_file[main_file['usda_clu_id'].isin(filtered_rows)] #['cluid'])]

# Save the filtered data to a new CSV file
# # Save the filtered data to a new CSV file
filtered_data.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C5\CI5_difference_final delivery_forecast_clus.csv", index=False)
