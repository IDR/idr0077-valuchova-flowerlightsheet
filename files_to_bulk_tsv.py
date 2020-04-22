import csv
import os

project = "Project:name:idr0077-valuchova-flowerlightsheet/experimentA"
path_to_data = "/uod/idr/filesets/idr0077-valuchova-flowerlightsheet"

with open('idr0077-experimentA-filePaths.tsv', mode='w') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    # iterate all images...
    for root, dirs, files in os.walk(path_to_data):
        archive_root = os.path.relpath(root, path_to_data)
        for f in files:
            fullpath = os.path.join(root, f)
            # Only want .czi but NOT ...(1).czi stack slices
            if f.endswith('.czi') and '(' not in f:
                print(fullpath)
                # tsv_writer.writerow([target, image_path, new_name])
