# -*- coding: utf-8 -*-
"""
Created on 18 Aug. 2022

@author: sgupta
"""

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
import scipy
import scipy.optimize as opt
from plotly.subplots import make_subplots

df = dfss = filenamepkl = None

# Reading the _allData.json
def readAllData(filename, dfonly=True):
    '''read _allData.json routine to get params and data'''
    global params, data, df
    with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
    params, data, df = dataLoad['params'], dataLoad['data'], toPandas(dataLoad['params'], dataLoad['data'])
    return df if dfonly else params, data, df

# Generating the _allData.json after running batch simulations
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

# @author: sgupta
# Plotting firing frequency-current curves
def fI(df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    dur = stim['dur']
    dc=df[['amp','cellnum','spkt']].copy()
    dc['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dc['Vrmp'] = dc.Vlist.apply(lambda x: x[0])
    dc['spkend'] = df.spkt.apply(lambda x: x[len(x)-1] if len(x)>0 else -1)
    dc['scnt'] = df.spkt.apply(len)

    #computing no. of times Vm crosses resting membrane potential
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

    #computing no. of times Vm crosses a set subthreshold value
    ct = []
    for indx in dc.index:
        y = dc['Vlist'][indx]
        z = 0
        for i in range(0,len(y)-1):
            if ((y[i] >= -40 and y[i + 1] < -40) or (y[i] <= -40 and y[i + 1] > -40)):
                z = z+1
        ct.append(z)
        del y

    dc['subthrCross'] = ct
    del ct,z

    temp = dc
    isi = []

    # computing inter-spike interval
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

    col_names = dc.columns.values.tolist()
    print(col_names)
    df_shape = dc.shape
    print("Number of rows: ", df_shape[0])
    print("Number of columns: ", df_shape[1])

    init = max([x if x<=2*stimend/3 else 0 for x in df['t'][0]])
    end = max([x if x<=stimend else 0 for x in df['t'][0]])


    dc['Block'] = dc[['Vlist','scnt','rmpCross','mxisi','subthrCross']].apply(lambda x: np.nan if (((-40<= max(x.Vlist[df['t'][0].index(init):df['t'][0].index(end)])<-10) and (x.scnt>=1) and (x.rmpCross>=2)) or ((x.scnt>=1) and ((2*x.scnt)/x.subthrCross < 1)) or (x.mxisi>=120)) else 1, axis =1)
    dc['Phasic'] = dc.scnt.apply(lambda x: np.nan if 0<x<=1 else 1)
    dc['Burst'] = dc[['spkend','scnt','subthrCross']].apply(lambda x: np.nan if ((x.spkend<=(stim['delay']+((stimend+5)/4))) and (1<x.scnt<=4) and (x.scnt == x.subthrCross/2)) else 1, axis=1)
    dc['Post-stimulus Firing'] = dc.spkend.apply(lambda x: np.nan if stimend+5<=x<=data[list(data)[0]]['simConfig']['duration'] else 1)
    dc['Tonic'] = dc.spkt.apply(lambda x: 1 if len(x)>4 and stim['delay']<=x[-1]<=stimend+5 else np.nan)

    dfss = dc.dropna() #Plot only for tonically firing cells


    dfss.scnt    = dc.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss['scnt'] = dc.spkt.apply(len)
    dfss['spk1'] = dc.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
    dfss['f1']   = dc.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
    dfss['f2']   = dc.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
    dfss['sdur'] = dc.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
    dfss['ffdur'] = dfss.sdur.apply(lambda x: dur if x<=dur else x)
    dfss['hzz']   = dfss.scnt.div(dfss.ffdur).mul(1e3).fillna(0).replace(np.inf,0) # >>> NaN
    dfss.drop(dfss.index[dfss['hzz'] == 0], inplace = True)
    dfss.drop(dfss.index[dfss['sdur'] == 0], inplace = True)

    # least-error fit
    def func(x, m, c):
        return (m*x) + c
    xdata = np.array(dfss['amp'])
    ydata = np.array(dfss['hzz']) 
    optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata)

    print(optimizedParameters)

    font = 17
    fr = px.strip(dfss, x='amp', y='hzz', color = dfss['cellnum'].astype(str), color_discrete_sequence = px.colors.qualitative.Set3,template="simple_white")
    fr.update_traces(marker=dict(size=font/1.5,line = dict(color='black',width=0.5)),jitter = 0)
    fr = px.line(dfss, x='amp', y='hzz',color=dfss['cellnum'].astype(str), color_discrete_sequence= px.colors.qualitative.Set3, line_dash = dfss['cellnum'], symbol = dfss['cellnum'],markers=True,template="simple_white")
    fr.update_traces(line = dict(width=2), marker=dict(size=font/1.8,line = dict(width=1,color='indigo')))
    fr.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False) 
    fr.update_layout(xaxis_title='Current Clamp (nA)', yaxis_title='Firing Frequency (Hz)',showlegend=False)
    pio.write_image(fr,"fi.png",format='png',scale=10,width=640,height=460, validate=True)
    # fr.show()

    # inset
    dfsub = dfss[['amp', 'cellnum', 'Vrmp', 'scnt', 'hzz']].copy()
    dfins = dfsub.loc[dfsub['amp']<=0.1]

    font = 17
    f = px.line(dfins, x='amp', y='hzz',color=dfins['cellnum'].astype(str), color_discrete_sequence= px.colors.qualitative.Set3, line_dash = dfins['cellnum'], symbol = dfins['cellnum'],markers=True,template="simple_white")
    f.update_traces(line = dict(width=2), marker=dict(size=font/1.8,line = dict(width=1,color='indigo')))
    f.update_layout(width=1000,height=800,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font),coloraxis_showscale=False) 
    f.update_layout(xaxis_title='Current Clamp (nA)', yaxis_title='Firing Frequency (Hz)',showlegend=False)
    pio.write_image(f,"fi_inset.png",format='png',scale=10,width=640,height=460, validate=True)
    # f.show()
    return

#Classification of responses
# @author: sgupta 
def classification(df):
    stim = data[list(data)[0]]['net']['params']['stimSourceParams']['iclamp']
    stimend = stim['dur'] + stim['delay']
    dc=df[['amp','cellnum','spkt']].copy()
    dc['Vlist'] = df.V_soma.apply(lambda x: x['cell_0'])
    dc['Vrmp'] = dc.Vlist.apply(lambda x: x[0])
    dc['spkend'] = df.spkt.apply(lambda x: x[len(x)-1] if len(x)>0 else -1)
    dc['scnt'] = df.spkt.apply(len)

    #computing no. of times Vm crosses resting membrane potential
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

    #computing no. of times Vm crosses a set subthreshold value
    ct = []
    for indx in dc.index:
        y = dc['Vlist'][indx]
        z = 0
        for i in range(0,len(y)-1):
            if ((y[i] >= -40 and y[i + 1] < -40) or (y[i] <= -40 and y[i + 1] > -40)):
                z = z+1
        ct.append(z)
        del y

    dc['subthrCross'] = ct
    del ct,z

    temp = dc
    isi = []

    # computing inter-spike interval
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

    col_names = dc.columns.values.tolist()
    print(col_names)
    df_shape = dc.shape
    print("Number of rows: ", df_shape[0])
    print("Number of columns: ", df_shape[1])

    init = max([x if x<=2*stimend/3 else 0 for x in df['t'][0]])
    end = max([x if x<=stimend else 0 for x in df['t'][0]])

    #Classification

    dc['Subthreshold'] = dc.scnt.apply(lambda x: 1 if x<1 else np.nan)
    dc['Phasic'] = dc.scnt.apply(lambda x: 1 if 0<x<=1 else np.nan)
    dc['Burst'] = dc[['spkend','scnt','subthrCross']].apply(lambda x: 1 if ((x.spkend<=(stim['delay']+((stimend+5)/4))) and (1<x.scnt<=4) and (x.scnt == x.subthrCross/2)) else np.nan, axis=1)
    dc['Tonic'] = dc.spkt.apply(lambda x: 1 if len(x)>4 and stim['delay']<=x[-1]<=stimend+5 else np.nan) 
    dc['na'] = df['ina'] 
    dc['t'] = df['t']


    # Added by mmgee
    dc = dc.sort_values(['cellnum', 'amp'], ascending=[True, True])
    dc = dc[dc['amp']>= 0.1]
    dc.to_json('classification.json') 

    return

def fphi(df):
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
    # pio.write_image(fr,"phi_f.png",format='png',scale=3,width=1300,height=700, validate=True)
    fr.show()

    #3D plot
    # font = 16
    # f = px.scatter_3d(dfss, x='phi', y='amp', z='hzz',color='hzz',color_continuous_scale='plasma', labels={'phi':'Fractional Amplitude of I<sub>Kcnc1</sub>','hzz':'Firing Frequency (Hz)', 'amp':'Current Clamp (nA)'},template="simple_white")
    # f.update_traces(marker=dict(size=font/1.5,line = dict(color='black',width=2)))
    # f.update_layout(width=1200,height=1000,uniformtext_minsize=font,uniformtext_mode='show',font=dict(size=font))
    # pio.write_image(f,"3Dffphii.png",format='png',scale=3,width=1300,height=700, validate=True)
    # f.show()
    return


# Figure 4 classification analysis
filename = '//lustre//ogunnaike//users//2420//matlab_example//ragp//classification//22aug25b_allData.json'
readAllData(filename,dfonly = True)
classification(df)

# Figure 5 plotting (firing frequency-current curve)
fI(df)

# Supplementary figure in Github
# readAllData('22aug25c_allData.json')
fphi(df)



