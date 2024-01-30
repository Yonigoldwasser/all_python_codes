import boto3
import os
import datetime
import subprocess
import glob
import sys
from concurrent import futures

def get_all_s3_objects(bucket, prefix, s3_client):
  init_response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
  objs = init_response['Contents']
  has_more = init_response['IsTruncated']
  while has_more:
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, StartAfter=objs[-1]['Key'])
    objs.extend(response['Contents'])
    has_more = response['IsTruncated']
  return objs

def upload_file(filepath, bucket, prefix):
  s3.upload_file(filepath, bucket, prefix)

client_bucket = sys.argv[1]
s3=boto3.client('s3')
date=f'{datetime.datetime.now().date().isoformat().replace("-","")}.tif'
#all_rasters = get_all_s3_objects(client_bucket, 'crop-classification/rasters/', s3)
#uploaded = set([x['Key'].split('/')[-3] for x in all_rasters])
local_dir = 'sorted'
local_files = os.listdir(local_dir)
local_set = set(local_files)
threads = []
with futures.ThreadPoolExecutor(max_workers=6) as exec:
  for f in local_files:
    if f.endswith('.tif'):
      cluid=f[:-4]
      threads.append(exec.submit(upload_file,os.path.join(local_dir,f),client_bucket,f'crop-classification/rasters/2024/{cluid}/daily/{date}'))
      print(cluid)
for t in futures.as_completed(threads):
  if t.exception():
    raise t.exception()