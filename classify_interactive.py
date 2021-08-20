stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
stimend = stim['dur'] + stim['delay']
dclass=df[['amp','cellnum']].copy()
dclass['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
dclass['Vrmp'] = dclass.Vlist.apply(lambda x: x[0])
dclass['spkend'] = df.spkt.apply(lambda x: x[len(x)-1] if len(x)>0 else -1)
dfss=df[['amp', 'cellnum', 'avgRate']].copy() 
dfss['scnt'] = df.spkt.apply(len)

dclass['Vsubth'] = dclass.Vlist.apply(lambda x: 1 if max(x)<0 else 0)
dclass['Vph'] = dfss.scnt.apply(lambda x: 1 if 0<x<=3 else 0)
dclass['Vton'] = df.spkt.apply(lambda x: 1 if len(x)>3 and stim['delay']<=x[-1]<=stimend+5 else 0)
dclass['Vton_susps'] = dclass.spkend.apply(lambda x: 1 if stimend+5<=x>=data[list(data)[0]]['simConfig']['duration']-50 else 0)
dclass['Vton_brfps'] = dclass.spkend.apply(lambda x: 1 if stimend+5<=x<=data[list(data)[0]]['simConfig']['duration']-50 else 0)

dclass.sum() # prints all columns
dtypes = ['Vsubth','Vph','Vton','Vton_susps','Vton_brfps']
arr = dclass[dtypes].sum()

import matplotlib.pyplot as plt
arr.plot.bar(legend=False)
plt.savefig('ZZZ.png')
plt.show()


dclass[dtypes].sum()





fig, ax = plt.subplots()
ax.clear()
for a,c in zip(set(df['amp']), ('g','r')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vsubth', color=c, ax=ax)
plt.title('Subthreshold')
plt.savefig('ZZZ.png')
plt.show()
