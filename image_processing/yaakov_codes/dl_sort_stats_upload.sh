
target_file=$1
client_bucket=$2
CI_field=$3
geojson_filepath=$4
s3_csv_target_dir=$5

python dl_zips.py $target_file $client_bucket && \
rm -rf sorted && mkdir sorted && \
python sort_clu_chips.py $CI_field $geojson_filepath && \
python make_stats_V2.py $geojson_filepath && \
python upload_chips.py $client_bucket && \
aws s3 mv --recursive --exclude "*" --include "*.csv" ./ s3://${s3_csv_target_dir} && \
aws s3 mv --recursive --exclude "*" --include "*.json" ./ s3://${s3_csv_target_dir}