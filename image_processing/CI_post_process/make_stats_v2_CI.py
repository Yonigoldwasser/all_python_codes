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
client_bucket = sys.argv[2]

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
    ml_model_code = ml_model_code.replace('c', '')
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
        ################################################
        # 15*15 meter pixel is 225 m2
        #acres_by_area = (pix_count * 225)/ 4046.86
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
        # if early classification keep conf medium
        if today > str(datetime.date(2023, 7, 1)):
            if ml_model_code == 'f' or (ml_model_code[1].isdigit() and int(ml_model_code[1]) >= 5):
        #if (today > str(datetime.date(2023, 7, 1))) and ((int(ml_model_code[-1]) >= 5) or (ml_model_code == 'f')):
                classification = 0.3
            else:
                classification = 0.1
        if stat_code2 == 0:
            # if the crop is nonag in every senario put conf as 0.1 - low
            conf_value = 0.1
        else:
            if ml_model_code == 'f':
                conf_value = 0

            else:
                conf_value = location + classification + stat_code2
        ################################################################
        results.append({
            'clu_id': clu_id,
            'crop code': stat_code,
            'crop name': CODES_DICT[stat_code],
            'acres': str(code_acres),
            'confidence': conf_value
            #'acres2': str(acres_by_area)
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
            #'acres2': str(acres_by_area)
        })


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
    # if crop['latest'][-1] == ml_model[-1]:
    # use this line if we use a models for CI
    if ml_model != 'f' and ml_model != 'fa':
        if crop['latest'][-1] == ml_model[1]:
            latests.append(True)
        else:
            latests.append(False)
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


# Initialize an empty list to store the dictionaries
dict_list = []
# determine customer name by client bucket
if 'fmh' in client_bucket:
    customer_name = 'fmh'
elif 'proag' in client_bucket:
    customer_name = 'proag'
elif 'hudson' in client_bucket:
    customer_name = 'hudson'
elif 'rcis' in client_bucket:
    customer_name = 'rcis'
else:
    customer_name = 'nau'


# Iterate over the rows of the DataFrame
for _, row in df.iterrows():
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
        'customer_name': customer_name

    }
    dict_list.append(my_dict2)
# check match no match of non ag clus to forecast. if match stay with CI, if no match label clu as 'fa' - updates the geojson CI column
print("match/no match started")

# Load CSV data
CS_forecast = sys.argv[3]
csv_data = {}  # Crop name to crop ID mapping
with open(CS_forecast, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_crop_code = row['crop_code']
        csv_clu_name = row['CommonLand']
        if csv_crop_code:
            csv_data[csv_clu_name] = int(csv_crop_code.rstrip('.0'))
        else:
            csv_data[csv_clu_name] = int(200)
# Load GeoJSON data
with open(features_file, 'r') as geojson_file:
    geojson_data = json.load(geojson_file)
# Sort the features by the "name" property
sorted_features = sorted(geojson_data['features'], key=lambda x: x['properties']['CommonLand'])

# Update the GeoJSON data with sorted features
geojson_data['features'] = sorted_features
# Process GeoJSON data from the original geojson (from the top)

for feature in geojson_data['features']:
    properties = feature['properties']
    clu_name = properties['CommonLand']
    # print('first',clu_name)

    for entry in dict_list:
        # print(entry)
        g = entry['clu_id']
        if clu_name == g:
            # print(entry)
            entry_name = g
            crop_code = int(entry['crop_identification'][0]['crop_code'])
            if crop_code == 102:
                if clu_name in csv_data:
                    csv_crop_code1 = csv_data[clu_name]
                    if crop_code != csv_crop_code1:
                        clu_name1 = clu_name
                        last_CI_key = list(properties.keys())[-1]
                        properties[last_CI_key] = 'f'


# Find the position of the substring '_geojson' in the file path
index = features_file.find('_geojson')
if index != -1:
    # Insert '_updated' before the substring '_geojson'
    new_file_path = features_file[:index] + '_updated' + features_file[index:]

# print(features2)
with open(new_file_path, 'w') as updated_geojson_file:
    json.dump(geojson_data, updated_geojson_file)