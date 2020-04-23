import csv
import os
import re

project = "idr0077-valuchova-flowerlightsheet/experimentA"
path_to_data = "/uod/idr/filesets/idr0077-valuchova-flowerlightsheet"

# TODO: Handle submitter instructions to ignore and replace...
to_ignore = [
    'DIC after.czi'                     # from Supplemental toxicity
    '2019-01-17 DR5 stages 03.czi',     # from figure 4
    # we don't have these other 3
    '2019-01-17 DR5 stages 05b.czi',
    '2019-01-17 DR5 stages 07 weaker.czi',
    '2019-01-17 DR5 stages 09 ewaker.czi',
]
replace_in_figure_4 = [
    '2019-01-16 DR5 nls 07b.czi',
    '2019-01-16 DR5 nls 03.czi',
    '2019-01-16 DR5 nls 09.czi',
    '2019-01-16 DR5 nls 05.czi'
]

projection_orig_names = {
    '2018-12-18 ASY H2B 3D 8 angles_Maximum intensity projection.czi': '2018-12-18 ASY H2B bud 05 3D 8 angles.czi'
}

# iterate all images...
imgs_to_dataset = {}
tsv_rows = []
projections = []
for root, dirs, files in os.walk(path_to_data):
    for f in files:
        # We want '.czi' files but not any ...(n).czi slices
        if f.endswith('.czi') and '(' not in f and f not in to_ignore:
            fullpath = os.path.join(root, f)
            match = re.search(r'^.*(figure 0\d).*', fullpath)
            if match:
                # 'figure 01' -> 'Figure 1'
                dataset = match.group(1).title().replace(' 0', ' ')
            elif f == "2019-01-11 ASY H2B a 60min 03bud.czi":
                # Special case: handle ftp uploads
                dataset = "Figure 3"
            elif f in replace_in_figure_4:
                # Special case: handle ftp uploads
                dataset = "Figure 4"
            elif "Supplement toxicity" in fullpath:
                dataset = "Supplement toxicity"
            else:
                dataset = "???"
            print(dataset, fullpath, f)
            if f.endswith("_Maximum intensity projection.czi"):
                projections.append([dataset, fullpath, f])
            else:
                imgs_to_dataset[f] = dataset
                tsv_rows.append([dataset, fullpath, f])

# Use imgs_to_dataset mapping to assign Projections...
for row in projections:
    dataset, fullpath, f = row
    if f in projection_orig_names:
        name = projection_orig_names[f]
    else:
        name = f.replace("_Maximum intensity projection", "")
    if name in imgs_to_dataset:
        dataset = imgs_to_dataset[name]
    tsv_rows.append([dataset, fullpath, f])

# sort...
tsv_rows.sort(key=lambda row: row[0] + row[2]))

# write to .tsv
with open('idr0077-experimentA-filePaths.tsv', mode='w') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    # Project:name:idr0077-valuchova-flowerlightsheet/Dataset:name:Figure 1
    for row in tsv_rows:
        dataset, fullpath, f = row
        target = "Project:name:%s/Dataset:name:%s" % (project, dataset)
        tsv_writer.writerow([target, fullpath, f])
