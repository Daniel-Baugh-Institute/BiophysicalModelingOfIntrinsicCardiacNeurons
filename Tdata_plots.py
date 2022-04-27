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

font = 17

name = 'tdata_all_15'
cs = 'binary'
wr = 15 # width of reduced heatmap
wf = 15 # width of full heatmap

df = pd.read_csv(f"{name}.csv")

def plotHeatmap(dfr,gene,phy,l,w,x1,xe,y,t1,t2,ttle):
	f = plt.figure(figsize=(w,8))
	sns.set(font_scale = 1.8)
	ax = sns.heatmap(dfr.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = gene,cmap=cs,cbar=False)
	ax2 = ax.twinx()
	ax2.yaxis.set_ticks_position('right')
	ax2 = sns.heatmap(dfr.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = phy,cmap=cs,cbar=False)
	ax2.set_ylabel('Physiological Name',fontsize=font)
	ax2.set(title=ttle)
	ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize = font)
	plt.text(x1,y,t1, fontdict={'size':font})
	plt.text(xe,y,t2, fontdict={'size':font})
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
tx1 = -48
txe = 318
ty = 15.8
txt1 = 'Single Neuron: #1'
txt2 = '#321'
title = 'Discretized Expression Data'
phys = ["HCN3","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN1","HCN4","Cav 1.2 (L)","Cav 2.2 (N)","Kv 1.1 ($\u03B1$ unit)","Kir 3.1","HCN2","Cav 3.3 (T)","Kv 3.1","Kv 1.1 ($\u03B21$ unit)","Nav 1.1"]
# plotHeatmap(dfm2l,gfull,phys,'full',wf,tx1, txe, ty,txt1,txt2,title)

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
gr = gred.tolist()
gr[gr.index('Kcna1')]=gr[gr.index('Kcna1')]+'+ab1'

# sort xaxis: most to least common genes
dfrm2l = dfred.drop(['Gene','sum'],axis=1).transpose()
dfrm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfrm2l.values]
dfrm2l = dfrm2l.sort_values(by=['bitsum'],ascending=[False])
del dfrm2l['bitsum']

tx1 = -15
txe = 103
ty = 14.8
txt1 = 'Neuron ID: #N000'
txt2 = 'N103'
title = 'Unique Neuronal States'
phys =["HCN3","HCN1","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN4","Cav 1.2 (L)","Cav 3.3 (T)","Kv 1.1","Kir 3.1","Cav 2.2 (N)","HCN2","Kv 3.1","Nav 1.1"]

# plotHeatmap(dfrm2l,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,title)

# save .csv for netParams
# dfrm2l.transpose().to_csv(f"red_{name}_m2l.csv", header=False, index=False)
# dfm2l.transpose().to_csv(f"{name}_m2l.csv", header=False, index=False)
