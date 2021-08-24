import matplotlib.pyplot as plt

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
subtypes = ['Vsubth','Vph','Vton','Vton_susps','Vton_brfps']
dclass.sum() # prints all columns

# multiple amps: 101 cells: 21jul18a
grpamp = dclass.groupby('amp')
arr = grpamp[subtypes].sum()
scalar = np.arange(0.2,1.2,0.2)
for col, s in zip(subtypes,scalar): dclass[col]=dclass[col]*s

fig = plt.figure()
arr.plot.bar(legend=True)
plt.ylabel('#of Cells')
plt.title('Counts')
plt.savefig('21aug18a_bar.png')
plt.show()


fig = plt.figure()
ax = fig.add_subplot()
for a,c in zip(set(df['amp']), ('g','r','m')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vsubth',marker='o',color=c,ax=ax)
for a,c in zip(set(df['amp']), ('g','r','m')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vph',marker='x',color=c,ax=ax)
for a,c in zip(set(df['amp']), ('g','r','m')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vton',marker='s',color=c,ax=ax)
for a,c in zip(set(df['amp']), ('g','r','m')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vton_brfps',marker='^',color=c,ax=ax)
for a,c in zip(set(df['amp']), ('g','r','m')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vton_susps',marker='*',color=c,ax=ax)
plt.ylim(0.1,1.1)
plt.yticks([0.1,1.1],"")
plt.ylabel('Subtypes')
plt.title('Classification')
plt.show()
plt.savefig('21aug18a_scatter.png')


# single amp: 115 cells: 21jul07A

dclass['Vsubth'] = dclass.Vlist.apply(lambda x: 1 if max(x)<0 else 0)
dclass['Vph'] = dfss.scnt.apply(lambda x: 1 if 0<x<=3 else 0)
dclass['Vton'] = df.spkt.apply(lambda x: 1 if len(x)>3 and stim['delay']<=x[-1]<=stimend+5 else 0)
dclass['Vton_susps'] = dclass.spkend.apply(lambda x: 1 if stimend+5<=x>=data[list(data)[0]]['simConfig']['duration']-50 else 0)
dclass['Vton_brfps'] = dclass.spkend.apply(lambda x: 1 if stimend+5<=x<=data[list(data)[0]]['simConfig']['duration']-50 else 0)


subtypes = ['Vsubth','Vph','Vton','Vton_susps','Vton_brfps']
arr = dclass[subtypes].sum()
dclass[subtypes].sum()


dclass.plot('cellnum','Vsubth',kind='scatter',s=s, c='y', label='Subthreshold',ax=ax)
dclass.plot('cellnum','Vph',kind='scatter',s=s,c='b', label='Phasic',ax=ax)
dclass.plot('cellnum','Vton',kind='scatter',s=s,c='r', label='Tonic',ax=ax)
dclass.plot('cellnum','Vton_susps',kind='scatter',s=s,c='k', label='Tonic with sus post-stim',ax=ax)
dclass.plot('cellnum','Vton_brfps',kind='scatter',s=s,c='c', label='Tonic with brief post-stim',ax=ax)
plt.savefig('21jul07A_scatter.png')


fig = plt.figure()
arr.plot.bar(legend=False)
plt.ylabel('#of Cells')
plt.title('No of Cells per Subtype')
plt.savefig('21jul07A_bar.png')
plt.show()





fig, ax = plt.subplots()
ax.clear()
for a,c in zip(set(df['amp']), ('g','r')): dclass.loc[df.amp==a].plot.scatter('cellnum', 'Vsubth', color=c, ax=ax)
plt.title('Subthreshold')
plt.savefig('ZZZ.png')
plt.show()
