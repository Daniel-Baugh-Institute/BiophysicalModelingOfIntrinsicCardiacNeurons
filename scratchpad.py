import plotly.graph_objects as go
import plotly_express as px
import matplotlib.pyplot as plt
#import random

dfss=df[['amp', 'cellnum', 'avgRate']].copy()  # note double brackets
dfss.scnt    = df.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
dfss['scnt'] = df.spkt.apply(len)
dfss['spk1'] = df.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
dfss['f1']   = df.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
dfss['f2']   = df.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
dfss['sdur'] = df.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
dfss['hz']   = dfss.scnt.div(dfss.sdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN


############################# import IPython; IPython.embed()

fig = px.line(dfss, x='amp', y='hz', color = 'cellnum', hover_data=['cellnum','hz','amp'], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'f-I curve', markers = True, error_y="stdhz", error_y_minus="stdhz")
fig.show()

fig.write_image("/Users/suranjanagupta/Pory/SPARC_Simulations/ProjectWork/Q3Q4/github_ragp/activeRAGP/ragp/allData/21dec15b/class_tally.png")

b = px.box(dfss, x='amp',y='hz',labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'},title = 'f-I curve')
fig = px.line(dfss, x='amp', y='hz', color = 'cellnum', hover_data=['cellnum','hz','amp'], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'f-I curve')
fig.update_traces(patch={"line": {"dash": 'dot'}})
fig.add_trace(b.data[0])
fig.show()

figg = px.scatter_3d(dfss, x='cellnum', y='amp', z='hz',color='hz',labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'})

fig = px.bar(arr,text = 'value',labels={'amp':'Current Stimulus (nA)','value':'No. of Simulations','variable':'Classification Subtypes'})
newnames = {'Vsubth':'Subthreshold','Vph':'Phasic','Vton':'Tonic','Vton_susps': 'Tonic with Sustained Post-stim', 'Vton_brfps': 'Tonic with Brief Post-stim'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],legendgroup = newnames[t.name],hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
fig.update_traces(texttemplate='%{text:3.2f}', textposition='inside')
fig.show()

fig = px.line(dfss, x=df["ka"], y='hz', color = 'amp', hover_data=['cellnum','hz','amp'], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'f-I curve', markers = True, error_y=None, error_y_minus=None)

# ff vs KA

dfss['hz_0'] = dfss['hz'].replace({0:np.nan})

fig = px.line(dfss, x=df["ka"], y='hz_0',color = df["amp"].astype(str),labels={'cellnum':'Cell Number','hz_0':'Firing Frequency (Hz)', 'color':'Current Clamp (nA)','x':'Ka Conductance (S/cm2)'}, markers=True)
fig.show()

figg = px.scatter_3d(dfss, x='cellnum', y='amp', z=df["ka"],color='hz',labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)','z':'Ka Conductance (S/cm2)'})


#################################################

fig = px.scatter(dfss, x='amp', y='hz', color = df["ka"].astype(str), size = 'amp', hover_data=['cellnum','hz','amp'], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)','color':'Ka Conductance (S/cm2)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()

fig.write_image("/Users/suranjanagupta/Pory/SPARC_Simulations/ProjectWork/Q3Q4/github_ragp/activeRAGP/ragp/allData/21dec06a/ka.png")

fig = px.scatter(dfss, x='cellnum', y='hz', color = df["ka"].astype(str), size = 'amp', hover_data=['cellnum','hz','amp'], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)','color':'Ka Conductance (S/cm2)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()

fig.write_image("/Users/suranjanagupta/Pory/SPARC_Simulations/ProjectWork/Q3Q4/github_ragp/activeRAGP/ragp/allData/21dec06a/fig2.png")


figg = px.scatter_3d(dfss, x='cellnum', y='amp', z='hz',color='hz', hover_data=['cellnum','hz','amp',df.ka,df.na, df.kcnc, df.kcnab, df.h1, df.h2, df.h3, df.h4, df.c1a, df.c1b, df.c1c, df.c1g, df.c1i],labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)','hover_data_3':'Ka Conductance (S/cm2)', 'hover_data_4':'Na Conductance (S/cm2)', 'hover_data_5':'Kcnc Conductance (S/cm2)', 'hover_data_6':'Kcnab Conductance (S/cm2)', 'hover_data_7':'HCN1 Conductance (S/cm2)', 'hover_data_8':'HCN2 Conductance (S/cm2)', 'hover_data_9':'HCN3 Conductance (S/cm2)', 'hover_data_10':'HCN4 Conductance (S/cm2)', 'hover_data_11':'Cacna1a Conductance (S/cm2)', 'hover_data_12':'Cacna1b Conductance (S/cm2)', 'hover_data_13':'Cacna1c Conductance (S/cm2)', 'hover_data_14':'Cacna1g Conductance (S/cm2)', 'hover_data_15':'Cacna1i Conductance (S/cm2)'})

figg.write_image("/Users/suranjanagupta/Pory/SPARC_Simulations/ProjectWork/Q3Q4/github_ragp/activeRAGP/ragp/allData/21dec06a/3d.png")

##################################################

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

grpamp = dclass.groupby('amp')
arr = grpamp[subtypes].sum()

fig = plt.figure()
arr.plot.bar(legend=True)
plt.ylabel('Number of Simulations')
plt.xlabel('Current Stimulus (nA)')
plt.show()
plt.savefig('/Users/suranjanagupta/Pory/SPARC_Simulations/ProjectWork/Q3Q4/github_ragp/activeRAGP/ragp/allData/21nov30b/fig4.png')

#
df57 =  df.loc[df['cellnum']==57]



fig = px.scatter(dfss, x='cellnum', y='hz',color='amp', size = 'hz', hover_data=['cellnum','hz','amp', df.ka], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()

fig = px.scatter(dfss, x='cellnum', y='hz', color = df["amp"].astype(str),size = 'hz', hover_data=['cellnum','hz','amp', df.ka], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()

fig = px.scatter(dfss, x='amp', y='hz', color = df["ka"].astype(str), size = 'amp', hover_data=['cellnum','hz','amp', df.ka], labels={'cellnum':'Cell Number','hz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()

fig = px.scatter(dfss, x='cellnum', y='sdur', color = df["amp"].astype(str), size = 'amp', hover_data=['cellnum','hz','amp', df.ka], labels={'cellnum':'Cell Number','sdur':'Duration of Spiking (ms)', 'color':'Current Clamp (nA)'}, title = 'Firing frequency / cell for different current stimulus')
fig.show()


fig = px.scatter(dfss, x='cellnum', y='sdur',color='amp', size = 'amp', hover_data=['cellnum','sdur','amp',df.km,df.ka], labels={'cellnum':'Cell Number',
'sdur':'Duration of Firing (ms)', 'amp':'Current Clamp (nA)'}, title = 'Duration of Firing / cell for different current stimulus')
fig.show()

fig = px.scatter(dfss, x='cellnum', y='f1',color='amp', size = 'amp', hover_data=['cellnum','f1','amp',df.km,df.ka], labels={'cellnum':'Cell Number','f1':'1st ISI (Hz)', 'amp':'Current Clamp (nA)'}, title = 'First ISI / cell for different current stimulus')
fig.show()

#
stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
stimend = stim['dur'] + stim['delay']
dclass=df[['amp','cellnum']].copy()
dclass['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
dclass['Vrmp'] = dclass.Vlist.apply(lambda x: x[0])
dclass['spkend'] = df.spkt.apply(lambda x: x[len(x)-1] if len(x)>0 else -1)

dclass['Vsubth'] = dclass.Vlist.apply(lambda x: 2**0 if max(x)<0 else np.nan)
dclass['Vph'] = dfss.scnt.apply(lambda x: 2**1 if 0<x<=1 else np.nan)
dclass['Vton'] = df.spkt.apply(lambda x: 2**2 if len(x)>3 and stim['delay']<=x[-1]<=stimend+5 else np.nan)
dclass['Vton_susps'] = dclass.spkend.apply(lambda x: 2**3 if stimend+5<=x>=data[list(data)[0]]['simConfig']['duration']-50 else np.nan)
dclass['Vton_brfps'] = dclass.spkend.apply(lambda x: 2**4 if stimend+5<=x<=data[list(data)[0]]['simConfig']['duration']-50 else np.nan)

f=go.Figure()
f.add_trace(go.Scatter(x=dclass['cellnum'], y=dclass['Vsubth'], mode = 'markers', marker = dict(color = 'beige', size =20, line = dict(color='MediumPurple',width=2)), text = dclass.cellnum, name = 'Subthreshold', showlegend=True))

f.add_trace(go.Scatter(x=dclass['cellnum'], y=dclass['Vph'], mode = 'markers', marker = dict(color = 'LightPink', size =20, line = dict(color='MediumPurple',width=2)), text = dclass.cellnum, name = 'Phasic', showlegend=True))

f.add_trace(go.Scatter(x=dclass['cellnum'], y=dclass['Vton'], mode = 'markers', marker = dict(color = 'LightSkyBlue', size =20, line = dict(color='MediumPurple',width=2)), text = dclass.cellnum, name = 'Tonic', showlegend=True))

f.add_trace(go.Scatter(x=dclass['cellnum'], y=dclass['Vton_susps'], mode = 'markers', marker = dict(color = 'LightSteelBlue', size =20, line = dict(color='MediumPurple',width=2)), text = dclass.cellnum, name = 'Tonic with Sustained Post-stim', showlegend=True))

f.add_trace(go.Scatter(x=dclass['cellnum'], y=dclass['Vton_brfps'], mode = 'markers', marker = dict(color = 'LightSeagreen', size =20, line = dict(color='MediumPurple',width=2)), text = dclass.cellnum, name = 'Tonic with Brief Post-stim', showlegend=True))

f.update_layout(title='Classification of Responses',legend_orientation='v')
f.update_xaxes(title='Cell Number')

f.show()

fi = go.Figure()
fi.add_trace(go.Mesh3d(x=dfss.cellnum, y=dfss.amp,z=dfss.hz,opacity=0.5,color='rgba(244,22,100,0.6)'))
fi.show()
fi.add_trace(go.Heatmap(x=dfss.cellnum, y=dfss.amp,z=dfss.hz)


# NOT WORKING :.( after soo many hours!!
#Tallying 
dtally = dclass[['cellnum','amp','Vsubth','Vph','Vton','Vton_susps','Vton_brfps']].copy()
cl = list(dtally)
del cl[0:2]
dtally[cl] = dtally[cl].div([1,2,4,8,16])
grpamp = dtally.groupby('amp')
barplt = grpamp[cl].sum()
barplt = barplt.div(barplt.sum()).mul(100)
fig = px.bar(barplt, text = 'value', labels={'amp':'Current Stimulus (nA)','value':'Percentage','variable':'Classification Subtypes'})
newnames = {'Vsubth':'Subthreshold','Vph':'Phasic','Vton':'Tonic','Vton_susps': 'Tonic with Sustained Post-stim', 'Vton_brfps': 'Tonic with Brief Post-stim'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],legendgroup = newnames[t.name],hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
fig.update_traces(texttemplate='%{text:3.2f}', textposition='inside')
fig.show()



total = d[cl].sum()
total.name = 'Total'
d = d.append(total.transpose())
perc = d.loc['Total'].div(d.loc['Total'].sum()).mul(100)
perc.name = 'Percentage'
d = d.append(perc.transpose())

d = dclass[['cellnum','amp','Vsubth','Vph','Vton','Vton_susps','Vton_brfps']].copy()
c = list(d)
del c[0:2]
grp = d.groupby(['cellnum','amp']).sum()
grp[cl] =grp[cl].div([1,2,4,8,16])
grp['sum']=grp.sum(axis=1)

tal = grp[cl].divide([1,2,4,8,16])
total = tal.sum()
total.name = 'Total'
tal = tal.append(total.transpose())
perc = tal.loc['Total'].div(tal.loc['Total'].sum()).mul(100)
perc.name = 'Percentage'
tal = tal.append(perc.transpose())





tal.sum() -> each entry should be 16 but it's not -> some are not getting classified -> sanity check -> need to check what's wrong

grp['sum']=grp.sum(axis=1) # for the row/cell-based classification as Raj suggested but it's no use since each cell is run 'sample' 							   # of times. It will work if only cellnum and amp are varied. Not if, more dims are involved
g = d.groupby(['cellnum','amp'])
g.describe()
g.apply(print)

