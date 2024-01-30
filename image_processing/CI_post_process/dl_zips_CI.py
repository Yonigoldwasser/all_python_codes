import sys

import boto3
import os
import subprocess

# This code download all zip folder with clus clipping rasters from AWS bucket and puts them in a folder in instance named
# by the CI run - example - Y8
s3 = boto3.client('s3')
target_file = sys.argv[1]
#bucket = sys.argv[2]
bucket = 'pw-crop-classification-rs'
print(bucket)
prefixes = s3.list_objects_v2(Bucket=bucket,Prefix=f'2023/general/{target_file}/', Delimiter='/')['CommonPrefixes']
for pref in prefixes:
  # name of sub folders in Y1_10m_cropid
  prefix = pref['Prefix']
  print(prefix)
  # name of footprint - like: cropid_2023_11
  fp_id = prefix.split('/')[-2]
  keys = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']
  for key in keys:
    # This line extracts the object's key (file path) and assigns it to the variable k.
    k = key['Key']
    # dirname is the Y6 for example - the first Y and number of the Y something_10m_cropid folder in general. this is the folder name that will be in the instance
    dirname=k.split('/')[2].split('_')[0]
    print(dirname)
    if not k.endswith('clus.zip') and not k.endswith('.tif'):
      print('not valid')
      continue
    subprocess.run(f'aws s3 cp s3://{bucket}/{k} {dirname}/',shell=True).check_returncode()
    if k.endswith('clus.zip'):
      subprocess.run(f'unzip -q -o -d {dirname} {dirname}/clus.zip',shell=True).check_returncode()