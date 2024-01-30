
import requests
import pandas as pd

url = "https://quickstats.nass.usda.gov/api/api_GET/"

params = {
    "key": "",
    "source_desc": "SURVEY",
    "sector_desc": "CROPS",
    "group_desc": "FIELD CROPS",
    "commodity_desc": "CORN",
    "statisticcat_desc": "PROGRESS",
    "short_desc": "CORN - PROGRESS, MEASURED IN PCT PLANTED",#, COTTON, UPLAND - PROGRESS, MEASURED IN PCT PLANTED, SOYBEANS - PROGRESS, MEASURED IN PCT PLANTED, WHEAT, SPRING, DURUM - PROGRESS, MEASURED IN PCT PLANTED, WHEAT, SPRING, (EXCL DURUM) - PROGRESS, MEASURED IN PCT PLANTED
    "agg_level_desc": "STATE",
    "year__or": "2023"
}


response = requests.get(url, params=params)

data = response.json()["data"]

df = pd.DataFrame(data)

print(df)

