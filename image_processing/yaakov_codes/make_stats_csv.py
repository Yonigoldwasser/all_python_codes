import csv
import datetime
import geopandas as gpd
import pandas as pd
import numpy
import rasterio as rs
import os
import glob
import sys
from datetime import date

import json
today = date.today().strftime('%Y-%m-%d')
MAX_CROPS = 3
CODES_DICT = {
    '41': 'Corn',
    '81': 'Soybeans',
    '21': 'Cotton',
    '11': 'Wheat',
    '997': 'Soil',
    '101': 'Other',
    '102': 'NonAg'
}
# gdf = gpd.read_file(sys.argv[1])

features_file = sys.argv[1] # updated geojason?
with open(features_file) as src:
    features = json.load(src)['features']

f_dict = {}
for f in features:
    cluid = f['properties']['CommonLand']
    f_dict[cluid] = f['properties']
inputdir = 'sorted'           # the sorted folder
files = os.listdir(inputdir)
results = []
results_dict = {}
for f in files:
    if not f.endswith('tif'):
        continue
    cluid = f[:-4]
    clu_acres = float(f_dict[cluid]['CluCalcula'])
    ds = rs.open(os.path.join(inputdir, f))
    f_arr = ds.read()
    meta = ds.profile
    total_pix_count = numpy.sum(f_arr != meta.data['nodata'])
    detected_pixels = 0
    l = [21, 81, 11, 997, 41, 998]  # why this order - need to change to 101, 102
    os.makedirs(os.path.join(inputdir, f'stats/{cluid}'), exist_ok=True)
    for i in l:
        r = numpy.where(f_arr == i, i, 0)
        if numpy.sum(r == i) > 0:
            detected_pixels += numpy.sum(r == i)
            with rs.open(os.path.join(inputdir, f'stats/{cluid}/{i}ras.tif'), 'w', **meta) as dst:
                dst.write(r.astype(rs.uint8)[0, :, :], 1)

    # create list of classes mask tifs
    tifs = []
    for i in glob.glob(os.path.join(inputdir, f'stats/{cluid}/*.tif')):
        tifs.append(i)
    tifs.sort()
    print(tifs, 'created')

    print('start calculating stats')
    if len(tifs) == 0:
        results.append({
            'cluid': cluid,
            'crop code': '998',
            'crop name': CODES_DICT['998'],
            'acres': str(clu_acres)
        })
        if cluid not in results_dict:
            results_dict[cluid] = []
        results_dict[cluid].append({'crop code': '998',
            'crop name': CODES_DICT['998'],
            'acres': str(clu_acres)})
    for a in tifs:
        with rs.open(a) as stat_ds:
            stat_arr = stat_ds.read()
        stat_code = os.path.basename(a).split('.')[0][:-3]
        pix_count = numpy.sum(stat_arr == int(stat_code))
        area_proportion = pix_count/total_pix_count
        code_acres = clu_acres*area_proportion
        results.append({
            'cluid': cluid,
            'crop code': stat_code,
            'crop name': CODES_DICT[stat_code],
            'acres': str(code_acres)
        })
        if cluid not in results_dict:
            results_dict[cluid] = []
        results_dict[cluid].append({'crop code': stat_code,
            'crop name': CODES_DICT[stat_code],
            'acres': str(code_acres)})

    # if detected_pixels < total_pix_count:
    #     others_acres = str(clu_acres*(total_pix_count-detected_pixels)/total_pix_count)
    #     results.append({
    #         'cluid': cluid,
    #         'crop code': 998,
    #         'crop name': CODES_DICT['998'],
    #         'acres': others_acres
    #     })
    #     if cluid not in results_dict:
    #         results_dict[cluid] = []
    #     results_dict[cluid].append({'crop code': '998',
    #         'crop name': CODES_DICT['998'],
    #         'acres': others_acres})
current_time = datetime.datetime.now().date().isoformat().replace('-','')
with open(f'crops_acres_{current_time}.csv','w') as out:
    csv_reader = csv.writer(out)
    csv_reader.writerow(('cluid', 'crop code', 'crop name', 'acres'))
    for r in results:
        csv_reader.writerow((r['cluid'],r['crop code'], r['crop name'],r['acres']))

with open(f'crops_acres_consolidated_{current_time}.csv','w') as out:
    csv_reader = csv.writer(out)
    header = ('cluid', 'crop code 1', 'crop name 1','acres 1', 'crop code 2', 'crop name 2','acres 2', 'crop code 3', 'crop name 3','acres 3')
    csv_reader.writerow(header)
    for cluid in results_dict:
        row = [cluid,]
        for i,crop in enumerate(results_dict[cluid]):
            row.extend((crop['crop code'], crop['crop name'], crop['acres']))
        missing = len(header) - len(row)
        row.extend(['' for x in range(missing)])
        csv_reader.writerow(row)