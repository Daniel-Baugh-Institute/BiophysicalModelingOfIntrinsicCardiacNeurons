import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import plotly_express as px
import math as m
import plotly.io as pio
import seaborn as sns

font = 16

name = 'tdata_all_15'
cs = 'binary'

df = pd.read_csv(f"{name}.csv")

def plotHeatmap(dfr,gene,l):
	f = plt.figure()
	ax = sns.heatmap(dfr.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = gene,cmap=cs,cbar=False)
	plt.savefig(f"{name}_{l}_heatmap.png",dpi=300,bbox_inches='tight')
	# f.show()
	return

# org yaxis: most # to least # of genes
df['sum'] = df.sum(axis=1,numeric_only=True)
dfasc = df.sort_values(by=['sum'],ascending=[True])
dfasc = dfasc.reset_index()
del dfasc['index']
del df['sum']
gfull = dfasc['Gene']

# org xaxis: cells with most to least common genes
dfm2l = dfasc.drop(['Gene','sum'],axis=1).transpose()
dfm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfm2l.values]
dfm2l = dfm2l.sort_values(by=['bitsum'],ascending=[False])
del dfm2l['bitsum']

plotHeatmap(dfm2l,gfull,'full')

# max # of genes is different in 321 cells vs in 104 cells

# dropping Kcnab1 from red. binary map
dfwob = df.drop(df['Gene'].tolist().index("Kcnab1"))
gwob = dfwob['Gene']
dfred = dfwob.drop('Gene',axis=1).transpose().drop_duplicates(keep='first').transpose()

# sort yaxis: maximally expressed genes at the bottom
dfred.insert(0,"Gene",gwob)
dfred['sum'] = dfred.sum(axis=1,numeric_only=True)
dfred = dfred.sort_values(by=['sum'],ascending=[True])
gred = dfred['Gene']

# sort xaxis: most to least common genes
dfrm2l = dfred.drop(['Gene','sum'],axis=1).transpose()
dfrm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfrm2l.values]
dfrm2l = dfrm2l.sort_values(by=['bitsum'],ascending=[False])
del dfrm2l['bitsum']


plotHeatmap(dfrm2l,gred,'red')

# save .csv for netParams
# dfrm2l.transpose().to_csv(f"red_{name}_m2l.csv", header=False, index=False)
