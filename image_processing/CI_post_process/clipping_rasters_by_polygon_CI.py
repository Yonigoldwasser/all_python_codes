import os
import json
import sys

import boto3
from pwatchers.api.api_client import PipelineApiClient, PipelineQueryBuilder
from pwatchers.api.filters import StackFilter

#################################
# update necessary fields
################################
# The grid footprint file that includes all clients clus.
footprints_geojson_file_path = r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\ProAg_FMH_footprints1.geojson"

# with open(sys.argv[1]) as src:
with open(footprints_geojson_file_path) as src:
    features = json.load(src)['features']
# hudson_fps.extend(proag_fps)
season = '2023'
s3 = boto3.client('s3')
#client = 'proag'
# s3_raster_prefix = f'data/cropid/{season}/proag/'
batch = boto3.client('batch', region_name='eu-central-1')
s3_geojson_path = 'pw-nau-data/crop-classification/rs_input/CI2_NAU_all_clus_for_Y2N2.geojson'
s3_geojson_cluid_field = 'CommonLand'
#client_bucket = 'hudson-client-data' if client == 'hudson' else 'proag-data'
rasters = s3.list_objects_v2(Bucket='pw-crop-classification-rs', Prefix='2023/rs-input')['Contents']
##

for feature in features:
    stack_id = f"cropid_2023_{feature['properties']['ID']}"
    print(feature)
    for raster in rasters:
        # 10m_merge rasters of each classification - change 'Y1' to the latest CI.
        if not raster['Key'].endswith('_cropid.tif') or 'Y2N2_nau' not in raster['Key']:
            continue
        print(raster)
        #################for new fmh clus###############################################
        raster_key = raster["Key"].split("/")[-1][:-4]
        print(raster_key)
        # new_raster_key = raster_key.replace('_', 'NR_', 1)
        # print(new_raster_key)
        #########################################################################

        parameters = {
            's3_s1_img_path': 'pw-crop-classification-rs/' + raster['Key'],
            # 'hudson-client-data/clus/Hudson2022/unknown_clus_hudson.geojson', #
            's3_clus_geojson_path': s3_geojson_path,
            'clu_field': s3_geojson_cluid_field,
            's3_out_dir': f'pw-crop-classification-rs/2023/general/{raster["Key"].split("/")[-1][:-4]}/{stack_id}/',
            # 's3_out_dir': f'pw-crop-classification-rs/2023/general/{new_raster_key}/{stack_id}/',

            'stack_id': stack_id,
            'stack_geometry': str(feature['geometry']['coordinates'][0]).replace(' ', ''),
            # json.dumps(geom), #
            'insert_to_db': '0'
        }
        print(f'submitting job with parameters: {parameters}')
        res = batch.submit_job(
            jobName=os.path.basename(raster['Key']).split('.')[0] + 'cropid-split-clus',
            jobDefinition='raster-standlayer-split',
            jobQueue='gamma-coherence',
            parameters=parameters, containerOverrides={'resourceRequirements': [
                {
                    'value': '8',
                    'type': 'VCPU'
                }, {
                    'value': '40000',
                    'type': 'MEMORY'
                }
            ]}
        )
        print(res)