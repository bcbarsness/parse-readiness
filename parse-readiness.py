
#!/usr/bin/python
# utf-8
# USAGE: python parse-readiness.py -i <input filename> -o <output filename>
# Reduces dataset to include records with a parent, any root nodes, and only
# the most recent assessment report.

import pandas as pd
import argparse

## input args ##
parser = argparse.ArgumentParser()
parser.add_argument('-r','--root', help='Check for root nodes',required = False, action='store_true')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=False, default='out.csv')
args = parser.parse_args()

# show argument values
print ("Input file: %s" % args.input )
print ("Output file: %s" % args.output )
print("Check for root nodes? {}".format(args.root))

df = pd.read_csv(args.input, low_memory=False)
unique_uics = df.UIC.unique()
print("Total rows: {0}  Total columns: {1}  Total UICs: {2}".format(df.shape[0],
 df.shape[1], unique_uics.size))
print(list(df))

## find root UICs ##
def get_root_nodes():
    root_nodes = []
    for uic in unique_uics:
        #print(uic)
        if not (df[df['UIC'] == uic]['Parent level to child'].isin([1]).any()):
            root_nodes.append(uic)
    return(root_nodes)

if args.root:
    print("List of root nodes: {}".format(get_root_nodes()))
else:
    ##
    df = df.loc[(df['Parent level to child'] == 1) | (df['UIC'].isin(get_root_nodes()))]

    # Something to explore, do we get a performance gain by comparing python
    # date objects vs strings
    #df['RICDA'] = pd.to_datetime(df['RICDA'])

    df = df[df.groupby(['UIC'])['RICDA'].transform(max) == df['RICDA']]

    # assigns 'None' to any missing properties
    df = df.where((pd.notnull(df)), 'None')

    df.to_csv(args.output)
