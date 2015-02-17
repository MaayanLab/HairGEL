## convert repFPKM table to MySQL database
import os, sys
import MySQLdb
import numpy as np
sys.path.append('C:\Users\Zichen\Documents\\bitbucket\maayanlab_utils')
from fileIO import read_df

os.chdir('D:\Zichen_Projects\Rendl_RNAseq')

mat, gene_tids, samples = read_df('repFpkmMatrix_allGenes.txt')
print mat.shape, len(gene_tids), len(samples)

d_sig = {}
with open ('signatures.txt') as f:
	signatures = next(f).split('\t')
	for line in f:
		sl = line.split('\t')
		for gene, sig in zip(sl, signatures):
			if gene != '' and gene.strip() != '':
				d_sig[gene.strip()] = sig.strip()

# from pprint import pprint
# pprint(d_sig)

conn = MySQLdb.connect(host='localhost',user='root', passwd='',db='hairgel')
cur = conn.cursor()


ii = 0
for row, gene_tid in zip(mat, gene_tids):
	genes = gene_tid.split('|')[0].split(',')
	for gene in genes:
		ii += 1
		try:
			values = [ii, gene]
			for i in np.arange(0,16,2):
				values.append( row[i:i+2].mean() )
				values.append( row[i:i+2].std() )
			# print len(values)
			sql = "INSERT INTO fpkms VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%tuple(values)
			# print sql
			cur.execute(sql)
			conn.commit()
		except Exception, e:
			print e
			conn.rollback()

# for gene, sig in d_sig.items():
# 	try:
# 		sql = "INSERT INTO signature VALUES ('%s', '%s')" % (gene, sig)
# 		cur.execute(sql)
# 		conn.commit()
# 	except Exception, e:
# 		print e
# 		conn.rollback()


conn.close()