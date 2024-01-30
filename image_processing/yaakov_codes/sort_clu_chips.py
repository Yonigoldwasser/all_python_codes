import subprocess
import json
import glob
import os
import sys
import logging
from concurrent import futures

CI_field = sys.argv[1]
with open(sys.argv[2]) as src: # takes the updated (push/nopush) json file that we wrote its path when starting code in command line (second argument in the command line)
  features=json.load(src)['features']
print(len(features))
local_dirs = glob.glob('*')
local_dir_names = {}
for dir in local_dirs:
  if dir.startswith('Y'):
    try:
      int(dir.split('_')[0][1:])
      local_dir_names[dir] = glob.glob(f'{dir}/**/*.tif',recursive=True)
    except:
      pass

sorting = {}

filemap = {}
# making lists for all file in each classification folders.
for k in local_dir_names:
  filemap[k] = {}
  for f in local_dir_names[k]:
    fname = os.path.basename(f)
    filemap[k][fname]=f

threads = []
def sort_file(f, sorting_dict):
  props = f['properties']
  cluid=props['CommonLand']                          # change to comman unit
  dirname=props[CI_field]
  if dirname.lower() == 'f':
    return
  try:
    subprocess.run(f'cp {filemap[dirname][cluid+".tif"]} sorted/',shell=True).check_returncode()
    sorting_dict[cluid] = dirname
  except Exception as ex:
    logging.getLogger().exception(cluid)
    sorting_dict[cluid]='not found'
with futures.ThreadPoolExecutor(max_workers=20) as exec:
  for f in features:
    threads.append(exec.submit(sort_file,f,sorting))

for t in futures.as_completed(threads):
  pass
with open(f'sorting_{CI_field}.json','w') as out:
  json.dump(sorting, out)