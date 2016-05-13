## convert repRPKM table to MySQL table using pandas

import os, sys
from sqlalchemy import create_engine
import numpy as np
import pandas as pd

# conn = MySQLdb.connect(host='localhost',user='root', passwd='',db='hairgel')
conn = create_engine('mysql://root:@localhost/hairgel', echo_pool=True)

WORKDIR = '/Users/zichen/Documents/Zichen_Projects/Rendl_RNAseq4/'
os.chdir(WORKDIR)

df = pd.read_csv('repRpkmMatrix_featureCounts_batch_1_3.csv')

# print df.head()
# print df.shape

zone_celltypes = map(lambda x: x.split('$')[0], df.columns[1:])

df_to_insert = pd.DataFrame({'gene': df['gene']})

for zone_celltype in zone_celltypes:
	columns = df.columns[1:][np.in1d(zone_celltypes, [zone_celltype])]
	print columns
	avg = df[columns].mean(axis=1)
	sd = df[columns].std(axis=1)
	print avg.shape, sd.shape, sd.count()
	df_to_insert[zone_celltype + '_avg'] = avg
	df_to_insert[zone_celltype + '_sd'] = sd

print df_to_insert.head()
print df_to_insert.shape
df_to_insert.to_sql('rpkms4', conn, chunksize=100,
	flavor='mysql', index_label='id', if_exists='replace')

