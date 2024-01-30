
import requests
import pandas as pd

url = "https://quickstats.nass.usda.gov/api/api_GET/"

params = {
    "key": "B5D9AE75-3641-335E-BE75-7796474E5596",
    "source_desc": "SURVEY",
    "sector_desc": "CROPS",
    "group_desc": "FIELD CROPS",
    "commodity_desc": ["CORN", "WHEAT", "COTTON", "SOYBEANS", "HAY", "SORGHUM", "SUNFLOWER", "OATS", "BARLEY", "CANOLA", "RICE", "POTATOES"],
    "statisticcat_desc": ["AREA PLANTED", "YIELD", "PRODUCTION"],
    #"short_desc": [:],
    "domain_desc": "TOTAL",
    "agg_level_desc": "STATE",
    "state_name": "KANSAS",
    "year": ["2018","2019", "2020", "2021", "2022"],
    "freq_desc": "ANNUAL",
    "reference_period_desc": "YEAR",
}
response = requests.get(url, params=params)
data = response.json()["data"]
df = pd.DataFrame(data)
print(df.columns)
# List of columns to keep
columns_to_keep = ['util_practice_desc', 'freq_desc', 'location_desc', 'agg_level_desc', 'state_name', 'short_desc',
                'statisticcat_desc', 'Value', 'year', 'unit_desc']

# Extracting only the desired columns
df_filtered = df[columns_to_keep]

print(df_filtered)

# Create an Excel writer object
writer = pd.ExcelWriter(r"C:\Users\User\Documents\USDA_report.xlsx")
# Write the combined DataFrame to the Excel file
df_filtered.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
print(df_filtered)