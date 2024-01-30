import os
import json
import sys

import boto3
from pwatchers.api.api_client import PipelineApiClient, PipelineQueryBuilder
from pwatchers.api.filters import StackFilter

#################################
# update necessary fields
################################
geojson_file_path = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\ProAg_2023_CI_footprints.geojson"

# with open(sys.argv[1]) as src:
with open(geojson_file_path) as src:
    features = json.load(src)['features']
# hudson_fps.extend(proag_fps)
season = '2023'
s3 = boto3.client('s3')
client = 'proag'
# s3_raster_prefix = f'data/cropid/{season}/proag/'
batch = boto3.client('batch', region_name='eu-central-1')
s3_geojson_path = 'proag-data/crop-classification/rs_input/CI3_clus_geojson.geojson'
s3_geojson_cluid_field = 'CommonLand'
client_bucket = 'hudson-client-data' if client == 'hudson' else 'proag-data'
# geom = clu_convex_hull_handler({'client': client, 'fp_id': 'unknown'}, {})['coordinates'][0]
# rasters = s3.list_objects_v2(Bucket='pw-pipeline-resources', Prefix=s3_raster_prefix)['Contents']
rasters = s3.list_objects_v2(Bucket='proag-data', Prefix='crop-classification/rs_input')['Contents']
#rasters?

for feature in features:
    stack_id = f"cropid_2023_{feature['properties']['ID']}"
    print(feature)
    for raster in rasters:
        # 10m_merge rasters of each classification
        if not raster['Key'].endswith('_cropid.tif') or 'Y3' not in raster['Key']:
            continue
        print(raster)

        parameters = {
            's3_s1_img_path': 'proag-data/' + raster['Key'],
            # 'hudson-client-data/clus/Hudson2022/unknown_clus_hudson.geojson', #
            's3_clus_geojson_path': s3_geojson_path,
            'clu_field': s3_geojson_cluid_field,
            's3_out_dir': f'{client_bucket}/crop-classification/general/2023/{raster["Key"].split("/")[-1][:-4]}/{stack_id}/',
            'stack_id': stack_id,
            'stack_geometry': str(feature['geometry']['coordinates'][0][0]).replace(' ', ''),
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