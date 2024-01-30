
#target_file=$1
client_bucket=$1
CI_field=$2
geojson_filepath=$3
s3_csv_target_dir=$4
#
#python dl_zips.py $target_file $client_bucket && \
rm -rf sorted && mkdir sorted && \
python sort_clu_chips_CI.py $CI_field $geojson_filepath && \
python make_stats_CI.py $geojson_filepath $client_bucket && \
python upload_chips_CI.py $client_bucket && \
aws s3 mv --recursive --exclude "*" --include "crops_acres*.csv" ./ s3://${s3_csv_target_dir} && \
aws s3 mv --recursive --exclude "*" --include "*.json" ./ s3://${s3_csv_target_dir}