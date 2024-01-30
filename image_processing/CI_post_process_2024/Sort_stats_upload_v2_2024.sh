
#target_file=$1
client_bucket=$1
CI_field=$2
geojson_filepath=$3
updated_geojson_filepath=$4
forecast_file=$5
s3_csv_target_dir=$6
geojson_s3_csv_target_dir=$7
##
rm -rf sorted && mkdir sorted && \
python sort_clu_chips_CI.py $CI_field $geojson_filepath && \
python make_stats_v2_CI.py $geojson_filepath $client_bucket $forecast_file && \
rm -rf sorted && mkdir sorted && \
python sort_clu_chips_CI.py $CI_field $updated_geojson_filepath && \
python make_stats_CI.py $updated_geojson_filepath $client_bucket && \
python upload_chips_CI.py $client_bucket && \
aws s3 mv --recursive --exclude "*" --include "crops_acres*.csv" ./ s3://${s3_csv_target_dir} && \
aws s3 mv --recursive --exclude "*" --include "*.json" ./ s3://${s3_csv_target_dir} && \
aws s3 cp $updated_geojson_filepath s3://${geojson_s3_csv_target_dir}