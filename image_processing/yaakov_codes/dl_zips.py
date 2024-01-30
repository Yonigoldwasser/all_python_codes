import sys

import boto3
import os
import subprocess

s3=boto3.client('s3')
target_file = sys.argv[1]
bucket = sys.argv[2]
prefixes = s3.list_objects_v2(Bucket=bucket,Prefix=f'crop-classification/general/2023/{target_file}/', Delimiter='/')['CommonPrefixes']
for pref in prefixes:
  prefix=pref['Prefix']
  print(prefix)
  fp_id = prefix.split('/')[-2]
  keys = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']
  for key in keys:
    k = key['Key']
    dirname=k.split('/')[3].split('_')[0]
    print(dirname)
    if not k.endswith('clus.zip') and not k.endswith('.tif'):
      print('not valid')
      continue
    subprocess.run(f'aws s3 cp s3://{bucket}/{k} {dirname}/',shell=True).check_returncode()
    if k.endswith('clus.zip'):
      subprocess.run(f'unzip -q -o -d {dirname} {dirname}/clus.zip',shell=True).check_returncode()