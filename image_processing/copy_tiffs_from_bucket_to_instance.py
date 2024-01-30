import boto3
import os
import pandas as pd
import sys
# Initialize the S3 client
s3 = boto3.client('s3')
file = pd.read_csv(sys.argv[1])
# Filter the DataFrame based on the state value (e.g., 'New York')
filtered_df = file[file['state'] == 'IL']
filtered_df = filtered_df[filtered_df['s3_link'].notna()]
# Extract the values from the 'link' column and convert to a list
file_paths_in_bucket = filtered_df['s3_link'].tolist()
# Bucket name and list of file paths in the bucket
bucket_name = 'proag-data'

# Destination folder on the EC2 instance
destination_folder = sys.argv[2]

# Ensure the destination directory exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Iterate over file paths and download them
for s3_path in file_paths_in_bucket:
    # Destination path on the EC2 instance
    local_path = os.path.join(destination_folder, os.path.basename(os.path.dirname(os.path.dirname(s3_path))))
    print(local_path)
    # Download file from S3 to the EC2 instance
    s3.download_file(bucket_name, s3_path, local_path)

print("Files downloaded successfully!")