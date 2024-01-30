import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CI_by_area_comparison\Y9_zonal_stats_comparison.csv")
replacement_dict = {102: 'nonag', 41: 'corn', 21: 'cotton', 81: 'soybeans', 11: 'wheat', 101: 'other', 0: 'NoData'}
for col in df.columns[-2:]:  # Remember, indexing in Python is 0-based and the end of the range is exclusive
    df[col] = df[col].replace(replacement_dict)

CDL_forecast = pd.read_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\All_proag_clus_PWid_CommonLand_cdl_21_forecast.csv")
forecast_mapping = dict(zip(CDL_forecast["CommonLand"], CDL_forecast['cdl']))
df["cdl_forecast"] = df["CommonLand"].map(forecast_mapping)


nonag = [61,63,64,65,82,83,87,88,111,112,121,122,123,124,131,141,142,143,152,176,190,195]
# Replace the values
df.iloc[:,-1].replace(nonag, 'nonag')
df.loc[df['cdl_forecast'].isin([61,63,64,65,82,83,87,88,
                                  111,112,121,122,123,124,131,
                                  141,142,143,152,176,190,195]), 'cdl_forecast']='nonag'
cdl_values = {1:'corn', 2:'cotton', 5:'soybeans',12:'corn', 13:'corn', 23:'wheat',26:'soybeans', 225:'corn', 226:'corn', 237:'corn',  238:'cotton', 239:'cotton', 241:'soybeans', 254:'soybeans'}
df["cdl_forecast"] = df["cdl_forecast"].replace(cdl_values)

# Function to determine if a value is numeric
def replace_if_numeric(value):
    if isinstance(value, (int, float)):
        return 'other'
    return value

# Replace numeric values in the column
df["cdl_forecast"] = df["cdl_forecast"].apply(replace_if_numeric)

# df.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CI_by_area_comparison\Y9_zonal_stats_withForecast_comparison.csv")

# Define the total clus
total = 115700
# Iterate over the columns starting from the third one and compare its values to the last column
matches = {}  # This dictionary will store the column name and the number of matches
# Find the number of columns
num_columns = len(df.columns)
# Last column
last_column = df["cdl_forecast"]
for col in df.columns[-3:-1]:  # We exclude the last column itself from comparison
    # Count matches between the current column and the last column
    count = (df[col] == last_column).sum()
    percentage = (count / total) * 100
    matches[col] = f"{count} ({percentage:.2f}%)"

print("Overall Matches:", matches)

overall_matches_df = pd.DataFrame([matches], index=['Overall'])
print(overall_matches_df)

unique_values = {}
selected_columns = df.columns[-3:-1]
def calculate_percentage(counts, total):
    return {key: f"{value} ({(value / total) * 100:.2f}%)" for key, value in counts.items()}
# For entire DataFrame
unique_values = {}
for col in selected_columns:
    counts = df[col].value_counts(ascending=False).to_dict()
    unique_values[col] = calculate_percentage(counts, len(df))
print("Overall unique values:", unique_values)
# Convert the unique values dictionary to a DataFrame
overall_unique_df = pd.DataFrame.from_dict(unique_values)
print("Overall unique values:", overall_unique_df)

# Function to compare columns
def compare_columns(group):
    last_column = group[group.columns[-1]]
    matches = {}
    state_total = len(group)  # Count of rows for this state
    for col in group.columns[-3:-1]:  # Exclude the last column itself from comparison
        # Count matches between the current column and the last column
        count = (group[col] == last_column).sum()
        percentage = (count / state_total) * 100
        matches[col] = f"{count} ({percentage:.2f}%)"

    return pd.Series(matches, name='StateAbbre')
    return pd.pd.Series(matches, name='cdl_forecast')

# Matches for each state
result = df.groupby('StateAbbre').apply(compare_columns)
result2 = df.groupby('cdl_forecast').apply(compare_columns)
print("\nMatches per state:")
print(result)
print(result2)

# Group by 'StateAbbre' and get size of each group
group_sizes = df.groupby('StateAbbre').size()
print('group_sizes', group_sizes)
# For each state
def get_unique_values_per_state(group):
    return {col: calculate_percentage(group[col].value_counts(ascending=False).to_dict(), len(group)) for col in selected_columns}
statewise_unique_values = df.groupby('StateAbbre').apply(get_unique_values_per_state)
print("\nState-wise unique values:")
print(statewise_unique_values)

# Function to count matches and compute percentage for both crop1 and crop2 against reference_crop
def count_and_percentage(group):
    match_count_crop1 = (group['Y9reg_majority'] == group['cdl_forecast']).sum()
    match_count_crop2 = (group['Y9area_majority'] == group['cdl_forecast']).sum()
    total_count = len(group)
    return pd.Series({'Y9reg_majority_match': match_count_crop1,
                      'Percentage': match_count_crop1 / total_count * 100,
                      'Y9area_majority_match': match_count_crop2,
                      'Percentage2': match_count_crop2 / total_count * 100})

# Group by 'state' and aggregate using the custom function
crop_state_match = df.groupby(['StateAbbre', 'cdl_forecast']).apply(count_and_percentage).reset_index()
crop_state_match = crop_state_match.replace('cdl_forecast','crop')
print(crop_state_match)


# Convert state-wise matches to a DataFrame
state_matches_df = result.reset_index()
state_matches_df2 = result2.reset_index()

# Flatten the dictionary
flattened_data = []
for key, subdict in statewise_unique_values.items():
    temp = {'Category': key}
    temp.update(subdict)
    flattened_data.append(temp)

statewise_unique_values_df = pd.DataFrame(flattened_data)
# Flatten the dictionary
semi_df = pd.concat([overall_matches_df,overall_unique_df, result2, result], ignore_index=False)
print(semi_df)

final_df = pd.concat([semi_df,crop_state_match])

print(final_df)
# Save to CSV
#final_df.to_csv(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CI_by_area_comparison\Results.csv")