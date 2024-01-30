import os
import rasterio
import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt
from rasterio.features import sieve
import cv2
from sklearn.neighbors import NearestNeighbors
import sys
from scipy import ndimage
import boto3
import subprocess

# This code download all zip folder with clus clipping rasters from AWS bucket and puts them in a folder in instance
# named by the CI run - example - Y8
s3 = boto3.client('s3')
target_file = sys.argv[1]
#bucket = sys.argv[2]
bucket = 'pw-crop-classification-rs'
print(bucket)
prefixes = s3.list_objects_v2(Bucket=bucket,Prefix=f'2024/general/{target_file}/', Delimiter='/')['CommonPrefixes']
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
    # dirname is the Y6 for example - the first Y and number of the Y something_10m_cropid folder in general. this is
    # the folder name that will be in the instance
    dirname=k.split('/')[2].split('_')[0] #[:-1]
    print(dirname)
    if not k.endswith('clus.zip') and not k.endswith('.tif'):
      print('not valid')
      continue
    subprocess.run(f'aws s3 cp s3://{bucket}/{k} {dirname}/',shell=True).check_returncode()
    if k.endswith('clus.zip'):
      subprocess.run(f'unzip -q -o -d {dirname} {dirname}/clus.zip',shell=True).check_returncode()

################################################################################################################
#########shrink_expand_majority_filter_functions(NAU acres test - not in use in benny)##########################
# # Define the majority filter function
# def majority_filter(input_array, size=5):
#   # Create a structure element for filtering, using a square connectivity of the given size
#   struct_element = np.ones((size, size))
#
#   # Use the generic_filter function from scipy.ndimage to apply the majority filter
#   def mode_filter(values):
#       # Exclude pixels with a value of 102 (or any other value you want to ignore)
#       values = values[values != 102]
#       if len(values) == 0:
#           return 0  # Return 0 if all values are ignored
#       unique_values, counts = np.unique(values, return_counts=True)
#       return unique_values[np.argmax(counts)]
#
#   # Apply the majority filter
#   filtered_array = ndimage.generic_filter(input_array, function=mode_filter, size=size, mode='constant', cval=0,
#                                           footprint=struct_element)
#   return filtered_array
#
# # Define the majority filter function
# def majority_filter2(image, size=5):
#     # The majority filter function
#     def majority_filter_func(values):
#         # Filter out the ignored value (241) from the calculation
#         values = values[values != 241]
#         if len(values) == 0:
#             return 241  # Return the ignored value if all values are to be ignored
#         return np.bincount(values.astype(int)).argmax()
#
#     return ndimage.generic_filter(image, majority_filter_func, size=size)
#
# def preserve_original_values(original, modified, ignored_value=241):
#     # Preserve original values where the pixel value is 241
#     mask = original == ignored_value
#     modified[mask] = original[mask]
#     return modified
# def preserve_original_values102(original, modified, ignored_value=102):
#     # Preserve original values where the pixel value is 102
#     mask = original == ignored_value
#     modified[mask] = original[mask]
#     return modified
# def saga_shrink_and_expand(image_array, kernel_size=9):
#     original_image = np.copy(image_array)  # Preserve the original image
#
#     # Create a kernel for morphology operations
#     kernel = np.ones((kernel_size, kernel_size), np.uint8)
#
#     # Shrink (Erode)
#     shrunk_image = cv2.erode(image_array, kernel, iterations=1)
#     shrunk_image = preserve_original_values(original_image, shrunk_image)
#     plt.imshow(shrunk_image, cmap='gray')
#     plt.title('shrunk_image')
#     plt.show()
#
#     # Apply the majority filter
#     majority_filtered_image = majority_filter2(shrunk_image, size=9)
#     majority_filtered_image = preserve_original_values(original_image, majority_filtered_image)
#     plt.imshow(majority_filtered_image, cmap='gray')
#     plt.title('majority_filtered_image')
#     plt.show()
#
#     # Another round of shrink (Erode)
#
#     final_image = cv2.erode(majority_filtered_image, kernel, iterations=1)
#     final_image = preserve_original_values(original_image, final_image)
#     final_image = preserve_original_values102(original_image, final_image)
#
#     plt.imshow(final_image, cmap='gray')
#     plt.title('final_image')
#     plt.show()
#
#     return final_image
################################################################################################################


def clean_nonag_on_boarder(raster, crops_codes, no_data_val):

    rows, cols = raster.shape

    # find non-agg pixels
    nonag_rs, nonag_cs = np.nonzero(raster == crops_codes['NONAG'])

    # iterate over non-agg pixels
    for nonag_r, nonag_c in zip(nonag_rs, nonag_cs):

        # non-agg neighbors
        nonag_neis = raster[max(0,nonag_r-1):min(nonag_r+2,rows),max(0,nonag_c-1):min(nonag_c+2,cols)]

        # check if neighbors are on boarder
        if (nonag_neis == no_data_val).any():

            # change non-agg neighbors to dominant crop
            nonag_neis = nonag_neis[~np.isin(nonag_neis,[crops_codes['NONAG'], no_data_val])].ravel()
            if len(nonag_neis):
                vals, counts = np.unique(nonag_neis,return_counts=True)
                raster[nonag_r,nonag_c] = vals[np.argmax(counts)]

    return raster


def main_raster_cleaning(raster, crops_codes, thres, no_data_val):

    # copy cleaned raster
    clean_raster = np.copy(raster)

    # filter non-agg pixels
    valid_raster_filter = ~np.isin(raster,[no_data_val, crops_codes['NONAG']])
    if valid_raster_filter.any():

        # count valid pixels and find dominant crops in raster
        valid_crops = raster[valid_raster_filter].ravel()
        unique_crops, counts = np.unique(valid_crops,return_counts=True)
        tot_crops = np.sum(counts)
        unique_dominant_crops = unique_crops[(100*(counts/tot_crops))>thres]
        dominant_crops_filt = np.isin(raster,unique_dominant_crops)
        dominant_crops = raster[dominant_crops_filt].ravel()
        dominant_crops_rs, dominant_crops_cs = np.nonzero(dominant_crops_filt)

        # change non dominant crops to dominant
        nn_obj = NearestNeighbors(n_neighbors=1)
        nn_obj.fit(np.array([dominant_crops_rs, dominant_crops_cs]).T)
        if len(unique_crops) > 1:

            for unique_crop, count in zip(unique_crops, counts):
                if np.isin(unique_crop,dominant_crops):
                    continue
                num_labs, labels = cv2.connectedComponents((raster == unique_crop).astype(np.uint8))
                for lab in range(1,num_labs):
                    lab_filt = labels == lab
                    lab_rs, lab_cs = np.nonzero(lab_filt)
                    _, nn_inds = nn_obj.kneighbors(np.array([lab_rs, lab_cs]).T)
                    nn_dominant_crops = dominant_crops[nn_inds]
                    unique_dominant_crops, counts_dominant = np.unique(nn_dominant_crops, return_counts=True)
                    clean_raster[lab_rs, lab_cs] = unique_dominant_crops[np.argmax(counts_dominant)]

    return clean_raster


def process_tif(ins):
    # crops usda codes
    crops_codes = {'CORN': 41, 'COTTON': 21, 'SOYBEANS': 81, 'WHEAT': 11, 'OTHER': 101, 'NONAG': 102}
    try:

        # unpack inputs
        tif, orig_tifs_folder, new_tifs_folder, thres = ins

        # sieve paramters
        sieve_retain_percentage = 2
        sieve_retain_min_size = 10

        # open dataset for reading and create copy
        ds = rasterio.open(os.path.join(orig_tifs_folder, tif))
        no_data_val = np.uint8(ds.meta['nodata'])
        meta = ds.meta.copy()
        raster = ds.read()[0]
        ds.close()

        # sum valid pixels
        num_of_valid_pix = np.sum(raster != no_data_val)
        sieve_retain_size = int(num_of_valid_pix * sieve_retain_percentage / 100)

        # clean non-agriculture pixels on boarders
        raster = clean_nonag_on_boarder(raster, crops_codes, no_data_val)

        # call seive if clu size is above minimal size
        if sieve_retain_size > sieve_retain_min_size:
            raster = sieve(raster, size=sieve_retain_size)

        # clean raster by dominant crop
        clean_raster = main_raster_cleaning(raster, crops_codes, thres, no_data_val)
        ################################################################################################################
        # clean_raster = majority_filter(clean_raster, size=5)
        # result_image = saga_shrink_and_expand(clean_raster)
        ################################################################################################################
        # check that crs is valid
        if meta['crs'] is None:
            print(f'crs in {tif} is None')
        # write new raster
        with rasterio.open(os.path.join(new_tifs_folder,tif), 'w', **meta) as wds:
            wds.write(clean_raster, 1)
    except BaseException as e:
        print(e, tif)
    return


def main_impl(orig_tifs_folder,new_tifs_folder, thres):
    # create multiprocessing inputs
    tifs = [x for x in os.listdir(orig_tifs_folder) if x.endswith('tif')]
    ins = [[x,orig_tifs_folder,new_tifs_folder, thres] for x in tifs]
    # call threads pool
    with Pool(4) as p:
        p.map(process_tif, ins)


def main_():
    print("started clu cleaning")
    print(dirname)
    thres = 30  # minimal crop percentage

    # input and output folders
    orig_tifs_folder = rf"{dirname}/tmp/output"
    new_tifs_folder = rf"{dirname}/tmp/output"
    # if not os.path.isdir(new_tifs_folder):
    #     os.makedirs(new_tifs_folder)

    # main implementation
    main_impl(orig_tifs_folder,new_tifs_folder, thres)
    print('finished cleaning')

if __name__ == '__main__':
    main_()

