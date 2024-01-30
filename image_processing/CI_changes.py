import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
import seaborn as sns
import os

df_folder_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CIs_dataframes"
#files = [file for file in os.listdir(df_folder_path) if file.endswith('.csv')]
files = [file for file in os.listdir(df_folder_path) if file.endswith('.csv') and 'forecast' not in file.lower()]
print(files)

if 'ProAg' in df_folder_path:
    total_clus = 117500
else:
    total_clus = 2114
# Initialize an empty DataFrame to track changes
changes_df = pd.DataFrame(columns=['Name', 'Change'])
# Read the last file as the base file
base_file = pd.read_csv(f'{df_folder_path}\{files[-1]}')
print(base_file)
# filter out the forcast clus
# base_file = base_file.loc[base_file['ml_model_code'] != 'fa']
# Count the number of rows in the DataFrame
num_clus = len(base_file)
print("Number of clus:", num_clus)
Percent_out_of_total = (num_clus/total_clus)*100
print("Percent_out_of_total:", Percent_out_of_total)
num_latest = len(base_file[base_file['latest'] == True])
print("num_latest:", num_latest)
Y1_approved = len(base_file[base_file['ml_model_code'] == 'Y1a'])
print("Y1_approved:", Y1_approved)
Y2_approved = len(base_file[base_file['ml_model_code'] == 'Y2a'])
Y3_approved = len(base_file[base_file['ml_model_code'] == 'Y3a'])
Y4_approved = len(base_file[base_file['ml_model_code'] == 'Y4a'])
Y5_approved = len(base_file[base_file['ml_model_code'] == 'Y5a'])
Y6_approved = len(base_file[base_file['ml_model_code'] == 'Y6a'])
Y7_approved = len(base_file[base_file['ml_model_code'] == 'Y7a'])
Y8_approved = len(base_file[base_file['ml_model_code'] == 'Y8a'])
Y9_approved = len(base_file[base_file['ml_model_code'] == 'Y9a'])
B8_approved = len(base_file[base_file['ml_model_code'] == 'B8'])
fa_apprved = len(base_file[base_file['ml_model_code'] == 'fa'])

Num_tile_latest_approved = base_file[base_file['latest'] == True]['tile'].nunique()
print('num of tiles approved :',Num_tile_latest_approved)
Num_tile_from_all_CIs = base_file['tile'].nunique()
print('num of tiles approved all CIs :',Num_tile_from_all_CIs)


df_data = pd.DataFrame({'Variable': ['Number of clus pushed', 'Percent from total clus', 'Latest CI clus updated', 'From Y1a CI',
                                     'From Y2a CI', 'From Y3a CI', 'From Y4a CI', 'From Y5a CI', 'From Y6a CI', 'From Y7a CI',
                                     'From Y8a CI', 'From Y9a CI', 'From B8 CI', 'From fa CI', 'Number of tiles approved latest CI','Number of overall tiles approved from all CI'],
                   'Value': [num_clus, Percent_out_of_total, num_latest, Y1_approved, Y2_approved, Y3_approved, Y4_approved,
                             Y5_approved, Y6_approved, Y7_approved, Y8_approved, Y9_approved, B8_approved, fa_apprved, Num_tile_latest_approved, Num_tile_from_all_CIs  ]})

print(df_data)

# Initialize an empty DataFrame to track changes
changes_df = pd.DataFrame(columns=['clu_id', 'Change'])
# Read the last file as the base file
#base_file = pd.read_csv(f'{df_folder_path}\{files[-1]}')
target_values = ['41', '81', '21', '11', '101', '102']  # Add more values if needed
# Initialize a count dictionary
count_dict = {value: 0 for value in target_values}

# Iterate through the previous files in reverse order
for i in range(len(files) - 2, -1, -1):
    current_file = pd.read_csv(f'{df_folder_path}\{files[i]}')
    changes_added = False  # Flag to track if changes have been added

    for index, row in base_file.iterrows():
        crop = eval(row['crop_identification'])
        crop_value = crop[0]['crop_code']
        name_value = row['clu_id']
        base_ml_model = row['ml_model_code']
        tile = row['tile']
        if crop_value in target_values:
            count_dict[crop_value] += 1

        # Compare crop value with the corresponding row in the current file
        current_crop = current_file.loc[current_file['clu_id'] == name_value]#, 'crop_identification']#.values
        current_crop_row = current_file.loc[current_file['clu_id'] == name_value, 'crop_identification'].values
        for index, row in current_crop.iterrows():
            current_ml_model = row['ml_model_code']
            current_crop = eval(row['crop_identification'])
            current_crop = current_crop[0]['crop_code']


        if len(current_crop_row) == 1 and current_crop != crop_value:
            changes_df = changes_df.append({'clu id': name_value, 'Tile': tile, 'Change': f'from {current_crop} to {crop_value}', 'ml model': f'from {current_ml_model} to {base_ml_model}'}, ignore_index=True)
            changes_added = True
        elif len(current_crop_row) != 1:
            # If no matching row in current file, check previous files
            for j in range(i - 1, -1, -1):
                prev_file = pd.read_csv(f'{df_folder_path}\{files[j]}')
                prev_crop = prev_file.loc[prev_file['clu_id'] == name_value]
                prev_crop_row = prev_file.loc[prev_file['clu_id'] == name_value, 'crop_identification'].values


                for index, row in prev_crop.iterrows():
                    prev_ml_model = row['ml_model_code']
                    prev_crop = eval(row['crop_identification'])
                    prev_crop = prev_crop[0]['crop_code']


                if len(prev_crop_row) == 1 and prev_crop != crop_value:
                    changes_df = changes_df.append({'clu id': name_value, 'Tile': tile, 'Change': f'from {prev_crop} to {crop_value}', 'ml model': f'from {prev_ml_model} to {base_ml_model}'},ignore_index=True)
                    changes_added = True
                    break

        if changes_added:
            continue

    if changes_added:

        break
# Display the changes DataFrame
replace_dict = {'41': 'Corn', '21': 'Cotton', '11': 'Wheat', '81': 'Soybean', '101': 'Other', '102': 'Non Ag'}
Number_of_Changed_clus = pd.DataFrame(columns=['Number_of_Changed_clus'])
Number_of_Changed = len(changes_df['clu id'])
Number_of_Changed_clus.loc[0,'Number_of_Changed_clus'] = Number_of_Changed
changes_value_counts = changes_df['Change'].value_counts()

# Create new columns for value and count
stat_df = pd.DataFrame()
stat_df['Change value'] = changes_value_counts.index
stat_df['Count'] = changes_value_counts.values


for key in count_dict:
    value = count_dict[key]
    percent_from_total_clus = (value/total_clus)*100
    percent_from_approved_clus = (value/num_clus)*100
    count_dict[key] = (value, percent_from_approved_clus,percent_from_total_clus)

# Create a list of dictionaries with key-value pairs
count_dict_data = [{'Crop': key, 'CI Clu count': values[0], 'Percent from approved': values[1], 'Percent from total': values[2]} for key, values in count_dict.items()]
count_df = pd.DataFrame(count_dict_data)
count_df = count_df.replace(replace_dict)

# Create an Excel writer object
writer = pd.ExcelWriter(r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C9\CI9_Changes_report.xlsx")
# Calculate the number of columns for the spacing
num_columns = 2
# Create a spacer DataFrame
spacer = pd.DataFrame(columns=[''] * num_columns)
# Concatenate the DataFrames
combined_df = pd.concat([df_data, spacer, count_df, spacer, changes_df, Number_of_Changed_clus, stat_df], axis=1)

# Write the combined DataFrame to the Excel file
combined_df.to_excel(writer, sheet_name='Sheet1', index=False)

writer.save()

############### confidence histogram ########################################
conf_list = []
for x in base_file['confidence']:
    if x<= 0.39:
        x= 'Low'
    elif 0.39 <x<= 0.69:
        x = "Medium"
    elif x> 0.69:
        x = 'High'
    conf_list.append(x)


# Create a histogram
bins = ["Low", "Medium", "High"]
# Count the frequency of each bin in the values
value_counts = {bin: conf_list.count(bin) for bin in bins}

# Create a list of frequencies corresponding to the bins
frequencies = [value_counts.get(bin, 0) for bin in bins]
# Set custom colors for the bars
colors = ["red", "orange", "green"]
# Create a histogram using seaborn
sns.barplot(x=bins, y=frequencies, palette=colors)

# Set the title and labels
plt.title('Histogram')
plt.xlabel('Confidence')
plt.ylabel('Clu amount')
# Add the value of frequency on top of each bar
for i, freq in enumerate(frequencies):
    plt.annotate(str(freq), xy=(i, freq), ha='center', va='bottom')
# Save the plot as an image
output_file = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\C9\CI9_histogram.png"
plt.savefig(output_file)
# Display the histogram
plt.show()