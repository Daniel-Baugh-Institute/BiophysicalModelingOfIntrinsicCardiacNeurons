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
