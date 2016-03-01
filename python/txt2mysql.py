## convert repFPKM table to MySQL database
import os, sys
import MySQLdb
import numpy as np
import openpyxl as px
# sys.path.append('C:\Users\Zichen\Documents\\bitbucket\maayanlab_utils')
sys.path.append('/Users/zichen/Documents/bitbucket/maayanlab_utils')
from fileIO import read_df

# os.chdir('D:\Zichen_Projects\Rendl_RNAseq')
# os.chdir('/Users/zichen/Documents/Zichen_Projects/Rendl_RNAseq2')
# mat, gene_tids, samples = read_df('repFpkmMatrix_allGenes.txt')
# print mat.shape, len(gene_tids), len(samples)

os.chdir('/Users/zichen/Documents/Zichen_Projects/Rendl_RNAseq3')
mat, tids, samples = read_df('repFpkmMatrix_allGenes.txt')
d_tid_genes = {}
with open ('trackingIDs_geneSymbols.txt') as f:
	next(f)
	for line in f:
		sl = line.strip().split('\t')
		d_tid_genes[sl[0]] = sl[1].split(',')

# d_sig = {}
# with open ('signatures.txt') as f:
# 	signatures = next(f).split('\t')
# 	for line in f:
# 		sl = line.split('\t')
# 		for gene, sig in zip(sl, signatures):
# 			if gene != '' and gene.strip() != '':
# 				d_sig[gene.strip()] = sig.strip()

# from pprint import pprint
# pprint(d_sig)

conn = MySQLdb.connect(host='localhost',user='root', passwd='',db='hairgel')
cur = conn.cursor()


# ii = 0
# for row, gene_tid in zip(mat, gene_tids):
# 	genes = gene_tid.split('|')[0].split(',')
# 	for gene in genes:
# 		ii += 1
# 		try:
# 			values = [ii, gene]
# 			for i in np.arange(0,16,2):
# 				values.append( row[i:i+2].mean() )
# 				values.append( row[i:i+2].std() )
# 			# print len(values)
# 			sql = "INSERT INTO fpkms VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%tuple(values)
# 			# print sql
# 			cur.execute(sql)
# 			conn.commit()
# 		except Exception, e:
# 			print e
# 			conn.rollback()

# for gene, sig in d_sig.items():
# 	try:
# 		sql = "INSERT INTO signature VALUES ('%s', '%s')" % (gene, sig)
# 		cur.execute(sql)
# 		conn.commit()
# 	except Exception, e:
# 		print e
# 		conn.rollback()

## insert Amelie data
# mat, genes, samples = read_df('repFpkmMatrix_all_gene_symbols.txt')
# samples = np.array(samples)
# print mat.shape, len(genes), len(samples)

# # sort columns
# samples_numbers = np.array([int(s.split('_')[0][1:]) for s in samples])
# srt_idx = samples_numbers.argsort()
# samples = samples[srt_idx]
# mat = mat[:, srt_idx]

# print samples
# ii = 0
# for row,g in zip(mat, genes):
# 	for gene in g.split(','):
# 		ii += 1
# 		try:
# 			values = [ii, gene]
# 			for i in np.arange(0,40,2):
# 				values.append( row[i:i+2].mean() )
# 				values.append( row[i:i+2].std() )
# 			# print len(values)
# 			sql = "INSERT INTO fpkms2 VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%tuple(values)
# 			# print sql
# 			cur.execute(sql)
# 			conn.commit()
# 		except Exception, e:
# 			print e
# 			conn.rollback()

## insert Amelie signatures
# W = px.load_workbook('SignatureGenes_AR.xlsx', use_iterators = True)
# sheet_names = W.get_sheet_names()
# sigs = []
# for sheet_name in sheet_names:
# 	sheet = W.get_sheet_by_name(name = sheet_name)
# 	i = 1
# 	while True:
# 		try:
# 			genes = str(sheet['A%s'%i].value)
# 			for gene in genes.split(','):
# 				sigs.append( (gene, sheet_name) )
# 			i += 1
# 		except IndexError:
# 			break
# 	print i, sheet_name

# print 'number of gene-cell pairs:', len(sigs)

# for (gene, cell) in sigs:
# 	try:
# 		sql = "INSERT INTO signature2 VALUES ('%s', '%s')" % (gene, cell)
# 		cur.execute(sql)
# 		conn.commit()
# 	except Exception, e:
# 		print e
# 		conn.rollback()

## insert Rachel's DS, DP, DF data
ii = 0
for row, tid in zip(mat, tids):
	genes = d_tid_genes[tid]
	for gene in genes:
		ii += 1
		try:
			values = [ii, gene]
			for i in np.arange(0,6,2):
				values.append( row[i:i+2].mean() )
				values.append( row[i:i+2].std() )
			# print len(values)
			sql = "INSERT INTO fpkms3 VALUES (%s,'%s',%s,%s,%s,%s,%s,%s)"%tuple(values)
			# print sql
			cur.execute(sql)
			conn.commit()
		except Exception, e:
			print e
			conn.rollback()

conn.close()
