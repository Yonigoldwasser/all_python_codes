
#shell for running mosaic command all at once.
CI_number_mosaic_file=$1

gdal_merge.py -o ${CI_number_mosaic_file}_merged.tif -co COMPRESS=LZW zips/*tif && \
gdal_translate -tr 0.00015 0.00015 -co COMPRESS=LZW ${CI_number_mosaic_file}_merged.tif ${CI_number_mosaic_file}_10m_cropid.tif && \
aws s3 cp ${CI_number_mosaic_file}_10m_cropid.tif s3://pw-crop-classification-rs/crop-classification/2023/rs_input/