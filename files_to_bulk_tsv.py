import csv
import os
import re

project = "idr0077-valuchova-flowerlightsheet/experimentA"
path_to_data = "/uod/idr/filesets/idr0077-valuchova-flowerlightsheet"

# TODO: Unclear how to handle submitter instructions to ignore and replace??
to_ignore = [
    'DIC after.czi'
    '2019-01-17 DR5 stages 03.czi',
    '2019-01-17 DR5 stages 05b.czi',
    '2019-01-17 DR5 stages 07 weaker.czi',
    '2019-01-17 DR5 stages 09 ewaker.czi',
]
replace_with = [
    '2019-01-16 DR5 nls 07b.czi',
    '2019-01-16 DR5 nls 03.czi',
    '2019-01-16 DR5 nls 09.czi'
]

with open('idr0077-experimentA-filePaths.tsv', mode='w') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    # iterate all images...
    for root, dirs, files in os.walk(path_to_data):
        archive_root = os.path.relpath(root, path_to_data)
        imgs_in_dir = []
        for f in files:
            # We want '.czi' files but not all ...(123).czi slices
            if f.endswith('.czi') and '(' not in f and f not in to_ignore:
                imgs_in_dir.append(f)
        if len(imgs_in_dir) == 0:
            # didn't find any files when we exclude '('
            # Try to allow '(1).czi'
            for f in files:
                if f.endswith('(1).czi'):
                    imgs_in_dir.append(f)
        for f in imgs_in_dir:
            fullpath = os.path.join(root, f)
            match = re.search(r'^.*(figure 0\d).*', fullpath)
            if match:
                dataset = match.group(1).title()
            else:
                dataset = "Supplement toxicity"
            # Project:name:idr0077-valuchova-flowerlightsheet/Dataset:name:Figure 1
            target = "Project:name:%s/Dataset:name:%s" % (project, dataset)
            print(target, fullpath, f)
            tsv_writer.writerow([target, fullpath, f])
