"""
analysis.py: Functions to read and interpret figures from the batch simulation results.
"""
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

df = dfss = filenamepkl = None

def readAllData(filename, dfonly=True):
    '''read _allData.json routine to get params and data'''
    global params, data, df
    with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
    params, data, df = dataLoad['params'], dataLoad['data'], toPandas(dataLoad['params'], dataLoad['data'])
    return df if dfonly else params, data, df

# readBatchData(dataFolder, batchLabel, target=None, saveAll=True, vars=None, maxCombs=None, listCombs=None)
def readBatchData(dataFolder, batchLabel, paramFile = 'params.csv', target=None, saveAll=True, vars=None, maxCombs=None, listCombs=None):
    '''gather data from dataFolder with batchLabel and save back to dataFolder or to target'''
    params, data=None,None
    # read the batch file and cfg
    batchFile = f'{dataFolder}/{batchLabel}_batch.json'
    with open(batchFile, 'r') as fileObj:
        b = json.load(fileObj)['batch']

    if b['method'] == 'grid':
        if isinstance(listCombs, str):
            filename = str(listCombs)
            with open(filename, 'r') as fileObj:
                dataLoad = json.load(fileObj)
            listCombs = dataLoad['paramsMatch']

        # read params labels and ranges
        params = b['params']

        # reorder so grouped params come first
        preorder = [p for p in params if 'group' in p and p['group']]
        for p in params:
            if p not in preorder: preorder.append(p)
        params = preorder

        # read vars from all files - store in dict
        labelList, valuesList = list(zip(*[(p['label'], p['values']) for p in params]))
        valueCombinations = product(*(valuesList))
        indexCombinations = product(*[list(range(len(x))) for x in valuesList])
        data = {}
        print('Reading data...')
        missing = 0
        for i,(iComb, pComb) in enumerate(zip(indexCombinations, valueCombinations)):
            if (not maxCombs or i<= maxCombs) and (not listCombs or list(pComb) in listCombs):
                print(i, iComb)
                # read output file
                iCombStr = ''.join([''.join('_'+str(i)) for i in iComb])
                simLabel = b['batchLabel']+iCombStr
                outFile = b['saveFolder']+'/'+simLabel+'_data.json'
                try:
                    with open(outFile, 'r') as fileObj:
                        output = json.load(fileObj, object_pairs_hook=OrderedDict)
                    # save output file in data dict
                    data[iCombStr] = {}
                    data[iCombStr]['paramValues'] = pComb  # store param values
                    if not vars: vars = list(output.keys())

                    for key in vars:
                        if isinstance(key, tuple):
                            container = output
                            for ikey in range(len(key)-1):
                                container = container[key[ikey]]
                            data[iCombStr][key[1]] = container[key[-1]]

                        elif isinstance(key, str):
                            data[iCombStr][key] = output[key]

                except:
                    print('... file missing')
                    missing = missing + 1
                    output = {}
            else:
                missing = missing + 1

        print('%d files missing' % (missing))
    elif b['method'] == 'list':
        fileList = [x.name for x in os.scandir(dataFolder) if x.name.endswith('_data.json')]
        fileList.sort(key=lambda x: int(re.split(f'{batchLabel}|[_.]',x)[1]))
        dfParam = pd.read_csv(paramFile,delimiter=',')
        data = {}
        if (len(dfParam)!=len(fileList)):
            raise Exception(f"The number of files in {dataFolder} and the no. of parameters in {paramFile} do not match. {paramFile} cannot be read")
        labelList = list(dfParam.columns)
        params=[]
        for lab in labelList:
            params.append({'label':lab,'values':list(dfParam[lab])})
        for (iloc,datafile),paralist in zip(enumerate(fileList),dfParam.values):
            outFile = f'{dataFolder}/{datafile}'
            indexComb=int(re.split(f'{batchLabel}|[_.]',datafile)[1])
            data[indexComb] = {}
            paraComb = tuple(paralist)
            data[indexComb]['paramValues'] = paraComb
            with open(outFile, 'r') as fileObj:
                output = json.load(fileObj, object_pairs_hook=OrderedDict)
                if all([output['simConfig'][x]!=y for x,y in zip(labelList,dfParam.loc[iloc])]):
                    raise Exception(f"Parameter values in {paramFile} and in the json files do not match")
            if not vars: vars = list(output.keys())
            for key in vars:
                data[indexComb][key] = output[key]

	#pass

    else:
        raise Exception(f"Method {b['method'] if b['method'] else 'No method'} files cannot be read.")
    # save
    if saveAll:
        print('Saving to single file with all data')
        filename = f'{batchLabel}_allData.json'
        dataSave = {'params': params, 'data': data}
        with open(filename, 'w') as fileObj:
            json.dump(dataSave, fileObj)
    else:
        return params, data

# toPandas(params, data) convert data to Pandas
def toPandas(params, data):
    if 'simData' in data[list(data.keys())[0]]:
        rows = [list(d['paramValues'])+[s for s in list(d['simData'].values())] for d in list(data.values())]
        cols = [str(d['label']) for d in params]+[s for s in list(data[list(data.keys())[0]]['simData'].keys())]
    else:
        rows = [list(d['paramValues'])+[s for s in list(d.values())] for d in list(data.values())]
        cols = [str(d['label']) for d in params]+[s for s in list(data[list(data.keys())[0]].keys())]

    df = pd.DataFrame(rows, columns=cols)
    df['simLabel'] = list(data.keys())

    colRename=[]
    for col in list(df.columns):
        if col.startswith("[u'"):
            colName = col.replace(", u'","_'").replace("[u","").replace("'","").replace("]","").replace(", ","_")
            colRename.append(colName)
        else:
            colRename.append(col)
    df.columns = colRename

    return df

def plotEpas(df = df):
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

    font = 20

    f=go.Figure()
    f.add_trace(go.Scatter(x=dfep['cellnum'], y=dfep['pasv'], mode = 'markers', marker = dict(color = 'LightPink', size =20, line = dict(color='MediumPurple',width=2)), text = dfep.cellnum, name = 'Reversal Potential (mV)', showlegend=True))

    f.add_trace(go.Scatter(x=dfep['cellnum'], y=dfep['vm'], mode = 'markers', marker = dict(color = 'black', size =5, line = dict(color='MediumPurple',width=2)), text = dfep.cellnum, name = 'Resting Membrane Potential', showlegend=True))
    f.update_layout(width=1200,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),template='simple_white')
    f.update_xaxes(title='Neuronal-Type ID (T#)')
    f.write_image('P_epas.png')
    f.show()
    return

def plotRin (df=df):
    ripk = {}

    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    cells = df['cellnum'].tolist()
    for i in df['t'][0]:        #dt is same so time array is same for all cells
        if i<(stim['delay']):
            init = df['t'][0].index(i)
        if i<(stim['delay']+stim['dur']):
            end = df['t'][0].index(i)
    d = df[['cellnum','V_soma']].copy()
    d['ripk']=d.V_soma.apply(lambda x:(min(x['cell_0'][init:end])-x['cell_0'][init])/stim['amp'])
    # d['ripk'].to_csv('rinQ.csv')
    font = 18
    fr = px.scatter(d, x='cellnum', y='ripk', hover_data=['cellnum','ripk',df.index], labels={'cellnum':'Neuronal-Type ID (T#)','ripk':"Input Impedance (M\u03A9)"},template="simple_white")
    fr.update_traces(marker=dict(color = 'LightSteelBlue',size=font/2,line = dict(color='MediumPurple',width=2)))
    fr.update_layout(width=614.4,height=460.8,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    pio.write_image(fr,"P_Rin.png",format='png',scale=10,width=614.4,height=460.8, validate=True)
    fr.show()
    return

def plotRheobase(df):
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

    font = 18
    fr = px.scatter(drh, y='cellnum', x='rheo', hover_data=['cellnum','rheo'], labels={'cellnum':'Neuronal-Type ID (T#)','rheo':"Rheobase (nA)"},template="simple_white")
    fr.update_traces(marker=dict(color = 'Turquoise',size=font/2,line = dict(color='MediumPurple',width=2)))
    fr.update_layout(width=614.4,height=460.8,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    pio.write_image(fr,"R_Rheobase.png",format='png',scale=10,width=614.4,height=460.8, validate=True)
    fr.show()
    return

#ap metrics

def plotVm(df,batchLabel):
    makedirs(f'{batchLabel}/vmPlots')
    font = 15
    for indx in df.index:
        f = plt.figure()
        plt.plot(df['t'][indx],df['V_soma'][indx]['cell_0'],c='C0')
        plt.xlabel('Time (ms)', fontsize=font)
        plt.ylabel('Membrane Voltage (mV)', fontsize=font)
        plt.title(f"Neuronal-Type ID: T{df['cellnum'][indx]+1}", fontsize=font)
        plt.tick_params(axis='both',labelsize=font)
        plt.savefig(f"{batchLabel}/vmPlots/{df['simLabel'][indx]}.png",dpi=300,bbox_inches='tight')
        plt.close()
    return

def currentScapes(df,batchLabel):
    font = 17
    dp = df[['cellnum','simLabel']].copy()

    do = df[['cellnum','simLabel']].copy()
    do['io'] = df.ik.apply(lambda x: x['cell_0'] if x!={} else [0])
    do['ikcna'] = df.ikcna.apply(lambda x: x['cell_0'] if x!={} else [0])
    do['ikcnc'] = df.ikcnc.apply(lambda x: x['cell_0'] if x!={} else [0])
    do['ikcnj'] = df.ikcnj3.apply(lambda x: x['cell_0'] if x!={} else [0])
    dp['ska'] = do.ikcna.apply(lambda x: np.sum(x))
    dp['skc'] = do.ikcnc.apply(lambda x: np.sum(x))
    dp['skj'] = do.ikcnj.apply(lambda x: np.sum(x))

    di = df[['cellnum','simLabel']].copy()

    di['ina'] = df.ina.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica'] = df.ica.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ih'] = df.ih.apply(lambda x: x['cell_0'] if x!={} else [0])
    di = di.assign(ii=[np.array(n)+np.array(c)+np.array(h) for n,c,h in zip(di['ina'], di['ica'], di['ih'])])

    di['ica1a'] = df.ica1a.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica1b'] = df.ica1b.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica1c'] = df.ica1c.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica1d'] = df.ica1d.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica1g'] = df.ica1g.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ica1i'] = df.ica1i.apply(lambda x: x['cell_0'] if x!={} else [0])

    di['ihcn1'] = df.ihcn1.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ihcn2'] = df.ihcn2.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ihcn3'] = df.ihcn3.apply(lambda x: x['cell_0'] if x!={} else [0])
    di['ihcn4'] = df.ihcn4.apply(lambda x: x['cell_0'] if x!={} else [0])

    dp['sna'] = di.ina.apply(lambda x: np.sum(x))
    dp['sc1a'] = di.ica1a.apply(lambda x: np.sum(x))
    dp['sc1b'] = di.ica1b.apply(lambda x: np.sum(x))
    dp['sc1c'] = di.ica1c.apply(lambda x: np.sum(x))
    dp['sc1d'] = di.ica1d.apply(lambda x: np.sum(x))
    dp['sc1g'] = di.ica1g.apply(lambda x: np.sum(x))
    dp['sc1i'] = di.ica1i.apply(lambda x: np.sum(x))
    dp['sh1'] = di.ihcn1.apply(lambda x: np.sum(x))
    dp['sh2'] = di.ihcn2.apply(lambda x: np.sum(x))
    dp['sh3'] = di.ihcn3.apply(lambda x: np.sum(x))
    dp['sh4'] = di.ihcn4.apply(lambda x: np.sum(x))

    ci = ['lavender','yellow','moccasin','olivedrab','yellowgreen','salmon','lightpink','lightgrey','peru','palegreen','plum']
    co =['paleturquoise','lightsteelblue','mistyrose']
    li = ['Scn1a','Cacna1a','Cacna1b','Cacna1c','Cacna1d','Cacna1g','Cacna1i','HCN1','HCN2','HCN3','HCN4']
    lo = ['Kcna1+ab1','Kcnc1','Kcnj3']

    makedirs(f'{batchLabel}/percI')
    for indx in [0,1]: #dp.index:
        fr = make_subplots(cols=2, rows=1,specs=[[{"type": "domain"}, {"type": "domain"}]],subplot_titles=["%Inward Currents","%Outward Currents"]) 
        fr.add_trace(go.Pie(labels = li,values= dp[['sna','sc1a','sc1b','sc1c','sc1d','sc1g','sc1i','sh1','sh2','sh3','sh4']].copy().transpose().abs()[indx].tolist(),text=li,showlegend = True,marker = dict(colors = ci, line = dict(color='black',width=0.5)),insidetextorientation='horizontal', rotation = 180), row = 1, col = 1)
        fr.add_trace(go.Pie(labels = lo, values= dp[['ska','skc','skj']].copy().transpose()[indx].tolist(),text=lo,showlegend = True,marker = dict(colors = co, line = dict(color='black',width=0.5)),insidetextorientation='horizontal', rotation = 0), row = 1, col = 2)
        fr.update_layout(width=1100,height=600,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),title = f"Neuronal-Type ID: T{dp['cellnum'][indx]+1}")
        fr.update_annotations(font_size=font) # for sublot titles
        # fr.show()
        pio.write_image(fr,f"{batchLabel}/percI/{dp['simLabel'][indx]}.png",format='png',scale=10,width=1100,height=800, validate=True)
    del fr

    # Currentscapes
    dm = df[['cellnum','simLabel','t']].copy()
    dm = dm.assign(ka = [np.array(x)/(np.array(t)) for x,t in zip(do['ikcna'],do['io'])])
    dm = dm.assign(kc = [np.array(x)/(np.array(t)) for x,t in zip(do['ikcnc'],do['io'])])
    dm = dm.assign(kj = [np.array(x)/(np.array(t)) for x,t in zip(do['ikcnj'],do['io'])])

    dm = dm.assign(na = [np.array(x)/(np.array(t)) for x,t in zip(di['ina'],di['ii'])])
    dm = dm.assign(c1a = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1a'],di['ii'])])
    dm = dm.assign(c1b = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1b'],di['ii'])])
    dm = dm.assign(c1c = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1c'],di['ii'])])
    dm = dm.assign(c1d = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1d'],di['ii'])])
    dm = dm.assign(c1g = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1g'],di['ii'])])
    dm = dm.assign(c1i = [np.array(x)/(np.array(t)) for x,t in zip(di['ica1i'],di['ii'])])
    dm = dm.assign(h1 = [np.array(x)/(np.array(t)) for x,t in zip(di['ihcn1'],di['ii'])])
    dm = dm.assign(h2 = [np.array(x)/(np.array(t)) for x,t in zip(di['ihcn2'],di['ii'])])
    dm = dm.assign(h3 = [np.array(x)/(np.array(t)) for x,t in zip(di['ihcn3'],di['ii'])])
    dm = dm.assign(h4 = [np.array(x)/(np.array(t)) for x,t in zip(di['ihcn4'],di['ii'])])

    dm['V'] = df.V_soma.apply(lambda x: x['cell_0'])

    #### raw Currents vs t

    makedirs(f'{batchLabel}/currentScapes')
    for indx in [0,1]: #dp.index:
        vm = [(v-min(dm['V'][indx]))/(max(dm['V'][indx])-min(dm['V'][indx])) for v in dm['V'][indx]]

        q=0
        fr = make_subplots(cols=1, rows=3)
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = dm['V'][indx],name='',mode='lines',line=dict(width=1,color='black'),fill = 'none',fillcolor='slategray',stackgroup='one'),row=1,col=1)
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ina'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1a'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1b'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1c'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1d'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1g'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ica1i'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ihcn1'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ihcn2'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ihcn3'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = np.abs(di['ihcn4'][indx]),name=li[q],mode='lines',line=dict(width=1,color='indigo'),fill = 'tonexty',fillcolor=ci[q],stackgroup='one'),row=2,col=1)
        q = 0
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = do['ikcna'][indx],name=lo[q],mode='lines',line=dict(width=1,color='black'),fill = 'tonexty',fillcolor=co[q],stackgroup='one'),row=3,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = do['ikcnc'][indx],name=lo[q],mode='lines',line=dict(width=1,color='black'),fill = 'tonexty',fillcolor=co[q],stackgroup='one'),row=3,col=1)
        q+=1
        fr.add_trace(go.Scatter(x = dm['t'][indx], y = do['ikcnj'][indx],name=lo[q],mode='lines',line=dict(width=1,color='black'),fill = 'tonexty',fillcolor=co[q],stackgroup='one'),row=3,col=1)
        fr.update_xaxes(title_text="Time (ms)", row=3, col=1)
        fr.update_yaxes(title_text='Membrane Potential <br> (V<sub>m</sub>) (mV)', row=1, col=1)
        fr.update_yaxes(title_text='Inward Currents <br> (mA/cm<sup>2</sup>)', type = 'log',row=2, col=1)
        fr.update_yaxes(title_text='Outward Currents <br> (mA/cm<sup>2</sup>)', type = 'log',row=3, col=1)
        fr.update_layout(width=1100,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),legend_traceorder='normal',title = f"Neuronal-Type ID: T{dm['cellnum'][indx]+1}",template = 'simple_white')
        fr.update_annotations(font_size=font) # for sublot titles
        pio.write_image(fr,f"{batchLabel}/currentScapes/{dm['simLabel'][indx]}.png",format='png',scale=10,width=1100,height=800, validate=True)
    return

def IV(df):
    div=df[['cellnum','vc']].copy() #,'ina','ik','ica','ih','ipas'
    # div.replace({},)
    div['ina'] = df.ina.apply(lambda x: x['cell_0'] if x!={} else 0)
    div['ik'] = df.ik.apply(lambda x: x['cell_0'] if x!={} else 0)
    div['ica'] = df.ica.apply(lambda x: x['cell_0'] if x!={} else 0)
    div['ih'] = df.ih.apply(lambda x: x['cell_0'] if x!={} else 0)
    div['ipas'] = df.ipas.apply(lambda x: x['cell_0'] if x!={} else 0)
    div = div.assign(imem=[np.array(n) + np.array(k)+np.array(c) + np.array(h)+np.array(p) for n,k,c,h,p in zip(div['ina'], div['ik'],div['ica'], div['ih'],div['ipas'])])
    div['im']=div.imem.apply(lambda x: max(x) if abs(max(x))>=abs(min(x)) else min(x))

    font=17
    f = px.line(div,x = 'vc',y='im',color=div['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3, line_dash = div['cellnum'], markers=True, symbol = div['cellnum'].astype(str), labels={'vc': 'Voltage Clamp Levels (mV)','im':'Membrane Current (mA/cm<sup>2</sup>)','color':''},template="simple_white")
    f.update_traces(line = dict(width=2), marker=dict(line = dict(width=1,color='indigo')))
    f.update_layout(width=640,height=460,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    f.update(layout_showlegend=False)
    pio.write_image(f,"iv.png",format='png',scale=5,width=640,height=460, validate=True)
    # f.show()
    return

def fI(df):
    dur = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']['dur']

    dfss=df[['amp', 'cellnum', 'avgRate']].copy()  # note double brackets
    dfss.scnt    = df.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss['scnt'] = df.spkt.apply(len)
    dfss['spk1'] = df.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
    dfss['f1']   = df.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
    dfss['f2']   = df.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
    dfss['sdur'] = df.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
    dfss['ffdur'] = dfss.sdur.apply(lambda x: dur if x<=dur else x)
    dfss['hzz']   = dfss.scnt.div(dfss.ffdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN
    dfss.drop(dfss.index[dfss['hzz'] == 0], inplace = True)
    dfss.drop(dfss.index[dfss['sdur'] == 0], inplace = True)

    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dfss['amp'])
    ydata = np.array(dfss['hzz']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)

    font = 17
    b = px.line(x=xdata, y=func(xdata, *optimizedParameters))
    b.update_traces(line=dict(color="Black", width=2.5))
    # fr = px.strip(dfss, x='amp', y='hzz', color = dfss['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3,template="simple_white")
    # fr.update_traces(marker=dict(size=font/1.5,line = dict(color='black',width=0.5)),jitter = 0)
    fr = px.line(dfss, x='amp', y='hzz',color=dfss['cellnum'].astype(str), color_discrete_sequence= px.colors.qualitative.Set3, line_dash = dfss['cellnum'], symbol = dfss['cellnum'],markers=True,template="simple_white")
    fr.update_traces(line = dict(width=2), marker=dict(size=font/1.8,line = dict(width=1,color='indigo')))
    fr.add_trace(b.data[0])
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False) 
    fr.update_layout(xaxis_title='Current Clamp (nA)', yaxis_title='Firing Frequency (Hz)',showlegend=False)
    pio.write_image(fr,"R_fi.png",format='png',scale=10,width=640,height=460, validate=True)
    fr.show()
    return

def phiI(df):
    dur = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']['dur']

    dfss=df[['amp','phi', 'cellnum', 'avgRate']].copy()  # note double brackets
    dfss.scnt    = df.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss['scnt'] = df.spkt.apply(len)
    dfss['spk1'] = df.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
    dfss['f1']   = df.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
    dfss['f2']   = df.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
    dfss['sdur'] = df.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
    dfss['ffdur'] = dfss.sdur.apply(lambda x: dur if x<=dur else x)
    dfss['hzz']   = dfss.scnt.div(dfss.ffdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN
    dfss.drop(dfss.index[dfss['hzz'] == 0], inplace = True)
    dfss.drop(dfss.index[dfss['sdur'] == 0], inplace = True)

    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dfss['phi'])
    ydata = np.array(dfss['hzz']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)

    font = 18
    b = px.line(x=xdata, y=func(xdata, *optimizedParameters))
    b.update_traces(line=dict(color="Black", width=2.5))
    fr = px.strip(dfss, x='phi', y='hzz', color = dfss['amp'].astype(str),color_discrete_sequence= px.colors.qualitative.Pastel1,labels={'phi':'Fractional Amplitude of <i>Kcnc1</i> currents','hzz':'Firing Frequency (Hz)','color':'Current Amplitude (nA)'},template="simple_white")
    fr.update_traces(marker=dict(size=font/1.4,line = dict(color='black',width=1)),jitter = 0)
    fr.add_trace(b.data[0])
    fr.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),width=1300,height=700,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    pio.write_image(fr,"phii.png",format='png',scale=3,width=1300,height=700, validate=True)
    # fr.show()

    #3D plot
    font = 16
    f = px.scatter_3d(dfss, x='phi', y='amp', z='hzz',color='hzz',color_continuous_scale='plasma', labels={'phi':'Fractional Amplitude of I<sub>Kcnc1</sub>','hzz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'},template="simple_white")
    f.update_traces(marker=dict(size=font/1.5,line = dict(color='black',width=2)))
    f.update_layout(width=1200,height=1000,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    pio.write_image(f,"3Dffphii.png",format='png',scale=3,width=1300,height=700, validate=True)
    # f.show()
    return

def classification(df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    dc=df[['amp','cellnum','spkt']].copy()
    dc['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dc['Vrmp'] = dc.Vlist.apply(lambda x: x[0])
    dc['spkend'] = df.spkt.apply(lambda x: x[len(x)-1] if len(x)>0 else -1)
    dc['scnt'] = df.spkt.apply(len)

    cnt = []
    for indx in dc.index:
        y = dc['Vlist'][indx]
        c = 0
        for i in range(0,len(y)-1):
            if (y[i] >= dc['Vrmp'][indx] and y[i + 1] < dc['Vrmp'][indx]) or (y[i] <= dc['Vrmp'][indx] and y[i + 1] > dc['Vrmp'][indx]):
                c = c+1
        cnt.append(c)
        del y

    dc['rmpCross'] = cnt
    del c,cnt

    temp = dc
    isi = []

    for ind in dc.index:
        e = dc.iloc[ind]['spkt']
        intval = [0]
        if len(e)>1:
            intval = [e[j+1]-e[j] for j in range(0,len(e)-1)]
        else:
            None
        isi.append(intval)

    dc['isi'] = isi
    dc['mxisi'] = dc.isi.apply(lambda x: max(x))
    del isi,intval,e, ind

    font = 18

    init = max([x if x<=2*stimend/3 else 0 for x in df['t'][0]])
    end = max([x if x<=stimend else 0 for x in df['t'][0]])

    q = 0
    dc['Subthreshold'] = dc.scnt.apply(lambda x: 2**q if x<1 else np.nan)
    q+=1
    dc['Phasic'] = dc.scnt.apply(lambda x: 2**q if 0<x<=1 else np.nan)
    q+=1
    dc['Doublet/Triplet/Quadruplet'] = dc[['spkend','scnt']].apply(lambda x: 2**q if ((x.spkend<=(stim['delay']+((stimend+5)/4))) and (1<x.scnt<=4)) else np.nan, axis=1)
    q+=1
    dc['Tonic'] = dc.spkt.apply(lambda x: 2**q if len(x)>=3 and stim['delay']<=x[-1]<=stimend+5 else np.nan)
    q+=1
    dc['Post-stimulus Firing'] = dc.spkend.apply(lambda x: 2**q if stimend+5<=x<=data[list(data)[0]]['simConfig']['duration'] else np.nan)
    q+=1
    dc['Depolarisation Block'] = dc[['Vlist','scnt','rmpCross']].apply(lambda x: 2**q if ((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt==1) and (x.rmpCross==2)) else np.nan, axis =1)
    q+=1
    dc['Tonic Block'] = dc[['Vlist','scnt','rmpCross','mxisi']].apply(lambda x: 2**q if (((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt>=1) and (x.rmpCross>2)) or (x.mxisi>=120))else np.nan, axis =1)
    q+=1
    dc['Incomplete Repolarisation'] = dc[['scnt','rmpCross']].apply(lambda x: 2**q if ((x.rmpCross==1) and (x.scnt==1)) else np.nan, axis =1)

    dclass = dc[['amp','cellnum','Subthreshold','Phasic','Doublet/Triplet/Quadruplet','Tonic','Post-stimulus Firing','Depolarisation Block','Tonic Block','Incomplete Repolarisation']].copy()
    subtypes = ['Subthreshold','Phasic','Doublet/Triplet/Quadruplet','Tonic','Post-stimulus Firing','Depolarisation Block','Tonic Block','Incomplete Repolarisation']
    col = ['lightgray','pink','lightgreen','skyblue','plum','darkgoldenrod','darkblue','firebrick']

    #list unclassified entries
    # d = dclass[['Subthreshold','Phasic','Doublet/Triplet/Quadraplet','Tonic','Post-stim Firing','Depolarization Block','Tonic Block','Incomplete Repolarization']].copy()
    d = dclass[subtypes]
    d['sum'] = d.sum(axis = 1,numeric_only=True)
    d.loc[d['sum']==0]

    barvar = dclass.groupby('cellnum')[subtypes].sum().div([1,2,4,8,16,32,64,128])
    fr = px.bar(barvar, color_discrete_sequence = col, labels={'value':"Firing Patterns Elicited",'cellnum':"Neuronal-Type ID (T#)",'variable':"Classification Subtypes"},template="simple_white") #Count of each Subtype
    fr.update_layout(width=1100,height=650,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),showlegend=False,legend_traceorder='normal')
    fr.update_yaxes(showticklabels=False)
    pio.write_image(fr,"R_classVar.png",format='png',scale=10,width=1100,height=650, validate=True)
    fr.show()

    baramp = dclass.groupby('amp')[subtypes].sum().div([1,2,4,8,16,32,64,128])
    percamp = baramp.transpose().transform(lambda x: x*100/x.sum()).transpose().round(0)
    print(f'BARAMP PLOT STATISTICS: \n\n\n {baramp.transpose().transform(lambda x: x*100/x.sum()).transpose().round(0)}')
    f = go.Figure()
    for i,cat in enumerate(subtypes):
        f.add_trace(go.Bar(name = cat, x = baramp.index, y= baramp[cat].tolist(),text=percamp[cat].tolist(),showlegend = True,marker = dict(color = col[i])))

    f.update_yaxes(title='No. of Ephys. Responses <br> across all Neuronal-Types')
    f.update_xaxes(title_text='Current Stimulus (nA)')
    f.update_layout(width=1100,height=650,uniformtext_minsize=font-8,uniformtext_mode='hide',font=dict(size=font, color='black'),barmode = 'stack',legend_traceorder='reversed',template = 'simple_white')
    pio.write_image(f,"R_classAmp.png",format='png',scale=10,width=800,height=650, validate=True)
    f.show()

    bartype = dclass.sum(numeric_only = True,axis=0).drop(['amp','cellnum']).div([1,2,4,8,16,32,64,128])
    print(f'BARTYPE PLOT STATISTICS: \n\n\n {bartype.transpose().transform(lambda x: x*100/x.sum()).transpose().round(2)}')
    print(bartype)
    return

### AP Metrics #### 

def apPeak(df):
    dap=df[['amp', 'cellnum', 'na','ina','V_soma']].copy()  
    dap['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dap['APpk']  = dap.Vlist.apply(lambda x: max(x))
    dap['scnt'] = df.spkt.apply(len)
    dap['Vph'] = dap.scnt.apply(lambda x: 1 if 0<x<=1 else 0)
    dap.drop(dap.index[dap['Vph'] == 0], inplace = True)
    dap.drop(dap.index[dap['ina'] == {}], inplace = True)

    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dap['na'])
    ydata = np.array(dap['APpk']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)

    font = 18
    b = px.line(x=xdata, y=func(xdata, *optimizedParameters))
    b.update_traces(line=dict(color="Black", width=2.5))
    fr = px.strip(dap, x='na', y='APpk',color = dap['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3,labels={'na':'<i>Scn1a</i> Channel Conductance (S/cm<sup>2</sup>)','APpk':'Action Potential Peak (mV)'},template="simple_white")
    fr.update_traces(marker=dict(size=font/1.5,line = dict(color='indigo',width=0.5)),jitter=0)
    fr.add_trace(b.data[0])
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False,showlegend=False)
    pio.write_image(fr,"napk.png",format='png',scale=10,width=650,height=500, validate=True)
    # fr.show()
    return

def apFF(df):
    dur = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']['dur']

    dap=df[['amp', 'cellnum', 'h1', 'ihcn1','avgRate']].copy()  # note double brackets
    dap.scnt    = df.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dap['scnt'] = df.spkt.apply(len)
    dap['spk1'] = df.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
    dap['f1']   = df.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
    dap['f2']   = df.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
    dap['sdur'] = df.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
    dap['ffdur'] = dap.sdur.apply(lambda x: dur if x<=dur else x)
    # dfss['hz']   = dfss.scnt.div(dfss.sdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN
    # dfss['hzz']   = dfss[['scnt','sdur']].apply(lambda x: (x.scnt*1e3)/dur if (x.sdur>0) else 0, axis=1) # >>> NaN
    dap['hzz']   = dap.scnt.div(dap.ffdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN
    dap.drop(dap.index[dap['hzz'] == 0], inplace = True)
    dap.drop(dap.index[dap['sdur'] == 0], inplace = True)
    dap.drop(dap.index[dap['ihcn1'] == {}], inplace = True)

    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dap['h1'])
    ydata = np.array(dap['hzz']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)


    font = 18
    b = px.line(x=xdata, y=func(xdata, *optimizedParameters))
    b.update_traces(line=dict(color="Black", width=2.5))
    fr = px.strip(dap, x='h1', y='hzz', color = dap['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3,labels={'h1':'<i>HCN1</i> Channel Conductance (S/cm<sup>2</sup>)','hzz':'Firing Frequency (Hz)'},template="simple_white")
    fr.update_traces(marker=dict(size=font/1.5,line = dict(color='indigo',width=0.5)),jitter = 0)
    fr.add_trace(b.data[0])
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False,showlegend=False) 
    pio.write_image(fr,"h1ff.png",format='png',scale=10,width=650,height=500, validate=True)
    # fr.show()
    return

def apHyp(df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']

    dkc=df[['amp','cellnum','kc','ikcnc','spkt']].copy()
    dkc['scnt'] = dkc.spkt.apply(len)
    dkc['Vph'] = dkc.scnt.apply(lambda x: 1 if 0<x<=1 else 0)
    dkc['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dkc['Vrmp'] = dkc.Vlist.apply(lambda x: x[0])

    cnt = []
    for indx in dkc.index:
        y = dkc['Vlist'][indx]
        c = 0
        for i in range(0,len(y)-1):
            if (y[i] >= dkc['Vrmp'][indx] and y[i + 1] < dkc['Vrmp'][indx]) or (y[i] <= dkc['Vrmp'][indx] and y[i + 1] > dkc['Vrmp'][indx]):
                c = c+1
        cnt.append(c)
        del y

    dkc['rmpCross'] = cnt
    del c,cnt

    isi = []
    for ind in dkc.index:
        e = dkc.iloc[ind]['spkt']
        intval = [0]
        if len(e)>1:
            intval = [e[j+1]-e[j] for j in range(0,len(e)-1)]
        else:
            None
        isi.append(intval)

    dkc['isi'] = isi
    dkc['mxisi'] = dkc.isi.apply(lambda x: max(x))
    del isi,intval,e, ind

    init = max([x if x<=2*stimend/3 else 0 for x in df['t'][0]])
    end = max([x if x<stimend-5 else 0 for x in df['t'][0]])

    dkc['dblk'] = dkc[['Vlist','scnt','rmpCross']].apply(lambda x: 1 if ((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt==1) and (x.rmpCross==2)) else 0, axis =1)
    dkc['tblk'] = dkc[['Vlist','scnt','rmpCross','mxisi']].apply(lambda x: 1 if (((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt>=1) and (x.rmpCross>2)) or (x.mxisi>=120)) else 0, axis =1)
    dkc['incomp'] = dkc[['scnt','rmpCross']].apply(lambda x: 1 if ((x.rmpCross==1) and (x.scnt==1)) else 0, axis =1)


    dkc.drop(dkc.index[dkc['Vph'] == 0], inplace = True)
    dkc.drop(dkc.index[dkc['ikcnc'] == {}], inplace = True)
    dkc.drop(dkc.index[dkc['dblk'] == 1], inplace = True)
    dkc.drop(dkc.index[dkc['tblk'] == 1], inplace = True)
    dkc.drop(dkc.index[dkc['incomp'] == 1], inplace = True)

    dkc['Vmin'] = dkc.Vlist.apply(lambda x: min(x[x.index(max(x)) : df['t'][0].index(end)]))


    font = 18
    fr = px.scatter(dkc, x='kc', y='Vmin', log_x=False, color = dkc['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3, labels={'kc':'<i>Kcnc1</i> Channel Conductance (S/cm<sup>2</sup>)','Vmin':"Hyperpolarization Potential (mV)"},template="simple_white",trendline="ols", trendline_scope="overall", trendline_color_override="Black") #,trendline_options=dict(log_x=True))
    fr.update_traces(marker=dict(size=font/1.5,line = dict(color='indigo',width=0.5)))
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False,showlegend=False)
    pio.write_image(fr,"kchyp.png",format='png',scale=5,width=650,height=500, validate=True)
    # fr.show()

    results = px.get_trendline_results(fr)

    print(results.px_fit_results.iloc[0].summary())
    return

def apFWHM(df): 
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']

    init = max([x if x<=2*stimend/3 else 0 for x in df['t'][0]])
    end = max([x if x<=stimend else 0 for x in df['t'][0]])

    dw=df[['amp', 'cellnum', 'c1b','ica1b','V_soma','spkt']].copy()  # h2:ihcn2     
    dw['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dw['Vrmp'] = dw.Vlist.apply(lambda x: x[0])
    dw['scnt'] = df.spkt.apply(len)
    dw['Vph'] = dw.scnt.apply(lambda x: 1 if 0<x<=1 else 0)

    cnt = []
    for indx in dw.index:
        y = dw['Vlist'][indx]
        c = 0
        for i in range(0,len(y)-1):
            if (y[i] >= dw['Vrmp'][indx] and y[i + 1] < dw['Vrmp'][indx]) or (y[i] <= dw['Vrmp'][indx] and y[i + 1] > dw['Vrmp'][indx]):
                c = c+1
        cnt.append(c)
        del y

    dw['rmpCross'] = cnt
    del c,cnt

    isi = []

    for ind in dw.index:
        e = dw.iloc[ind]['spkt']
        intval = [0]
        if len(e)>1:
            intval = [e[j+1]-e[j] for j in range(0,len(e)-1)]
        else:
            None
        isi.append(intval)


    dw['isi'] = isi
    dw['mxisi'] = dw.isi.apply(lambda x: max(x))
    del isi,intval,e, ind

    dw['dblk'] = dw[['Vlist','scnt','rmpCross']].apply(lambda x: 1 if ((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt==1) and (x.rmpCross==2)) else 0, axis =1)
    dw['tblk'] = dw[['Vlist','scnt','rmpCross','mxisi']].apply(lambda x: 1 if (((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt>=1) and (x.rmpCross>2)) or (x.mxisi>=120)) else 0, axis =1)
    dw['incomp'] = dw[['scnt','rmpCross']].apply(lambda x: 1 if ((x.rmpCross==1) and (x.scnt==1)) else 0, axis =1)


    dw.drop(dw.index[dw['Vph'] == 0], inplace = True)
    dw.drop(dw.index[dw['ica1b'] == {}], inplace = True)
    dw.drop(dw.index[dw['dblk'] == 1], inplace = True)
    dw.drop(dw.index[dw['tblk'] == 1], inplace = True)
    dw.drop(dw.index[dw['incomp'] == 1], inplace = True)

    dw['APpk']  = dw.Vlist.apply(lambda x: max(x))
    dw['Hfmag'] = dw.APpk.sub(dw.Vrmp).mul(0.5).add(dw.Vrmp)

    wid = []

    for indx in dw.index:
        v = dw['Vlist'][indx]
        t1 = 0
        t2 = 0
        for i in range(0,len(v)-1):
            if (v[i] <= dw['Hfmag'][indx] and v[i + 1] >= dw['Hfmag'][indx]):
                t1 = df['t'][0][i]
            if (v[i] >= dw['Hfmag'][indx] and v[i + 1] <= dw['Hfmag'][indx]):
                t2 = df['t'][0][i]
        wid.append((t2-t1))
        del v

    dw['fwhm'] = wid 
    del t1, t2, wid


    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dw['c1b'])
    ydata = np.array(dw['fwhm']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)

    font = 18
    b = px.line(x=xdata, y=func(xdata, *optimizedParameters))
    b.update_traces(line=dict(color="Black", width=2.5))
    fr = px.strip(dw, x='c1b', y='fwhm', color = dw['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3,labels={'c1b':'<i>Cacna1b</i> Channel Conductance (S/cm<sup>2</sup>)','fwhm':'Full Width at Half-Maximum (ms)'},template="simple_white")
    fr.update_traces(marker=dict(size=font/1.5,line = dict(color='indigo',width=0.5)),jitter = 0)
    fr.add_trace(b.data[0])
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False,showlegend=False) 
    pio.write_image(fr,"c1bwid.png",format='png',scale=10,width=650,height=500, validate=True)
    # fr.show()
    return





