# import pandas as pd
#
# # Load the CSV file
# df = pd.read_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\proag_2023_season_clus_CI.csv")
# replacement_dict = {102: 'nonag', 41: 'corn', 21: 'cotton', 81: 'soybeans', 11: 'wheat', 101: 'other', 0: 'NoData'}
# for col in df.columns[22:-1]:  # Remember, indexing in Python is 0-based and the end of the range is exclusive
#     df[col] = df[col].replace(replacement_dict)
#
# last_column_name = df.columns[-1]
#
# nonag = [61,63,64,65,82,83,87,88,111,112,121,122,123,124,131,141,142,143,152,176,190,195]
# # Replace the values
# df[last_column_name] = df[last_column_name].replace(nonag, 'nonag')
#
# cdl_values = {1:'corn', 2:'cotton', 5:'soybeans',12:'corn', 13:'corn', 23:'wheat',26:'soybeans', 225:'corn', 226:'corn', 237:'corn',  238:'cotton', 239:'cotton', 241:'soybeans', 254:'soybeans'}
# df[last_column_name] = df[last_column_name].replace(cdl_values)
#
# # Function to determine if a value is numeric
# def replace_if_numeric(value):
#     if isinstance(value, (int, float)):
#         return 'other'
#     return value
#
# # Replace numeric values in the column
# df[last_column_name] = df[last_column_name].apply(replace_if_numeric)
#
# print(df)
# # Find the number of columns
# num_columns = len(df.columns)
#
# # Last column
# last_column = df.iloc[:, -1]
#
# # Iterate over the columns starting from the third one and compare its values to the last column
# matches = {}  # This dictionary will store the column name and the number of matches
#
# for col in df.columns[22:num_columns-1]:  # We exclude the last column itself from comparison
#     # Count matches between the current column and the last column
#     count = (df[col] == last_column).sum()
#     matches[col] = count
#
# print('matches',matches)
# #
# unique_values = {}
# selected_columns = df.columns[22:]
# # Count unique values for the selected columns
# # Count occurrences of each unique value for the selected columns
# value_counts_per_column = {col: df[col].value_counts(ascending=False) for col in selected_columns}
# for col, counts in value_counts_per_column.items():
#     unique_values[col] = counts.to_dict()
#
# print('unique_values',unique_values)
# # # Count values 'f' or 'fa' for columns indexed from 13 to 22
# # selected_columns = df.columns[13:22]
# # count_values_f = df[selected_columns].apply(lambda col: col[col.isin(['f', 'fa'])].count())
# # print(count_values_f)
# # Merge dictionaries
# matches_df = pd.DataFrame.from_dict(matches, orient='index')
# unique_values_df = pd.DataFrame.from_dict(unique_values, orient='index')
# print(matches_df)
# print(unique_values_df)
#
# result = pd.concat([df, matches_df, unique_values_df], axis=1)
# # result.to_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\proag_2023_season_clus_CI_values.csv", index=False)

##############################################################################################################################################################
import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\proag_2023_season_clus_CI.csv")
replacement_dict = {102: 'nonag', 41: 'corn', 21: 'cotton', 81: 'soybeans', 11: 'wheat', 101: 'other', 0: 'NoData'}
for col in df.columns[22:-1]:  # Remember, indexing in Python is 0-based and the end of the range is exclusive
    df[col] = df[col].replace(replacement_dict)

nonag = [61,63,64,65,82,83,87,88,111,112,121,122,123,124,131,141,142,143,152,176,190,195]
# Replace the values
df.iloc[: ,-2] = df.iloc[: ,-2].replace(nonag, 'nonag')

cdl_values = {1:'corn', 2:'cotton', 5:'soybeans',12:'corn', 13:'corn', 23:'wheat',26:'soybeans', 225:'corn', 226:'corn', 237:'corn',  238:'cotton', 239:'cotton', 241:'soybeans', 254:'soybeans'}
df.iloc[: ,-2] = df.iloc[: ,-2].replace(cdl_values)

# Function to determine if a value is numeric
def replace_if_numeric(value):
    if isinstance(value, (int, float)):
        return 'other'
    return value

# Replace numeric values in the column
df.iloc[: ,-2] = df.iloc[: ,-2].apply(replace_if_numeric)

# Find the number of columns
num_columns = len(df.columns)
df.iloc[:, -1] = df.iloc[:, -1].astype(str).str.lower()
# Last column
last_column = df.iloc[:, -1]

# Iterate over the columns starting from the third one and compare its values to the last column
matches = {}  # This dictionary will store the column name and the number of matches

for col in df.columns[22:num_columns]:  # We exclude the last column itself from comparison
    # Count matches between the current column and the last column
    count = (df[col] == last_column).sum()
    matches[col] = count

print('matches',matches)
#
unique_values = {}
selected_columns = df.columns[22:]
# Count unique values for the selected columns
# Count occurrences of each unique value for the selected columns
value_counts_per_column = {col: df[col].value_counts(ascending=False) for col in selected_columns}
for col, counts in value_counts_per_column.items():
    unique_values[col] = counts.to_dict()

print('unique_values',unique_values)
# # Count values 'f' or 'fa' for columns indexed from 13 to 22
# selected_columns = df.columns[13:22]
# count_values_f = df[selected_columns].apply(lambda col: col[col.isin(['f', 'fa'])].count())
# print(count_values_f)
# Merge dictionaries
matches_df = pd.DataFrame.from_dict(matches, orient='index')
unique_values_df = pd.DataFrame.from_dict(unique_values, orient='index')
print(matches_df)
print(unique_values_df)
counts = df['lilian_forecast'].value_counts()
print(counts)
counts = pd.DataFrame(counts)
print(counts)

# result = pd.concat([df, matches_df, unique_values_df], axis=1)
# result.to_csv(r"C:\Users\User\Documents\ProAg_FMH_CC_2023\2023_season_summary\proag_2023_season_clus_CI_values.csv", index=False)