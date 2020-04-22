import csv
import os

project = "Project:name:idr0077-valuchova-flowerlightsheet/experimentA"
path_to_data = "/uod/idr/filesets/idr0077-valuchova-flowerlightsheet"

with open('idr0077-experimentA-filePaths.tsv', mode='w') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    # iterate all images...
    for root, dirs, files in os.walk(path_to_data):
        archive_root = os.path.relpath(root, path_to_data)
        imgs_in_dir = []
        for f in files:
            # We want '.czi' files but not all ...(123).czi slices
            if f.endswith('.czi') and '(' not in f:
                imgs_in_dir.append(f)
        if len(imgs_in_dir) == 0:
            # didn't find any files when we exclude '('
            # Try to allow '(1).czi'
            for f in files:
                if f.endswith('(1).czi'):
                    imgs_in_dir.append(f)
        for f in imgs_in_dir:
            fullpath = os.path.join(root, f)
            print(fullpath)
            # tsv_writer.writerow([target, image_path, new_name])
