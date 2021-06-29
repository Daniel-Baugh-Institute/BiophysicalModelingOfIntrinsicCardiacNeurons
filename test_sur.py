def RinStats(df=df):
	dfrin=df[['cellnum', 't','V_soma']].copy()
	vmin = {}
	rmp = {}
	vss = {}
	r_vmin = {}
	r_vss = {}
	minpos = 0
	sspos = 0
	for c in dfrin.cellnum:
		vmin[c] = min(dfrin.V_soma[c]['cell_0'])
		stimamp = data[list(data.keys())[c]]['net']['cells'][0]['stims'][0]['amp']
			for i in dfrin.t.values[c]:
				if i<data[list(data.keys())[c]]['net']['cells'][0]['stims'][0]['delay']:
					minpos+=1
				if i<data[list(data.keys())[c]]['net']['cells'][0]['stims'][0]['dur']:
					sspos+=1
				rmp[c] = dfrin.V_soma[c]['cell_0'][minpos]
				vss[c] = dfrin.V_soma[c]['cell_0'][sspos]
				r_vmin[c] = (vmin[c]-rmp[c])/stimamp
				r_vss[c] = (vss[c]-rmp[c])/stimamp

fig, axs = plt.subplots(2,1)
axs[0].scatter(list(r_vmin),list(r_vmin.values()))
axs[0].set_title('Rm (in MOhm corr. to neg. peak')
axs[1].scatter(list(r_vss),list(r_vss.values()))
axs[1].set_title('Rm (in MOhm corr. to ss after sag')
