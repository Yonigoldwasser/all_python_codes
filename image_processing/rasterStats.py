import json
import os
import rasterio
import numpy as np
import pandas as pd
import rasterstats
from rasterstats import zonal_stats

with rasterio.open(r"C:\Users\User\Documents\Combined_CC_2023_vars\Poria_10m_mosaic.tif") as raster:
    raster = raster.read(1)
    raster[raster > 0] = 1
    print(raster)
    # reprojected_input_arr = np.array(raster.read(1))
    # #print(reprojected_input_arr)
    # reprojected_input_arr = np.where(reprojected_input_arr > 0, 1, 0)

features_file = r"C:\Users\User\Documents\FMH_2023_CC\FMH_clus.geojson"
with open(features_file) as src:
    features = json.load(src)['features']

df_list = []
for f in features[:10]:
    clu_id = f['properties']['CommonLand']
    geometry = str(f['geometry']['coordinates'][0][0]).replace(' ', '')
    print(geometry)
    print(clu_id)
    df=pd.DataFrame(zonal_stats(geometry, raster, stats=['sum']))
    df_list.append(df)

print(df_list)