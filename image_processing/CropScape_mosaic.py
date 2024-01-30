import os
from rasterio.features import sieve
import argparse
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import numpy as np
import geopandas as gpd
from osgeo import gdal

# define arg
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--size', required=False, type=int, default=20, help='minimum size of sieve kernel')
parser.add_argument('-conn', '--connectivity', required=False, type=int, default=4,
                    help='set connectivity to 4 or 8')
parser.add_argument('-dt', '--dtype', required=False, type=str, default='uint8', help='raster data type')
parser.add_argument('-f', '--from_values', required=False, nargs='+', type=int, default=[0, 1, 2, 5, 23, 7],
                    help='set from values to reclassify')
parser.add_argument('-t', '--to_values', required=False, nargs='+', type=int,
                    default=[102, 41, 21, 81, 11, 101],
                    help='set to values to reclassify')
args = parser.parse_args()

tiff = r"C:\Users\User\Documents\CropScape\CropScape_2021_cut.tif"

with rasterio.open(tiff) as src1:
    print(src1)
    output_arr = src1.read(1).astype(args.dtype)
    print(output_arr)
    nonActiveList =[61, 63, 64, 65, 82, 83, 87, 88, 111, 112, 121, 122, 123, 124, 131, 141, 142, 143, 152, 176, 190, 195]
    # # Replace the specified values with 0
    output_arr = np.where(np.isin(output_arr, nonActiveList), 0, output_arr)
    corn = [12, 13, 225, 226, 228, 237]
    output_arr = np.where(np.isin(output_arr, corn), 1, output_arr)
    soybeans = [5, 26, 241, 254]
    output_arr = np.where(np.isin(output_arr, soybeans), 5, output_arr)
    cotton = [232, 238, 239]
    output_arr = np.where(np.isin(output_arr, cotton), 2, output_arr)
    output_arr = np.where(output_arr == 3, 7, output_arr)
    output_arr = np.where(output_arr == 4, 7, output_arr)
    output_arr = np.where((output_arr >= 6) & (output_arr < 23), 7, output_arr)
    output_arr = np.where(output_arr >= 24, 7, output_arr)
    #print(output_arr)
    mask = np.where(output_arr == 0, False, True)
    output_arr = output_arr.astype(np.uint8)
    ############################################################################
    # apply sieve
    array = sieve(output_arr, size=args.size, connectivity=args.connectivity, mask=mask)
    # match CC args value to the new ones based on the USDA values.
    from_values = args.from_values
    to_values = args.to_values
    for fv, tv in zip(from_values, to_values):
        array = np.where(array == fv, tv, array)
    # put back 102 pixels that were runned over in sieve
    array = np.where(output_arr == 0, 102, array)
    output_profile = src1.profile
    output_profile.update({"dtype": args.dtype, "compress": 'lzw'})
    with rasterio.open(r"C:\Users\User\Documents\CropScape\CropScape_2021_cut_PoPr.tif", 'w', **output_profile) as output_dst:
        output_dst.write(array, 1)
        print(f"Finished sieving & poria")









