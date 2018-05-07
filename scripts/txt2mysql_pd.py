## convert repRPKM table to MySQL table using pandas

import os, sys
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, INTEGER
import numpy as np
import pandas as pd

# conn = MySQLdb.connect(host='localhost',user='root', passwd='',db='hairgel')
conn = create_engine('mysql://root:@localhost/hairgel', echo_pool=True)

# WORKDIR = '/Users/zichen/Documents/Zichen_Projects/Rendl_RNAseq4/'
# os.chdir(WORKDIR)

# df = pd.read_csv('repRpkmMatrix_featureCounts_batch_1_3.csv')


# zone_celltypes = map(lambda x: x.split('$')[0], df.columns[1:])

# df_to_insert = pd.DataFrame({'gene': df['gene']})

# for zone_celltype in zone_celltypes:
# 	columns = df.columns[1:][np.in1d(zone_celltypes, [zone_celltype])]
# 	print columns
# 	avg = df[columns].mean(axis=1)
# 	sd = df[columns].std(axis=1)
# 	print avg.shape, sd.shape, sd.count()
# 	df_to_insert[zone_celltype + '_avg'] = avg
# 	df_to_insert[zone_celltype + '_sd'] = sd

# print df_to_insert.head()
# print df_to_insert.shape
# df_to_insert.to_sql('rpkms4', conn, chunksize=100,
# 	flavor='mysql', index_label='id', if_exists='replace')

# P20 DSP data
df = pd.read_csv('/Volumes/Untitled/Zichen_Projects/Rendl_RNAseq_P20_DSP/repFpkmMatrix_cufflinks.csv')\
	.set_index('gene_id')
print df.head()
print df.shape
df.columns = df.columns.map(int)

meta_df = pd.read_csv('/Volumes/Untitled/Zichen_Projects/Rendl_RNAseq_P20_DSP/meta_df.csv')
meta_df = meta_df.set_index(meta_df.columns[0])
print meta_df.head()

df_to_insert = pd.DataFrame({'gene': df.index.tolist()})

for cell_type in meta_df['cell_type'].unique():
	columns = meta_df.query('cell_type == "%s"' % cell_type).index.tolist()
	avg = df[columns].mean(axis=1)
	sd = df[columns].std(axis=1)
	
	df_to_insert[cell_type + '_avg'] = avg.values
	df_to_insert[cell_type + '_sd'] = sd.values

	print cell_type, columns

print df_to_insert.head()
print df_to_insert.shape
print df_to_insert.dtypes
print df_to_insert.count()

print df_to_insert.gene.map(len).max()

df_to_insert.to_sql('fpkms_p20_dsp', conn, 
	chunksize=100,
	index_label='id', if_exists='replace', 
	dtype={
	'id': INTEGER(),
	'gene': NVARCHAR(length=18)}
	)


