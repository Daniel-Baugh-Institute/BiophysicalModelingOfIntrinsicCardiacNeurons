"""
analysis.py

Functions to read and plot figures from the batch simulation results.
"""

import json
import pandas as pd
#import seaborn as sb
import matplotlib.pyplot as plt
import pickle
import numpy as np
from pylab import *
from itertools import product
from pprint import pprint
from netpyne import specs
from collections import OrderedDict



#--------------------------------------------------------------------
# Function to read batch data
#--------------------------------------------------------------------
def readBatchData(dataFolder, batchLabel, loadAll=False, saveAll=True, vars=None, maxCombs=None, listCombs=None):
    # load from previously saved file with all data
    if loadAll:
        print('\nLoading single file with all data...')
        filename = '%s/%s/%s_allData.json' % (dataFolder, batchLabel, batchLabel)
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

#--------------------------------------------------------------------
# Function to convert data to Pandas
#--------------------------------------------------------------------
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

#--------------------------------------------------------------------
# Function to colors and style of figures
#--------------------------------------------------------------------
def setPlotFormat(numColors=8):
    plt.style.use('seaborn-whitegrid')

    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 'large'

    NUM_COLORS = numColors
    colormap = plt.get_cmap('nipy_spectral')
    colorlist = [colormap(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]

    plt.rc('axes', prop_cycle=(cycler('color', colorlist)))

def analysisMeasures(dataFolder, batchLabel, params, data):
    df = toPandas(params, data)
    spktime = dict(zip(df.simLabel,df.spkt))
    spkcount = {i:len(spktime[i]) for i in spktime.keys()}
    firstspk = {}
    datadict = {}
    rmpdict_em = {}
    rmpdict_mb = {}
    for i in spktime.keys():
        if spktime[i]==[]:
            firstspk[i] = 0
        else:
            firstspk[i] = spktime[i][0]

    for i in range(len(tuple(df.simLabel))):
        datadict[df.simLabel[i]]={'V_soma':df.V_soma[i],'t':df.t[i], 'spikeRate':df.avgRate[i], 'spikeTime':df.spkt[i],'spikeCount':spkcount[df.simLabel[i]],'timeFirstSpike':firstspk[df.simLabel[i]]}
        
    temp = pd.DataFrame.from_dict(datadict)
    tempstr = pd.DataFrame.to_json(temp)
    spkfile = '%s/%s_spkStats.json' % (dataFolder,batchLabel)
    with open(spkfile,'w') as f:
        f.write(tempstr)
        f.close()

    jsondict = json.load(open(spkfile))

    # RMP calculation
    for i in range(len(tuple(df.simLabel))):
        l = len(jsondict[df.simLabel[i]]['V_soma']['cell_0'])
        if l%2 ==0:
            mid = int(l/2)
        else: 
            mid = int((l-1)/2)
        rmpdict_em[df.simLabel[i]] = jsondict[df.simLabel[i]]['V_soma']['cell_0'][-1]-jsondict[df.simLabel[i]]['V_soma']['cell_0'][mid] #em: end-mid
        rmpdict_mb[df.simLabel[i]] = jsondict[df.simLabel[i]]['V_soma']['cell_0'][mid]-jsondict[df.simLabel[i]]['V_soma']['cell_0'][0] #mb: mid-beg
    # print(rmpdict.items())
    cid_em,rv_em = zip(*rmpdict_em.items())
    cid_mb,rv_mb = zip(*rmpdict_mb.items())
    # import IPython; IPython.embed()
    return cid_em, rv_em, cid_mb,rv_mb

def readPlot():
    dataFolder = 'data' #'amp_data' #'tauWeight_data'
    batchLabel = '21june18a' #'amp' #'tauWeight'

    params, data = readBatchData(dataFolder, batchLabel, loadAll=0, saveAll=1, vars=None, maxCombs=None)
    cellid_em, rmpv_em, cellid_mb, rmpv_mb  = analysisMeasures(dataFolder, batchLabel, params, data)

    fig, axs = plt.subplots(2,1,sharex = True, sharey = False)
    fig.suptitle("RMP")
    axs[0].scatter(cellid_em, rmpv_em)
    axs[0].set_ylabel('v[5ms]-v[mid ms]')
    axs[0].set_title('Scatter plot')
    axs[1].plot(cellid_mb, rmpv_mb,'.')
    axs[1].set_ylabel('v[mid ms]-v[0]')
    axs[1].set_xlabel('Cell ID')
    axs[1].set_title('Plot with .')
    plt.show()
    return


if __name__ == '__main__':
    readPlot()
