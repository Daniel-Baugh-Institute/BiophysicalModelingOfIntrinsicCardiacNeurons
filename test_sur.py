# Run spkStats() first
def classifyAP(df=df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    db=df[['amp','cellnum']].copy()
    db['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    db['Vrmp'] = db.Vlist.apply(lambda x: x[0])

    # db
    db['ind1'] = df.t.apply(lambda x:len(np.flatnonzero((stimend-10)<np.array(x))))
    db['ind2'] = df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<stimend)))
    db['Vend'] = db.apply(lambda row: row['Vlist'][row['ind1']:row['ind2']], axis =1)
    db['Vdb'] = db.apply(lambda row: ? if row['Vend'].max()-row['Vend'].min()<1 and row['Vend'].min()-row['Vrmp'][0]<30 else -1)

    # subthreshold -  No Na
    db['Vsubth'] = df.V_soma.apply(lambda x: ? if max(x)<0 else -1)

    # phasic - 1 AP
    db['Vph'] = dfss.scnt.apply(lambda x: ? if x<=3 else -1)

    # get time of last spike - tlast
    # tonic - w/o sp
    db['Vton'] #if tlast is within delay and stimend

    # tonic - w/ sustained sp
    db['Vton_infsp'] # if tlast ~ cfg.duration

    # tonic - w/o sustained sp
    db['Vton_finsp'] # if tlast<cfg.duration-50

    return


# def idDepnBlock(df=df):
#     dblk['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
#     dblk['Vend'] = dblk.apply(lambda row: row['Vlist'][4000:6000], axis =1)
#     dblk['Vdiff'] = dblk.Vend.apply(lambda x: max(x)-min(x) if min(x)+61>30 else -1)
#     return

# #Using df graphics
# dfss.loc[df.amp==0.6].plot.scatter('cellnum', 'Vdiff')
# plt.show()

# fig, ax = plt.subplots()
# ax.clear()
# for a,c in zip(set(df['amp']), ('b','g','r')): df.loc[df.amp==a].plot.scatter('cellnum', 'sdur', color=c, ax=ax)
# ax.set_ylim(400,500)


import matplotlib.pyplot as plt
fig = plt.plot(dfss.Vdiff, '.')
plt.show()



def RinStats(df=df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    dfrin=df[['amp','cellnum']].copy()
    dfrin['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dfrin['Vrmp'] = dfrin.Vlist.apply(lambda x: x[0])
    dfrin['Vmin'] = dfrin.Vlist.apply(min)
    dfrin['indxss'] = df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<stimend)))
    dfrin['Vss'] = dfrin.apply(lambda row: row['Vlist'][row['indxss']], axis =1)
    dfrin['Rin_ss'] = dfrin.Vss.sub(dfrin.Vrmp).div(df.amp)
    dfrin['Rin_min'] = dfrin.Vmin.sub(dfrin.Vrmp).div(df.amp)
    return dfrin

import matplotlib.pyplot as plt
fig, axs = plt.subplots(2,1)
axs[0].scatter(dfrin.cellnum, dfrin.Rin_min)
axs[0].set_title('Rm (in MOhm corr. to neg. peak')
axs[1].scatter(dfrin.cellnum, dfrin.Rin_ss)
axs[1].set_title('Rm (in MOhm corr. to ss after sag')
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import statistics
# import math
# def idDepnBlock(df=df):
#     stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
#     stimend = stim['dur'] + stim['delay']
#     dblk=df[['amp','cellnum']].copy()
#     dblk['ind1'] = df.t.apply(lambda x:len(np.flatnonzero((stimend-10)<np.array(x))))
#     dblk['ind2'] = df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<stimend)))
#     dblk['Vsubset'] = dblk.apply(lambda row: row['Vlist'][row['ind1']:row['ind2']], axis =1)
#     dblk['Vsubset_mn'] = dblk.Vsubset.apply(min)
#     dblk['Vsubset_mx']= dblk.Vsubset.apply(max)
#     dblk['Vsubset_avg']=dblk.Vsubset.apply(lambda x: statistics.mean(x))
#     #testing math.trunc() function to check for depn block
#     return dblk




