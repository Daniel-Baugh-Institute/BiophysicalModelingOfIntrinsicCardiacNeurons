def RinStats(df=df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    dfrin=df[['amp','cellnum']].copy()
    dfrin['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dfrin['Vrmp'] = dfrin.Vlist.apply(lambda x: x[0])
    dfrin['Vmin'] = dfrin.Vlist.apply(min)
    dfrin['indxss'] = df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<stimend)))
    return dfrin

# fig, axs = plt.subplots(2,1)
# axs[0].scatter(list(r_vmin),list(r_vmin.values()))
# axs[0].set_title('Rm (in MOhm corr. to neg. peak')
# axs[1].scatter(list(r_vss),list(r_vss.values()))
# axs[1].set_title('Rm (in MOhm corr. to ss after sag')
