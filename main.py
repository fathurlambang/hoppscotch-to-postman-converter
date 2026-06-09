import os

from hoppscotch_to_postman_converter import (
    convert_hoppscotch_to_postman_collection_v21,
    convert_hoppscotch_env_to_postman_env
)

# Convert to Postman v2.1
convert_hoppscotch_to_postman_collection_v21('Hirevo.json')


# Convert to Postman environment
# Place Hoppscotch environment JSON files in hoppscotch_exported_files/ folder

exported_dir = 'hoppscotch_exported_files'
if os.path.exists(exported_dir):
    for file in os.listdir(exported_dir):
        if file.endswith('.json'):
            convert_hoppscotch_env_to_postman_env(f'{exported_dir}/{file}')
else:
    print(f'Folder {exported_dir} not found, skipping environment conversion')
