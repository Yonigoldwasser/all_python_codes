
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
# folder of CI tifs, poria tifs, cropscape tifs, output folder for masked tifs, grid shapfile folder, output of preprocess CI tifs.
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-dir', '--directory', required=False, help='Specify directory that contains raster files', default=r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CI_by_area_comparison\Y9_by_crop_area_2023_08_30_raster+json")
parser.add_argument('-dir2', '--directory2', required=False, help='Specify directory that contains poria files', default=r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\Combined_Poria_2023")
parser.add_argument('-s', '--size', required=False, type=int, default=15, help='minimum size of sieve kernel')
parser.add_argument('-conn', '--connectivity', required=False, type=int, default=4,
                    help='set connectivity to 4 or 8')
parser.add_argument('-dt', '--dtype', required=False, type=str, default='uint8', help='raster data type')
parser.add_argument('-f', '--from_values', required=False, nargs='+', type=int, default=[0, 1, 2, 3, 4, 5, 7],
                    help='set from values to reclassify')
parser.add_argument('-t', '--to_values', required=False, nargs='+', type=int,
                    default=[102, 41, 21, 81, 11, 81, 101],
                    help='set to values to reclassify')

parser.add_argument('-output_folder2', '--output_folder2', required=False, help='Specify directory that will contain cropscape masked tiles',
                    default=r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CropScape_years_tiles")
parser.add_argument('-shapefile_path', '--shapefile_path', required=False, help='Specify directory that contains us_grid shapefile',
                    default=r"C:\Users\User\Documents\ProAg_FMH_CC_2023\Combined_CC_2023_vars\Combined_us_grid_clus_2023\us_grid_proag_FMH_2023.shp")
args = parser.parse_args()
saveDir = args.directory
Ynumber = "_" + saveDir.split("\\")[-1].split("_")[0]
saveDir2 = args.directory2
output_folder2 = args.output_folder2
shapefile_path = args.shapefile_path


# us_grid tiles shapefile for clipping the cropscape raster to the CC relevant tile.
shapefile = gpd.read_file(shapefile_path)

# # Get a list of all the files in the input folders
files1 = os.listdir(saveDir)
files2 = os.listdir(saveDir2)

# Postprocess tiffs output folder -  change to destination by CC date
output_folder = r"C:\Users\User\Documents\ProAg_2023_CC\ProAg_2023_InSeason\CI_by_area_comparison\Y9_by_area_PoPr_rasters"

#######################################################################################################################
# def for PoPr tiffs. non ag 102 from poria will give a 102 value once multiplied by 0 other of CC
# def custom_multiply_arrays(a, b):
#     result = np.multiply(a, b)
#     result[np.logical_and(a == 0, b == 10)] = 102
#     return result

#######################################################################################################################
## with poria ###
# loop over all files in the CC rasters folder
for file1 in files1[:2]:
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

        # Loop through each file in the second folder - Poria rasters
        for file2 in files2:
            # Check if the file is a raster and if its split parts match the first raster split parts - match CC rasters (regular or masked) and poria raster names.
            if file2.endswith(".tif"):
                raster_parts2 = os.path.splitext(file2)[0].split("_")
                raster_parts2 = raster_parts2[1]
                print(raster_parts2,'raster_parts2')
                if len(raster_parts1) == len(raster_parts2) and all(
                        raster_parts1 == raster_parts2 for raster_parts1, raster_parts2 in
                        zip(raster_parts1, raster_parts2)):
                        print("yes")
                        # Open the two rasters using rasterio - CC and poria
                        with rasterio.open(os.path.join(saveDir, file1)) as src1, rasterio.open(os.path.join(saveDir2, file2)) as src2:
                            # Reproject the input raster to match the multiplying raster
                            reprojected_input_arr = np.empty_like(src1.read(1).astype(args.dtype))
                            reproject(
                                src2.read(1).astype(args.dtype),
                                reprojected_input_arr,
                                src_transform=src2.transform,
                                src_crs=src2.crs,
                                dst_transform=src1.transform,
                                dst_crs=src1.crs,
                                resampling=Resampling.nearest)
                            ########################################################################Poria######
                            reprojected_poria_arr = np.where(reprojected_input_arr > 0, 1, 0)
                            CI_raster = src1.read(1).astype(args.dtype)
                            output_arr = np.multiply(CI_raster, reprojected_poria_arr)
                            output_arr = output_arr.astype(args.dtype)
                            ########################################################################
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
                            with rasterio.open(os.path.join(output_folder, 'new_' + save_name + Ynumber + '_PoPr.tif'), 'w',
                                               **output_profile) as output_dst:
                                #print(output_dst.shape, 'output_dst.shape')
                                output_dst.write(array, 1)
                                print(f"Finished sieving & poria & masks & reclassifying: \n{file1} \nto: {output_folder}")
#######################################################################################################################
######################### if no poria needed #############################################
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
            # save_name = "_".join(save_name)
            # with rasterio.open(os.path.join(output_folder, 'new_' + save_name + Ynumber + '_PoPr.tif'), 'w',
            #                    **output_profile) as output_dst:
            #     #print(output_dst.shape, 'output_dst.shape')
            #     output_dst.write(array, 1)
            #     print(f"Finished sieving & poria & masks & reclassifying: \n{file1} \nto: {output_folder}")