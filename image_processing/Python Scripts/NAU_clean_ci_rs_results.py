# import os
# import rasterio
# import numpy as np
# from multiprocessing import Pool
# import matplotlib.pyplot as plt
# from rasterio.features import sieve
# import cv2
# from sklearn.neighbors import NearestNeighbors
#
#
# def clean_nonag_on_boarder(raster, crops_codes, no_data_val):
#
#     rows, cols = raster.shape
#
#     # find non-agg pixels
#     nonag_rs, nonag_cs = np.nonzero(raster == crops_codes['NONAG'])
#
#     # iterate over non-agg pixels
#     for nonag_r, nonag_c in zip(nonag_rs, nonag_cs):
#
#         # non-agg neighbors
#         nonag_neis = raster[max(0,nonag_r-1):min(nonag_r+2,rows),max(0,nonag_c-1):min(nonag_c+2,cols)]
#
#         # check if neighbors are on boarder
#         if (nonag_neis == no_data_val).any():
#
#             # change non-agg neighbors to dominant crop
#             nonag_neis = nonag_neis[~np.isin(nonag_neis,[crops_codes['NONAG'], no_data_val])].ravel()
#             if len(nonag_neis):
#                 vals, counts = np.unique(nonag_neis,return_counts=True)
#                 raster[nonag_r,nonag_c] = vals[np.argmax(counts)]
#
#     return raster
#
#
# def main_raster_cleaning(raster, crops_codes, thres, no_data_val):
#
#     # copy cleaned raster
#     clean_raster = np.copy(raster)
#
#     # filter non-agg pixels
#     valid_raster_filter = ~np.isin(raster,[no_data_val, crops_codes['NONAG']])
#     if valid_raster_filter.any():
#
#         # count valid pixels and find dominant crops in raster
#         valid_crops = raster[valid_raster_filter].ravel()
#         unique_crops, counts = np.unique(valid_crops,return_counts=True)
#         tot_crops = np.sum(counts)
#         unique_dominant_crops = unique_crops[(100*(counts/tot_crops))>thres]
#         dominant_crops_filt = np.isin(raster,unique_dominant_crops)
#         dominant_crops = raster[dominant_crops_filt].ravel()
#         dominant_crops_rs, dominant_crops_cs = np.nonzero(dominant_crops_filt)
#
#         # change non dominant crops to dominant
#         nn_obj = NearestNeighbors(n_neighbors=1)
#         nn_obj.fit(np.array([dominant_crops_rs, dominant_crops_cs]).T)
#         if len(unique_crops) > 1:
#
#             for unique_crop, count in zip(unique_crops, counts):
#                 if np.isin(unique_crop,dominant_crops):
#                     continue
#                 num_labs, labels = cv2.connectedComponents((raster == unique_crop).astype(np.uint8))
#                 for lab in range(1,num_labs):
#                     lab_filt = labels == lab
#                     lab_rs, lab_cs = np.nonzero(lab_filt)
#                     _, nn_inds = nn_obj.kneighbors(np.array([lab_rs, lab_cs]).T)
#                     nn_dominant_crops = dominant_crops[nn_inds]
#                     unique_dominant_crops, counts_dominant = np.unique(nn_dominant_crops, return_counts=True)
#                     clean_raster[lab_rs, lab_cs] = unique_dominant_crops[np.argmax(counts_dominant)]
#
#     return clean_raster
#
#
# def process_tif(ins):
#
#     # crops usda codes
#     crops_codes = {'CORN': 41, 'COTTON': 21, 'SOYBEANS': 81, 'WHEAT': 11, 'OTHER': 101, 'NONAG': 102}
#     try:
#
#         # unpack inputs
#         tif, orig_tifs_folder, new_tifs_folder, thres = ins
#
#         # sieve paramters
#         sieve_retain_percentage = 2
#         sieve_retain_min_size = 10
#
#         # open dataset for reading and create copy
#         ds = rasterio.open(os.path.join(orig_tifs_folder,tif))
#         no_data_val = np.uint8(ds.meta['nodata'])
#         meta = ds.meta.copy()
#         raster = ds.read()[0]
#         ds.close()
#
#         # sum valid pixels
#         num_of_valid_pix = np.sum(raster != no_data_val)
#         sieve_retain_size = int(num_of_valid_pix * sieve_retain_percentage / 100)
#
#         # clean non-agriculture pixels on boarders
#         raster = clean_nonag_on_boarder(raster, crops_codes, no_data_val)
#
#         # call seive if clu size is above minimal size
#         if sieve_retain_size > sieve_retain_min_size:
#             raster = sieve(raster, size=sieve_retain_size)
#
#         # clean raster by dominant crop
#         clean_raster = main_raster_cleaning(raster, crops_codes, thres, no_data_val)
#
#         # check that crs is valid
#         if meta['crs'] is None:
#             print(f'crs in {tif} is None')
#         # write new raster
#         print(clean_raster)
#         clean_raster = sieve(clean_raster, size=30, connectivity=4)
#
#         with rasterio.open(os.path.join(new_tifs_folder,tif), 'w', **meta) as wds:
#             wds.write(clean_raster, 1)
#     except BaseException as e:
#         print(e, tif)
#     return
#
#
# def main_impl(orig_tifs_folder,new_tifs_folder, thres):
#
#     # create multiprocessing inputs
#     tifs = [x for x in os.listdir(orig_tifs_folder) if x.endswith('tif')]
#     ins = [[x,orig_tifs_folder,new_tifs_folder, thres] for x in tifs]
#
#     # call threads pool
#     with Pool(4) as p:
#         p.map(process_tif, ins)
#
#
# def main_():
#
#     thres = 30  # minimal crop percentage
#
#     # input and output folders
#     orig_tifs_folder = r"C:\Users\User\Desktop\test\benny_border_smoothing\nau_smoothing"
#     new_tifs_folder = r"C:\Users\User\Desktop\test\benny_border_smoothing\nau_smoothing\nau_after_smothing"
#     new_tifs_folder2 = r"C:\Users\User\Desktop\test\benny_border_smoothing\nau_smoothing\nau_after_smothing"
#     # array = sieve(output_arr, size=args.size, connectivity=args.connectivity, mask=mask)
#
#     if not os.path.isdir(new_tifs_folder):
#         os.makedirs(new_tifs_folder)
#
#     # main implementation
#     main_impl(orig_tifs_folder,new_tifs_folder, thres)
#
#
# if __name__ == '__main__':
#     main_()

import os
import rasterio
import numpy as np
from multiprocessing import Pool
from rasterio.features import sieve
import cv2
from sklearn.neighbors import NearestNeighbors
from scipy import ndimage
from scipy.ndimage import median_filter, binary_opening
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define the majority filter function
def majority_filter(input_array, size=15, ignore_value=0):
    # Create a structure element for filtering, using a square connectivity of the given size
    struct_element = np.ones((size, size))

    # Define the mode filter function with a condition to ignore specific pixel value
    def mode_filter(values):
        # Filter out the ignore_value (e.g., 0) from the values
        filtered_values = values[values != ignore_value]

        if len(filtered_values) == 0:
            # If all values are to be ignored, return the ignore_value
            return ignore_value

        # Avoid changing pixels with a specific value (e.g., 241)
        if values[len(values) // 2] == 241:
            return 241

        unique_values, counts = np.unique(filtered_values, return_counts=True)
        return unique_values[np.argmax(counts)]

    # Apply the majority filter
    filtered_array = ndimage.generic_filter(input_array, function=mode_filter, size=size, mode='constant',
                                            cval=ignore_value, footprint=struct_element)
    return filtered_array

def clean_nonag_on_boarder(raster, crops_codes, no_data_val):
    rows, cols = raster.shape
    nonag_rs, nonag_cs = np.nonzero(raster == crops_codes['NONAG'])

    for nonag_r, nonag_c in zip(nonag_rs, nonag_cs):
        nonag_neis = raster[max(0, nonag_r - 1):min(nonag_r + 2, rows), max(0, nonag_c - 1):min(nonag_c + 2, cols)]
        if (nonag_neis == no_data_val).any():
            nonag_neis = nonag_neis[~np.isin(nonag_neis, [crops_codes['NONAG'], no_data_val])].ravel()
            if len(nonag_neis):
                vals, counts = np.unique(nonag_neis, return_counts=True)
                raster[nonag_r, nonag_c] = vals[np.argmax(counts)]
    return raster

def main_raster_cleaning(raster, crops_codes, thres, no_data_val):
    clean_raster = np.copy(raster)
    valid_raster_filter = ~np.isin(raster, [no_data_val, crops_codes['NONAG']])

    if valid_raster_filter.any():
        valid_crops = raster[valid_raster_filter].ravel()
        unique_crops, counts = np.unique(valid_crops, return_counts=True)
        tot_crops = np.sum(counts)
        unique_dominant_crops = unique_crops[(100 * (counts / tot_crops)) > thres]
        dominant_crops_filt = np.isin(raster, unique_dominant_crops)
        dominant_crops = raster[dominant_crops_filt].ravel()
        dominant_crops_rs, dominant_crops_cs = np.nonzero(dominant_crops_filt)
        nn_obj = NearestNeighbors(n_neighbors=1)
        nn_obj.fit(np.array([dominant_crops_rs, dominant_crops_cs]).T)

        if len(unique_crops) > 1:
            for unique_crop, count in zip(unique_crops, counts):
                if np.isin(unique_crop, dominant_crops):
                    continue
                num_labs, labels = cv2.connectedComponents((raster == unique_crop).astype(np.uint8))
                for lab in range(1, num_labs):
                    lab_filt = labels == lab
                    lab_rs, lab_cs = np.nonzero(lab_filt)
                    _, nn_inds = nn_obj.kneighbors(np.array([lab_rs, lab_cs]).T)
                    nn_dominant_crops = dominant_crops[nn_inds]
                    unique_dominant_crops, counts_dominant = np.unique(nn_dominant_crops, return_counts=True)
                    clean_raster[lab_rs, lab_cs] = unique_dominant_crops[np.argmax(counts_dominant)]

    return clean_raster

def process_tif(ins):
    crops_codes = {'CORN': 41, 'COTTON': 21, 'SOYBEANS': 81, 'WHEAT': 11, 'OTHER': 101, 'NONAG': 102}
    try:
        tif, orig_tifs_folder, new_tifs_folder, thres = ins
        sieve_retain_percentage = 2
        sieve_retain_min_size = 10
        ds = rasterio.open(os.path.join(orig_tifs_folder, tif))
        no_data_val = np.uint8(ds.meta['nodata'])
        meta = ds.meta.copy()
        raster = ds.read()[0]
        ds.close()
        num_of_valid_pix = np.sum(raster != no_data_val)
        sieve_retain_size = int(num_of_valid_pix * sieve_retain_percentage / 100)
        raster = clean_nonag_on_boarder(raster, crops_codes, no_data_val)
        if sieve_retain_size > sieve_retain_min_size:
            raster = sieve(raster, size=sieve_retain_size)

        clean_raster = main_raster_cleaning(raster, crops_codes, thres, no_data_val)
        plt.imshow(clean_raster)
        plt.show()
        clean_raster = majority_filter(clean_raster)
        clean_raster = majority_filter(clean_raster)

        # masked_raster = np.ma.masked_equal(clean_raster, no_data_val)  # Mask values of 102
        # print(masked_raster)
        # plt.imshow(masked_raster)
        # plt.show()

        # median_filtered_raster = median_filter(masked_raster, size=15)
        # plt.imshow(median_filtered_raster)
        # plt.show()
        # Define the "no data" value
        # no_data_value = 241 # Replace with your specific "no data" value
        #
        # # Create a binary mask for "no data" pixels
        # no_data_mask = (clean_raster != no_data_value)
        #
        # # Apply the median filter only to non-"no data" pixels
        # clean_raster = clean_raster # Create a copy of the original image
        # kernel_size = 5  # Adjust the kernel size as needed
        # clean_raster[no_data_mask] = cv2.medianBlur(clean_raster, kernel_size)[no_data_mask]
        # plt.imshow(clean_raster)
        # plt.show()
        with rasterio.open(os.path.join(new_tifs_folder, tif), 'w', **meta) as wds:
            wds.write(clean_raster, 1)
    except BaseException as e:
        print(e, tif)
    return

def main_impl(orig_tifs_folder, new_tifs_folder, thres):
    tifs = [x for x in os.listdir(orig_tifs_folder) if x.endswith('tif')]
    ins = [[x, orig_tifs_folder, new_tifs_folder, thres] for x in tifs]
    with Pool(4) as p:
        p.map(process_tif, ins)

def main_():
    thres = 30
    orig_tifs_folder = r"C:\Users\User\Desktop\test\benny_border_smoothing\nau_smoothing"
    new_tifs_folder = r"C:\Users\User\Desktop\test\benny_border_smoothing\nau_smoothing\nau_after_smothing"

    if not os.path.isdir(new_tifs_folder):
        os.makedirs(new_tifs_folder)

    main_impl(orig_tifs_folder, new_tifs_folder, thres)

if __name__ == '__main__':
    main_()
