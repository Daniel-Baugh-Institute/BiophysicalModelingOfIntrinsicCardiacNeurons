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
plt.rcParams.update({'font.size': font})
name = 'tdata_all_15'
wr = 20 # width of reduced heatmap
wf = 20 # width of full heatmap

df = pd.read_csv(f"{name}.csv")

def plotHeatmap(dfr,gene,phy,l,w,x1,xe,y,t1,t2,cs):
	f = plt.figure(figsize=(w,7))
	# sns.set(font_scale = 1.8)
	ax = sns.heatmap(dfr.transpose(),linewidth = 0.4,xticklabels=False,yticklabels = gene,cmap=cs,cbar=False)
	ax.set_ylabel('Genomic Identity',fontsize=font)
	ax2 = ax.twinx()
	ax2.yaxis.set_ticks_position('right')
	ax2 = sns.heatmap(dfr.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = phy,cmap=cs,cbar=False)
	ax2.set_ylabel('Physiological Identity',fontsize=font)
	ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize = font)
	plt.text(x1,y,t1, fontdict={'size':font})
	plt.text(xe,y,t2, fontdict={'size':font})
	# plt.savefig(f"{name}_{l}_heatmap.png",dpi=300,bbox_inches='tight')
	plt.show()
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
tx1 = -38
txe = 318
ty = 15.8
txt1 = 'Single Neurone: #1'
txt2 = '#321'
cs = 'copper_r'
phys = ["HCN3","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN1","HCN4","Cav 1.2 (L)","Cav 2.2 (N)","Kv 1.1 ($\u03B1$ unit)","Kir 3.1","HCN2","Cav 3.3 (T)","Kv 3.1","Kv 1.1 ($\u03B21$ unit)","Nav 1.1"]
plotHeatmap(dfm2l,gfull,phys,'full',wf,tx1, txe, ty,txt1,txt2,cs)

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

tx1 = -12# -15
txe = 103
ty = 14.8
txt1 = 'Neuronal-Type ID: T1'
txt2 = 'T104'
cs = 'binary'
phys =["HCN3","HCN1","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN4","Cav 1.2 (L)","Cav 3.3 (T)","Kv 1.1","Kir 3.1","Cav 2.2 (N)","HCN2","Kv 3.1","Nav 1.1"]

plotHeatmap(dfrm2l,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs)


z = dfrm2l.transpose()
z.insert(0,"Gene",gred)
z = z.reset_index()
del z['index']
df104 = z.set_index('Gene')
g104 = gred

def orgHeatmap(d,g):
	d = d.drop(d['Gene'].tolist().index("Kcnab1"))
	# sort yaxis: maximally expressed genes at the bottom
	d['sum'] = d.sum(axis=1,numeric_only=True)
	dfasc = d.sort_values(by=['sum'],ascending=[True])
	dfasc = dfasc.reset_index()
	del dfasc['index']
	del d['sum']
	gfull = dfasc['Gene']
	# org xaxis: cells with most to least common genes
	dfm2l = dfasc.drop(['Gene','sum'],axis=1).transpose()
	dfm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfm2l.values]
	dfm2l = dfm2l.sort_values(by=['bitsum'],ascending=[False])
	del dfm2l['bitsum']

	z = dfm2l.transpose()
	z.insert(0,"Gene",gfull)
	z = z.reset_index()
	del z['index']
	y = z.set_index('Gene')
	x = y.reindex(index = g)
	return x

def freqBar(z,a,s):
	p = []
	for i in range(len(z.index)):
		cnt = 0
		for j in range(len(a.index)):
			if np.array_equal(z.values[i],a.values[j]):
				cnt+=1
		p.append(cnt)
	print (f"{s}:\n \t Total No. {sum(p)}\n \t Highest repetitions = {sorted(p)[-1]} @ Cell no. {p.index(sorted(p)[-1])+1}\n \t 2nd Highest repetitions = {sorted(p)[-2]} @ Cell no. {p.index(sorted(p)[-2])+1}\n")
	# import IPython; IPython.embed()
	return p

dovr = pd.DataFrame()
draw = orgHeatmap(df, g104)
dovr['Overall'] = freqBar(df104.transpose(),draw.transpose(),'')
# import IPython; IPython.embed()
print(f"No. of cells wrt frequency \n {dovr.value_counts()}")
print(f"Summary statistics \n {dovr.describe()}")

fnt = 25
plt.rcParams['font.size']=fnt
f,axs = plt.subplots(2,1, figsize=(25,15))
sns.set(font_scale = 1.8)
sns.heatmap(dfrm2l.transpose(),linewidth = 0.4,xticklabels=False,yticklabels = gr,cmap=cs,cbar=False, ax=axs[0])
axs[0].set_ylabel('Genomic Identity',fontsize=fnt)
axs[0].set_yticklabels(axs[0].get_ymajorticklabels(), fontsize = fnt)
ax2 = axs[0].twinx()
ax2.yaxis.set_ticks_position('right')
ax2 = sns.heatmap(dfrm2l.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = phys,cmap=cs,cbar=False)
ax2.set_ylabel('Physiological Identity',fontsize=fnt)
ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize = fnt)
plt.text(tx1,ty,txt1, fontdict={'size':fnt})
plt.text(txe,ty,txt2, fontdict={'size':fnt})
sns.barplot(x = dovr.index+1, y = dovr['Overall'],color='mediumseagreen', ax=axs[1])
axs[1].set_xticks(np.arange(1, 104, step=5))
axs[1].set_xlabel('Neuronal-Type ID (T#)',fontsize=fnt)
axs[1].set_ylabel('Number of Occurences',fontsize=fnt)
plt.tight_layout()
plt.savefig("tdata_red_freq.png",dpi=300,bbox_inches='tight')
plt.show()
