
Y_num=$1
client_bucket=$2
CI_field=$3
geojson_filepath=$4
updated_geojson_filepath=$5
forecast_file=$6
s3_csv_target_dir=$7
geojson_s3_csv_target_dir=$8
##
rm -rf sorted && mkdir sorted && \
python corn_cotton_approved_by_majority_3tiles.py $Y_num $geojson_filepath && \
python 2024_sort_clu_chips_CI.py $CI_field $geojson_filepath && \
python make_stats_v2_CI.py $geojson_filepath $client_bucket $forecast_file && \
rm -rf sorted && mkdir sorted && \
python 2024_sort_clu_chips_CI.py $CI_field $updated_geojson_filepath && \
python make_stats_CI.py $updated_geojson_filepath $client_bucket && \
python upload_chips_CI.py $client_bucket && \
aws s3 mv --recursive --exclude "*" --include "crops_acres*.csv" ./ s3://${s3_csv_target_dir} && \
aws s3 mv --recursive --exclude "*" --include "*.json" ./ s3://${s3_csv_target_dir} && \
aws s3 cp $updated_geojson_filepath s3://${geojson_s3_csv_target_dir}