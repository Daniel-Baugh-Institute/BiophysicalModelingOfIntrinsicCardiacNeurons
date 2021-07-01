def RinStats(df=df):
	dfrin=df[['amp','cellnum']].copy()
	dfrin['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
 	dfrin['Vmin'] = dfrin.Vlist.apply(min)
 	# dfrin['indxss']=df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<800)))
 	dfrin['indxss']=df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<data[list(data.keys())[c]]['net']['cells'][0]['stims'][0]['dur'])))
 	isslist = dfrin.indxss.tolist() 
	dfrin['vss']= dfrin.Vlist.apply(lambda x: x[i] for in isslist) #generator obj not callable
 	#LATER
 	# dfrin['indxrmp']=df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<50)))
 	dfrin['indxrmp']=df.t.apply(lambda x:len(np.flatnonzero(np.array(x)<data[list(data.keys())[c]]['net']['cells'][0]['stims'][0]['delay'])))


# fig, axs = plt.subplots(2,1)
# axs[0].scatter(list(r_vmin),list(r_vmin.values()))
# axs[0].set_title('Rm (in MOhm corr. to neg. peak')
# axs[1].scatter(list(r_vss),list(r_vss.values()))
# axs[1].set_title('Rm (in MOhm corr. to ss after sag')
