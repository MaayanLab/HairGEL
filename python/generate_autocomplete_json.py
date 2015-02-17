import os, sys, json
sys.path.append('C:\Users\Zichen\Documents\\bitbucket\maayanlab_utils')
from fileIO import file2list

os.chdir('D:\Zichen_Projects\Rendl_RNAseq')
gene_tids = file2list('repFpkmMatrix_allGenes.txt', 0)

gene_names = []
for gene_tid in gene_tids:
	if ',' in gene_tid:
		gene_names.extend(gene_tid.split('|')[0].split(','))
	else:
		gene_names.append(gene_tid.split('|')[0])

os.chdir('C:\\xampp\htdocs\hairgel')
json.dump(gene_names, open('geneNames.json','w'))
