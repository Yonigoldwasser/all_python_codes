import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
# Open the source and target raster files
with rasterio.open(r"C:\Users\User\Documents\CropScape\2017_30m_cdls\2017_30m_cdls.tif") as dest, rasterio.open(r'C:\Users\User\Documents\CropScape\CropScape2019_4326.tif') as src:
    # Reproject the input raster to match the multiplying raster
    profile = src.profile
    destr = np.empty_like(src.read(1))
    reproject(
        dest.read(1),
        destr,
        src_transform=dest.transform,
        src_crs=dest.crs,
        dst_transform=src.transform,
        dst_crs=src.crs,
        resampling=Resampling.nearest)
    # Update the profile with LZW compression
    profile.update(compress='lzw')
# Open the output raster file for writing\n",
with rasterio.open((r"C:\Users\User\Documents\CropScape\CropScape2017_4326.tif"), "w", **profile) as dst2:
    dst2.write(destr, 1)


