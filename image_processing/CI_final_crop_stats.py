import pandas as pd
import numpy as np
import os
import ast

# Folder path containing the CSV files
folder_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CIs_dataframes"
# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
print(csv_files)
# Create an empty DataFrame
result_df = pd.DataFrame()
result = []
names = []
print(names)

# Process each CSV file
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    df_name = csv_file[:-4]
    print(df_name)
    if df_name == 'crops_acres_df_20230501_forecast':
        # Remove duplicates based on specific columns
        df = df.drop_duplicates(subset=df.columns[0])
        cluid_values = df['clu_id'].tolist()
        cropid_values = df['crop_identification'].tolist()
        replace_dict = {'Corn': '41', 'Cotton': '21', 'Wheat': '11', 'Soybeans': '81', 'Other': '101', 'Non Ag': '102'}
        #print(df)

        df = df.replace(replace_dict)
        #print(df)
    else:
        # filter out the forcast clus
        #df = df.loc[df['ml_model_code'] != 'f']
        # Extract cluid and cropid columns
        cluid_values = df['clu_id'].tolist()
        cropid_values = [eval(crop_dict)[0]['crop_code'] for crop_dict in df['crop_identification']]
    if df_name not in names:
        names.append(df_name)
    df_name = pd.DataFrame(columns=['cluid', 'crop_code'])
    # Add cluid and crop_code values to the result DataFrame
    df_name = df_name.append(pd.DataFrame({'cluid': cluid_values, 'crop_code': cropid_values}), ignore_index=True)
    clus_amount_last_CI = df_name.shape[0]
    result.append(df_name)
print(df)
print(df.head())
print(df.info())

# Create an empty DataFrame to store the aggregated results
result_df = pd.DataFrame()

# Iterate over each DataFrame and its corresponding column name
for df, column_name in zip(result, names):
    # Aggregate the crop values for each name
    aggregated_df = df.groupby('cluid')['crop_code'].agg(list).reset_index()
    # Rename the 'crop' column with the corresponding column name
    aggregated_df.rename(columns={'crop_code': column_name}, inplace=True)
    # Merge the aggregated results with the previous results
    if result_df.empty:
        result_df = aggregated_df
    else:
        result_df = result_df.merge(aggregated_df, on='cluid', how='outer')

replace_dict = {'41': 'Corn', '21': 'Cotton', '11': 'Wheat', '81': 'Soybeans', '101': 'Other', '102': 'Non Ag'}
# Fill NaN values with empty lists
result_df = result_df.fillna('')
for column in result_df.columns[1:]:
    result_df[column] = result_df[column].apply(lambda x: str(x)[1:-1])

# Print the resulting DataFrame
result_df = result_df.apply(lambda x: x.str.replace("'", ""))
result_df = result_df.replace(replace_dict)
#
# Count the number of non-empty values in each row for the specific columns
# Get the specific columns from the second column to the end
specific_columns = result_df.columns[2:]
result_df['CIs_value_count'] = result_df[specific_columns].apply(lambda x: x[x != ''].count(), axis=1)


# Create a new column with default value 'Yes'
result_df['ALL_CIs_Match_forecast'] = 'Yes'
result_df['Last_CI_value_Match_forecast'] = 'Yes'

print(result_df.info())
# Iterate over each row in the DataFrame
for index, row in result_df.iterrows():
    # Get the value in the second column
    match_value = row[1]
    # Check if all values from the second column onwards match the value in the second column
    #if not all(row[2:-3] == match_value) and match_value != "":
    if match_value != "" and not all(x == match_value for x in row[2:-3] if x != ""):
        # If any value doesn't match, update the 'Match_All' column to 'No'
        result_df.at[index, 'ALL_CIs_Match_forecast'] = 'No'

    # Update if match_value is empty
    if match_value == "":
        result_df.at[index, 'ALL_CIs_Match_forecast'] = 'No'
        result_df.at[index, 'Last_CI_value_Match_forecast'] = 'No'
    else:
        if not row[-4] == match_value:
            result_df.at[index, 'Last_CI_value_Match_forecast'] = 'No'


# Count the occurrences of 'Yes' in the 'Match_All' column
all_yes_count = (result_df['ALL_CIs_Match_forecast'] == 'Yes').sum()
last_yes_count = (result_df['Last_CI_value_Match_forecast'] == 'Yes').sum()
#
#
# Calculate the percentage relative to the number of rows in the first column
percent_value = (all_yes_count / result_df.shape[0]) * 100
result_df['ALL_CIs_Match_percent'] = ''
result_df.at[0, 'ALL_CIs_Match_percent'] = percent_value
# Calculate the percentage relative to the number of rows in the first column
last_percent_value = (last_yes_count / result_df.shape[0]) * 100
result_df['Last_CI_value_Match_forecast_percent'] = ''
result_df.at[0, 'Last_CI_value_Match_forecast_percent'] = last_percent_value


subset_columns = result_df.columns[2:-5]

# Calculate the most frequent value for each row
most_frequent_values2 = result_df[subset_columns].apply(
    lambda x: x.value_counts().idxmax() if (x.nunique() > 1 and x.value_counts().idxmax() not in ["", float("nan")])
    else x.value_counts().index[1] if len(x.value_counts()) > 1
    else x.value_counts().idxmax() if len(x.value_counts()) == 1 and x.value_counts().idxmax() not in ["", float("nan")]
    else None,
    axis=1
)

insert_position_All_Same_Value = len(result_df.columns) - 4
# if all values of the classification are the same
All_Same_Value = result_df.apply(
    lambda row: 'yes' if len(set(row[subset_columns].replace('', float('nan')).dropna())) <= 1 else 'no',
    axis=1
)
# If all values in the row are "", update 'All_Same_Value' column to 'no'
result_df.insert(insert_position_All_Same_Value, 'All_Same_Value', All_Same_Value)
result_df.loc[result_df[subset_columns].eq("").all(axis=1), 'All_Same_Value'] = 'no'
########################################################################################
insert_position = len(result_df.columns) - 4
result_df.insert(insert_position, 'Most_frequent_value', most_frequent_values2)
Last_CI_value_by_approved_clus_percent = (last_yes_count / clus_amount_last_CI) * 100
result_df['Last_CI_value_by_approved_clus_percent'] = ''
result_df.at[0, 'Last_CI_value_by_approved_clus_percent'] = Last_CI_value_by_approved_clus_percent

# add ml_model to df
last_csv_file = csv_files[-1]
file_path = os.path.join(folder_path, last_csv_file)
last_csv_file_df = pd.read_csv(file_path)
ml_model_size_mapping = dict(zip(last_csv_file_df["clu_id"], last_csv_file_df['ml_model_code']))
result_df["last_ml_model"] = result_df["cluid"].map(ml_model_size_mapping)

# dataframe of all values that were calculated before
values_for_calc = {'Number of clus that match forecast in all CIs': all_yes_count, 'Number of clus that match forecast in latest CI': last_yes_count,
                   'number of clu approved latest CI': clus_amount_last_CI, 'Total clu number': result_df.shape[0]}

values_for_calc_df = pd.DataFrame(list(values_for_calc.items()), columns=['Variable', 'Value']).reset_index(drop=True)
print(values_for_calc_df)
final_df = pd.concat([result_df, values_for_calc_df], axis=1)

# Create a new DataFrame to store the sums of matching values to forecast for each column (CI)
sums_df = pd.DataFrame(columns=['Column', 'Sum'])

# Iterate through each column
for col_name in final_df.columns[2:10]:
    matching_sum = df.loc[df[col_name] == df.columns[1], col_name].sum()
    sums_df = sums_df.append({'Column': col_name, 'Sum': matching_sum}, ignore_index=True)
# # # Export the DataFrame to a CSV file
# final_df = pd.concat([final_df, sums_df], axis=1)
# output_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C9\CI9_final_with_forecast_report.csv"
# final_df.to_csv(output_file, index=False)

