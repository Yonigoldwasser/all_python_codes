
from osgeo import gdal
import os

####################################################
# change rasters folder path
####################################################

def merge_tifs_in_folder(input_folder, output_file):
    # Get all the TIFF files in the input folder
    print('starting merge')
    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tif')]

    # Use the GDAL merge utility from the API
    gdal.BuildVRT("temp.vrt", tif_files)
    gdal.Translate(output_file, "temp.vrt", creationOptions=["COMPRESS=LZW"])
    os.remove("temp.vrt")
    print("finished merge")
    return output_file

def translate_tif(input_file, output_file):
    print('starting translate')
    # Open the source file
    src_ds = gdal.Open(input_file, gdal.GA_ReadOnly)

    # GDAL Translate
    gdal.Translate(output_file, src_ds, xRes=0.00015, yRes=0.00015, creationOptions=["COMPRESS=LZW"])
    print("finished translate")
    return output_file


# Example of usage:
folder_path = r"C:\Users\User\Documents\CI_small_grid_comparison\20_grid_1_6_15_7_only_grid_reg_model\20_grid_1_6_15_7_only_grid_reg_model_2024-01-16_1705407304679_ci_preds\Popr"
merged_file = merge_tifs_in_folder(folder_path, r"C:\Users\User\Documents\CI_small_grid_comparison\20_grid_1_6_15_7_only_grid_reg_model\20_grid_1_6_15_7_only_grid_reg_model_2024-01-16_1705407304679_ci_preds\Popr\20_grid_only_grid_reg_model_1_6_15_7_merged.tif")
translated_file = translate_tif(merged_file, r"C:\Users\User\Documents\CI_small_grid_comparison\20_grid_1_6_15_7_only_grid_reg_model\20_grid_1_6_15_7_only_grid_reg_model_2024-01-16_1705407304679_ci_preds\Popr\20_grid_only_grid_reg_model_1_6_15_7_10m_cropid.tif")

