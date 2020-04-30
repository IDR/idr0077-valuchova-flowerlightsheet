import csv
import os
import re

project = "idr0077-valuchova-flowerlightsheet/experimentA"
path_to_data = "/uod/idr/filesets/idr0077-valuchova-flowerlightsheet"

# TODO: Handle submitter instructions to ignore and replace...
to_ignore = [
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20191219-disk02/Supplement toxicity/2018-12-03 HTR 03 buds cultivation budN05 FEPcap framefull mag1.7 Zopt 2angles 50ms G20 R10 a 60min/12 48/14 48/15 18/1612/DIC after.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20191219-disk01/figure 04/DR5 staging/2019-01-17 DR5 stages 03.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20191219-disk01/figure 04/DR5 staging/2019-01-17 DR5 stages 05b.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20191219-disk01/figure 04/DR5 staging/2019-01-17 DR5 stages 07 weaker.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20191219-disk01/figure 04/DR5 staging/2019-01-17 DR5 stages 09 ewaker.czi',
    # MIPs replaced with 20200429-ftp MIPs...
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/2018-12-18 ASY H2B bud 05 3D 8 angles_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200411-ftp/2019-01-25 DR5 nls 07 a 120min_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/2019-01-25 DR5 nls 07 a 120min_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/2018-10-31 PCNA ON 035 065 bud line 12 a15min singleside_G1_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/045 a 2 minC_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200411-ftp/2018-08-27 smg 04 a 5min_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/2018-08-27 smg 04 a 5min_Maximum intensity projection.czi',
    '/uod/idr/filesets/idr0077-valuchova-flowerlightsheet/20200428-ftp/2019-01-11 FEP HTR cotrol toxicity 03_Maximum intensity projection.czi',
]
replace_in_figure_4 = [
    '2019-01-16 DR5 nls 07b.czi',
    '2019-01-16 DR5 nls 03.czi',
    '2019-01-16 DR5 nls 09.czi',
    '2019-01-16 DR5 nls 05.czi'
]

projection_orig_names = {
    '2018-12-18 ASY H2B 3D 8 angles_Maximum intensity projection.czi': '2018-12-18 ASY H2B bud 05 3D 8 angles.czi',  # Figure 2
    '2019-01-22 Female ASY H2B 0_Maximum intensity projection.85 a 10min.czi': '2019-01-22 Female ASY H2B 0.85 a 10min.czi', # Figure 1
}

# iterate all images...
imgs_to_dataset = {}
tsv_rows = []
projections = []
for root, dirs, files in os.walk(path_to_data):
    for f in files:
        fullpath = os.path.join(root, f)
        # We want '.czi' files but not any ...(n).czi slices
        if f.endswith('.czi') and '(' not in f and fullpath not in to_ignore:
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
            if "Maximum intensity projection" in f:
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
tsv_rows.sort(key=lambda row: row[0] + row[2])

# write to .tsv
with open('idr0077-experimentA-filePaths.tsv', mode='w') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    # Project:name:idr0077-valuchova-flowerlightsheet/Dataset:name:Figure 1
    for row in tsv_rows:
        dataset, fullpath, f = row
        target = "Project:name:%s/Dataset:name:%s" % (project, dataset)
        tsv_writer.writerow([target, fullpath, f])
