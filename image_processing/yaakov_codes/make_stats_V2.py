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

print('start')

today = date.today().isoformat()
current_time = datetime.datetime.now().date().isoformat().replace('-', '')
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

features_file = sys.argv[1]
gdf = gpd.read_file(sys.argv[1])
with open(features_file) as src:
    features = json.load(src)['features']

f_dict = {}
for f in features:
    clu_id = f['properties']['CommonLand']
    f_dict[clu_id] = f['properties']
    latest = list(f_dict[clu_id].keys())[-1]
inputdir = r"sorted"  # the sorted folder
files = os.listdir(inputdir)
results = []
results_dict = {}
for f in files:
    print(f, 'f')
    if not f.endswith('tif'):
        continue
    clu_id = f[:-4]
    # calc_id = f[:-19]
    print(clu_id, 'clu_id')
    clu_acres = float(f_dict[clu_id]['CluCalcula'])
    tile_name = f_dict[clu_id]['tile']
    location = f_dict[clu_id]['location']
    ml_model_code = f_dict[clu_id][latest]
    latest1 = list(f_dict[clu_id].keys())[-1]
    ds = rs.open(os.path.join(inputdir, f))
    f_arr = ds.read()
    meta = ds.profile
    total_pix_count = numpy.sum(f_arr != meta.data['nodata'])
    detected_pixels = 0
    l = [21, 81, 11, 997, 41, 101, 102]  # why this order - need to change to 101, 102
    os.makedirs(os.path.join(inputdir, f'stats/{clu_id}'), exist_ok=True)
    for i in l:
        r = numpy.where(f_arr == i, i, 0)
        if numpy.sum(r == i) > 0:
            detected_pixels += numpy.sum(r == i)
            with rs.open(os.path.join(inputdir, f'stats/{clu_id}/{i}ras.tif'), 'w', **meta) as dst:
                dst.write(r.astype(rs.uint8)[0, :, :], 1)

    # create list of classes mask tifs
    tifs = []
    for i in glob.glob(os.path.join(inputdir, f'stats/{clu_id}/*.tif')):
        tifs.append(i)
    tifs.sort()
    print('start calculating stats')
    if len(tifs) == 0:
        results.append({
            'clu_id': clu_id,
            'crop code': '101',
            'crop name': CODES_DICT['101'],
            'acres': str(clu_acres),
            'confidence': 0.6
        })
        if clu_id not in results_dict:
            results_dict[clu_id] = []
        results_dict[clu_id].append({'crop code': '101',
                                     'crop name': CODES_DICT['101'],
                                     'acres': str(clu_acres),
                                     'confidence': 0.6,
                                     'tile name': tile_name,
                                     'ml_model': ml_model_code,
                                     'latest': latest1,
                                     's3_link': f'crop-classification/rasters/2023/{clu_id}/daily/{current_time}.tif'})
    for a in tifs:
        with rs.open(a) as stat_ds:
            stat_arr = stat_ds.read()
        stat_code = os.path.basename(a).split('.')[0][:-3]
        pix_count = numpy.sum(stat_arr == int(stat_code))
        area_proportion = pix_count / total_pix_count
        code_acres = clu_acres * area_proportion
        ################################################################
        # conf value based on crop, location and time of classification
        stat_code2 = stat_code
        if location == 'CornBelt':
            location = 0.3
        else:
            location = 0.1
        if stat_code2 == '41':
            stat_code2 = 0.25
        elif stat_code2 == '81':
            stat_code2 = 0.1
        elif stat_code2 == '102':
            stat_code2 = 0
        else:
            stat_code2 = 0.05
        if today < str(datetime.date(2023, 7, 1)):
            classification = 0.1
        else:
            classification = 0.3
        if stat_code2 == 0:
            # if the crop is nonag in every senario put conf as 0.1 - low
            conf_value = 0.1
        else:
            conf_value = location + classification + stat_code2
        ################################################################
        results.append({
            'clu_id': clu_id,
            'crop code': stat_code,
            'crop name': CODES_DICT[stat_code],
            'acres': str(code_acres),
            'confidence': conf_value
        })
        # print(results, 'results')
        if clu_id not in results_dict:
            results_dict[clu_id] = []
        results_dict[clu_id].append({
            'crop code': stat_code,
            'crop name': CODES_DICT[stat_code],
            'acres': str(code_acres),
            'confidence': conf_value,
            'tile name': tile_name,
            'ml_model': ml_model_code,
            'latest': latest1,
            's3_link': f'crop-classification/rasters/2023/{clu_id}/daily/{current_time}.tif'
        })

current_time = datetime.datetime.now().date().isoformat().replace('-', '')
with open(f'crops_acres_{current_time}.csv', 'w') as out:
    csv_reader = csv.writer(out)
    csv_reader.writerow(('clu_id', 'crop code', 'crop name', 'acres'))
    for r in results:
        csv_reader.writerow((r['clu_id'], r['crop code'], r['crop name'], r['acres']))

with open(f'crops_acres_consolidated_{current_time}.csv', 'w') as out:
    csv_reader = csv.writer(out)
    header = (
        'clu_id', 'crop code 1', 'crop name 1', 'acres 1', 'crop code 2', 'crop name 2', 'acres 2', 'crop code 3',
        'crop name 3', 'acres 3')
    csv_reader.writerow(header)
    for clu_id in results_dict:
        row = [clu_id, ]
        for i, crop in enumerate(results_dict[clu_id]):
            row.extend((crop['crop code'], crop['crop name'], crop['acres']))
        missing = len(header) - len(row)
        row.extend(['' for x in range(missing)])
        csv_reader.writerow(row)

clu_ids = []
results = []
confidences = []
ml_model_codes = []
tiles = []
latests = []
s3_links = []
for clu_id in results_dict:
    print(clu_id, 'clu_id')
    row = [clu_id, ]
    stats2 = []
    confs = []
    for i, crop in enumerate(results_dict[clu_id]):
        stats = {'crop_code': crop['crop code'], 'identified_acres': float(crop['acres'])}
        conf_clac = {'identified_acres': crop['acres'], 'conf': crop['confidence']}
        tile_name = crop['tile name']
        ml_model = crop['ml_model']
        stats2.append(stats)
        confs.append(conf_clac)
    stats2 = sorted(stats2, key=lambda x: float(x['identified_acres']), reverse=True)
    sorted_confs = sorted(confs, key=lambda x: float(x['identified_acres']), reverse=True)
    conf = sorted_confs[0]['conf']
    if crop['latest'][-1] == ml_model[-1]:
        latests.append(True)
    else:
        latests.append(False)
    s3_link = crop['s3_link']

    clu_ids.append(clu_id)
    results.append(stats2)
    confidences.append(conf)
    ml_model_codes.append(ml_model)
    tiles.append(tile_name)
    s3_links.append(s3_link)

df = pd.DataFrame(list(zip(clu_ids, results, confidences, ml_model_codes, tiles, s3_links, latests)),
                  columns=['clu_id', 'crop_identification', 'confidence', 'ml_model_code', 'tile', 's3_link', 'latest'])
df.insert(3, 'execution_date', today)
df.to_csv(f'crops_acres_df_{current_time}.csv')
#df.to_json(f'crops_json{current_time}.JSON', orient='records')
# Initialize an empty list to store the dictionaries
dict_list = []
# Iterate over the rows of the DataFrame
for _, row in df.iterrows():
    # Extract the relevant columns into a new DataFrame
    #results_df = row[['crop_identification', 'confidence', 'execution_date', 'ml_model_code', 'tile', 's3_link']]
    #results_dict = results_df.to_dict()#(orient='list')
    #my_dict = {
    #    '_id': 'ObjectId',
    #    'usda_clu_id': row['clu_id'],
    #    'results': results_dict,
    #    'latest': row['latest']
    #   }
    my_dict2 = {
        '_id': 'ObjectId',
        'clu_id': row['clu_id'],
        'crop_identification': row['crop_identification'],
        'confidence': row['confidence'],
        'execution_date': row['execution_date'],
        'ml_model_code': row['ml_model_code'],
        'tile': row['tile'],
        's3_link': row['s3_link'],
        'latest': row['latest'],
        'customer_name': "proag"

    }
    dict_list.append(my_dict2)

# Write the `dict_list` to the JSON file
with open(f'crops_acres_json_{current_time}.json', 'w') as f:
    json.dump(dict_list, f)
# # Identify overlapping column names
# overlapping_columns = set(gdf.columns).intersection(set(df.columns))
#
# # Create a new Pandas DataFrame with non-overlapping columns
# df_non_overlapping = df[[col for col in df.columns if col not in overlapping_columns]]
#
# # Merge the GeoPandas DataFrame with the non-overlapping Pandas DataFrame
# merged_df = gdf.merge(df_non_overlapping, left_index=True, right_index=True)
#
# print(merged_df)
