
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
parser.add_argument('-dir', '--directory', required=False, help='Specify directory that contains raster files', default=r"C:\Users\User\Documents\Hudson_2023")
parser.add_argument('-dir2', '--directory2', required=False, help='Specify directory that contains poria files', default=r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\Combined_Poria_2023")
parser.add_argument('-s', '--size', required=False, type=int, default=30, help='minimum size of sieve kernel')
parser.add_argument('-conn', '--connectivity', required=False, type=int, default=4,
                    help='set connectivity to 4 or 8')
parser.add_argument('-dt', '--dtype', required=False, type=str, default='uint8', help='raster data type')
parser.add_argument('-f', '--from_values', required=False, nargs='+', type=int, default=[0, 1, 3],
                    help='set from values to reclassify')
parser.add_argument('-t', '--to_values', required=False, nargs='+', type=int,
                    default=[102, 41, 101],
                    help='set to values to reclassify')

args = parser.parse_args()
saveDir = args.directory
saveDir2 = args.directory2



# # Get a list of all the files in the input folders
files1 = os.listdir(saveDir)
files2 = os.listdir(saveDir2)
output_folder = r"C:\Users\User\Documents\Hudson_2023\CI1_PoPr" # change to destination by CC date


#######################################################################################################################
# loop over all files in the CC rasters folder
for file1 in files1:
    # Check if the file is a raster tiff
    if file1.endswith(".tif"):
        print(file1, 'file1-first')
        raster_name = str(file1[:-4])
        # Extract the split parts of the raster name from the file name
        raster_parts = os.path.splitext(file1)[0].split("_")
        raster_parts1 = raster_parts[1]
        print(raster_parts1, 'raster_part-first')
        # define the from and to values
        from_values = args.from_values
        to_values = args.to_values

        ########################################################################
        # # if no poria needed
        with rasterio.open(os.path.join(saveDir, file1)) as src1:
            output_arr = src1.read(1).astype(args.dtype)
            # mask - true false for sieve only on crop pixels
            mask = np.where(output_arr == 0, False, True)
            output_arr = output_arr.astype(np.uint8)
            ############################################################################
            # apply sieve
            array = sieve(output_arr, size=args.size, connectivity=args.connectivity, mask=mask)
            # match CC args value to the new ones based on the USDA values.
            for fv, tv in zip(from_values, to_values):
                array = np.where(array == fv, tv, array)
            # put back 102 pixels that were runned over in sieve
            array = np.where(output_arr == 0, 102, array)
            output_profile = src1.profile
            output_profile.update({"dtype": args.dtype, "compress": 'lzw'})
            # Write the output numpy array to the output raster file

            save_name = os.path.basename(file1)[:-4].split("_")[:3]
            save_name = "_".join(save_name)
            with rasterio.open(os.path.join(output_folder, 'new_' + save_name + '_PoPr_v2.tif'), 'w',
                               **output_profile) as output_dst:
                #print(output_dst.shape, 'output_dst.shape')
                output_dst.write(array, 1)
                print(f"Finished sieving & poria & masks & reclassifying: \n{file1} \nto: {output_folder}")

