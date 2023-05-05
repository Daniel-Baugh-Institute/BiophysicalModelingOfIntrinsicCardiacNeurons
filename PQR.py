import json
import pickle
import pandas as pd
import numpy as np
import os,sys
from os import makedirs
import re
from collections import OrderedDict
from itertools import product
import plotly.graph_objects as go
import plotly_express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import scipy.optimize as opt
from plotly.subplots import make_subplots
import seaborn as sns

df = pd.read_csv('para.csv')

font = 17
plt.rcParams.update({'font.size': font})
df.plot(x = 'Name',kind = 'bar',stacked = False, figsize=(12,10))
plt.legend(bbox_to_anchor=(1, 0.9), loc=2)
plt.xlabel("Ion Channel Genes")
plt.ylabel("Relative Comparison of Ion Channel Conductance (%)")
plt.savefig("PQR_cond.png",dpi=300,bbox_inches='tight')
# plt.show()


font = 17
sze = 125
plt.rcParams.update({'font.size': font})

d = pd.read_csv('rin.csv')
# import IPython; IPython.embed()
ax = d.plot(kind="scatter", x="Cellnum",y="Model P", label="Model P",color='C0',s=sze,marker='o',edgecolor='black',figsize=(12,10))
d.plot(kind="scatter", x="Cellnum",y="Model Q", color= 'C1',s=sze,label="Model Q", marker='s',edgecolor='black',ax=ax)
d.plot( kind="scatter", x="Cellnum",y="Model R", color= 'C2',s=sze,label="Model R", marker='^',edgecolor='black',ax=ax)
ax.set_xticks(np.arange(1, 104, step = 10))
ax.set_xlabel("Neuronal-Type ID (T#)")
ax.set_ylabel(r'Input Impedance (M$\Omega$)')
plt.savefig("PQR_rin.png",dpi=300,bbox_inches='tight')
# plt.show()



########################
# Epas comparison

stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
if (stim['amp'] and stim['dur'] and stim['delay']==0):
    raise Exception("Epas cannot be computed in the presence of an ongoing stimulus")
elif (stim['amp'] and stim['dur'] and stim['delay']<=data[list(data)[0]]['simConfig']['duration']):
    for i in df['t'][0]:
        if i<stim['delay']:
            indx=df['t'][0].index(i)
else:
    indx = -1
# import IPython; IPython.embed()
print(indx)
cells = df['cellnum'].tolist()
vm = {}
pasv = {}

dfep = df[['cellnum','V_soma','epas']].copy()
dfep['vm']=dfep.V_soma.apply(lambda x:x['cell_0'][indx])
dfep['pasv']=dfep.epas.apply(lambda x:x['cell_0'][indx])

dfep[['cellnum','vm','pasv']].to_csv('epasQ.csv')


font = 17
sze = 100
plt.rcParams.update({'font.size': font})

d = pd.read_csv('PQRepas.csv')
# import IPython; IPython.embed()
ax = d.plot(kind="scatter", x="cellnum",y="Model P", label="Model P",color='C0',s=sze,marker='o',edgecolor='black',figsize=(12,10))
d.plot(kind="scatter", x="cellnum",y="Model Q", color= 'C1',s=sze,label="Model Q", marker='s',edgecolor='black',ax=ax)
d.plot( kind="scatter", x="cellnum",y="Model R", color= 'C2',s=sze,label="Model R", marker='^',edgecolor='black',ax=ax)
d.plot( kind="line", x="cellnum",y="vm", color= 'black',label="RMP",linestyle = 'dashed',linewidth = '2',ax=ax)
ax.set_xticks(np.arange(1, 104, step = 10))
ax.set_xlabel("Neuronal-Type ID (T#)")
ax.set_ylabel(r'Reversal Potential of Passive Leak Channels ($E_{pas}$) (mV)')
plt.savefig("PQR_epas.png",dpi=300,bbox_inches='tight')
plt.show()


#######################
# Rheobase
stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
stimend = stim['dur'] + stim['delay']
dr=df[['amp','cellnum']].copy()
dr['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
dr['Subth'] = dr.Vlist.apply(lambda x: 1 if max(x)<-20 else 0) #0=> AP, 1=> subthreshold response
del dr['Vlist']

c = []
r = []
    for k in params[1]['values']:
        print(k)
        d = dr.loc[dr['cellnum']==k]
        c.append(k)
        if (0 in d['Subth'].values.tolist()):
            r.append(d['amp'].values[d['Subth'].values.tolist().index(0)])
        else:
            r.append(-0.1)
        del d
print(len(c))
print(len(r))
drh = pd.DataFrame()
drh['cellnum']=c
drh['rheo']=r
del c,r

print(drh.groupby('rheo').count())

drh[['cellnum','rheo']].to_csv('rheoR.csv')


font = 19
sze = 12
plt.rcParams.update({'font.size': font})

d = pd.read_csv('PQRrheo.csv')


plt.figure(figsize=(14,12))
o = 'v'
ax = sns.stripplot(y=d['cellnum'],x=d['Model P'],color='C0',orient = o,size=sze,marker='o', edgecolor='black',linewidth=1, native_scale = False,jitter=True)
sns.stripplot(y=d['cellnum'],x=d['Model Q'],color='C1',orient = o,size=sze,marker='s',edgecolor='black', linewidth=1, native_scale = False, jitter=True,ax=ax)
sns.stripplot(y=d['cellnum'],x=d['Model R'],color='C2',orient = o,size=sze,marker='^',edgecolor='black', linewidth=1,native_scale = False, jitter=True,ax=ax)
ax.set_yticks(np.arange(1, 104, step = 10))
ax.set_ylabel("Neuronal-Type ID (T#)")
ax.set_xlabel('Rheobase (nA)')
plt.savefig("PQR_rheo.png",dpi=300,bbox_inches='tight')
plt.show()
del dr, drh, d
