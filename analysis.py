"""
analysis.py: Functions to read and interpret figures from the batch simulation results.
"""
import json
import pickle
import pandas as pd
import numpy as np
from collections import OrderedDict
from itertools import product
df = dfss = filenamepkl = None

def readAllData(filename):
    global params, data, df
    with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
    params, data, df = dataLoad['params'], dataLoad['data'], toPandas(dataLoad['params'], dataLoad['data'])

# readBatchData(dataFolder, batchLabel, loadAll=True, saveAll=True, vars=None, maxCombs=None, listCombs=None)
def readBatchData(dataFolder, batchLabel, loadAll=False, saveAll=True, vars=None, maxCombs=None, listCombs=None):
    # load from previously saved file with all data
    if loadAll:
        print('\nLoading single file with all data...')
        filename = '%s/%s_allData.json' % (dataFolder, batchLabel)
        with open(filename, 'r') as fileObj:
            dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
        params = dataLoad['params']
        data = dataLoad['data']
        return params, data

    if isinstance(listCombs, str):
        filename = str(listCombs)
        with open(filename, 'r') as fileObj:
            dataLoad = json.load(fileObj)
        listCombs = dataLoad['paramsMatch']

    # read the batch file and cfg
    batchFile = '%s/%s_batch.json' % (dataFolder, batchLabel)
    with open(batchFile, 'r') as fileObj:
        b = json.load(fileObj)['batch']

    # read params labels and ranges
    params = b['params']

    # reorder so grouped params come first
    preorder = [p for p in params if 'group' in p and p['group']]
    for p in params:
        if p not in preorder: preorder.append(p)
    params = preorder

    # read vars from all files - store in dict
    if b['method'] == 'grid':
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
                outFile = b['saveFolder']+'/'+simLabel+'.json'
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

        # save
        if saveAll:
            print('Saving to single file with all data')
            filename = '%s/%s_allData.json' % (dataFolder, batchLabel)
            dataSave = {'params': params, 'data': data}
            with open(filename, 'w') as fileObj:
                json.dump(dataSave, fileObj)

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
    #print(colRename)
    df.columns = colRename

    return df

# spikeStats(), save, load
''' example usage:
df1 = spikeStats() # assuming df has been read
plt.scatter(df1.hz, df1.avgRate) # a scatter plot
df1.scnt.describe() # stats on the stats eg: count 460.000000 mean 1.886957 std 4.674625 min 0.000000 25% 1.000000 50% 1.000000 75% 1.000000 max 27.000000
'''

def spikeStats(df=df): 
    # syntax example: dfss.spk1, dfss.f1
    dfss=df[['amp', 'cellnum', 'avgRate']].copy()  # note double brackets
    dfss.scnt = df.spkt.apply(len) # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss['spk1'] = df.spkt.apply(lambda x: x[0] if len(x)>0 else -1) # spk1; time of first spike
    dfss['f1']   = df.spkt.apply(lambda x: 1e3/(x[1] - x[0]) if len(x)>1 else 0) # f1: freq for 1st ISI
    dfss['f2']   = df.spkt.apply(lambda x: 1e3/(x[2] - x[1]) if len(x)>2 else 0) # f2: freq for 2nd ISI
    dfss['sdur'] = df.spkt.apply(lambda x: x[-1] - x[0] if len(x)>1 else 0) # sdur: duration of spiking
    dfss['hz']   = dfss.scnt.div(dfss.sdur).mul(1e3).replace(np.inf, 0) # hz: freq calculated as cnt/duration of spiking. Compare w/ avgRate. why are these diff?
    #dfss['fend'] = df.spkt.apply(lambda x: 1e3/(x[len(x)] - x[len(x)-1]) if len(x)>3 else 0) # fend: freq for last ISI
    #dfss['fend0'] = df.spkt.apply(lambda x: 1e3/(x[len(x-1)] - x[len(x)-2]) if len(x)>4 else 0) # fend-1: freq for 2nd tp last ISI
    #dfss['sfa'] = (statistics.mean(f_last))/(statistics.mean(f_first)) #spike freq adaptation ration = (mean(fend, fend-1))/((mean (f1, f2)) Suter et al.
    return dfss
    
def svSpikeStats(dataFolder, batchLabel, dfss=dfss):
    filenamejson = '%s/%s_spkStats.json' % (dataFolder, batchLabel)   
    filenamepkl =  '%s/%s_spkStats.pkl' % (dataFolder, batchLabel)   
    dfss.to_pickle(filenamepkl)
    dfss.to_json(filenamejson)

def ldSpikeStats(f=filenamepkl): return pd.read_pickle(f) 
