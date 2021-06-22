"""
analysis.py: Functions 1.) to read data from batch simulations and 2.) to calc. metrics for analysis. 
Saves an output file with all data for each of its 2 functionalities.
NOTE: need to define inputs to readBatchData to use interactively. dataFolder and batchLabel
        are defined in batch.py. C/p values for remaining variables.
"""

import json
import pandas as pd
from collections import OrderedDict
from itertools import product
from netpyne import specs
import matplotlib.pyplot as plt
import numpy as np

# readBatchData(dataFolder, batchLabel, loadAll=False, saveAll=True, vars=None, maxCombs=None, listCombs=None)
def readBatchData(dataFolder, batchLabel, loadAll=True, saveAll=True, vars=None, maxCombs=None, listCombs=None):
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

# spikeStats(dataFolder, batchLabel, params, data)
def spikeStats(dataFolder, batchLabel, params, data):
    df = toPandas(params, data) #GET RID OF toPandas and creation of this df. Construct df for columns = temp.index ()
    datadict = {}   # eliminate creation of datadict -- unnecessary
    spktimes = dict(zip(df.simLabel,df.spkt))
    spkcount = {i:len(spktimes[i]) for i in spktimes.keys()} #spkcount['amp_cellnum']
    firstspk = {} # timeFirstSpike
    avgRate = {} # spikeRate as spkcount/dur
    ifr = {} # instantaneous firing rate (freq) = inverse of ISIs = timeseries of inverse periods btwn successive APs (Neymotin et al)

    # calc firstspk = timeFirstSpike
    for i in spktimes.keys():
        if spktimes[i]==[]:
            firstspk[i] = 0
        else:
            firstspk[i] = spktimes[i][0]
    
    # calc avgRate 
        cfg = specs.SimConfig()
        avgRate = len(spkcount)/cfg.duration
    
    for i in range(len(tuple(df.simLabel))):
        datadict[df.simLabel[i]]={'V_soma':df.V_soma[i],'t':df.t[i], 'avgRate':df.avgRate[i], 'spikeTimes':df.spkt[i],'spikeCount':spkcount[df.simLabel[i]],'timeFirstSpike':firstspk[df.simLabel[i]]} #'IFR':ifr[df.simLabel[i]]}
        # spikeTimes = spktimes. use 'spikeTimes':spktimes[df.simLabel[i]] where  spktimes[df.simLabel[i]] should = df.spkt[i]
    temp = pd.DataFrame.from_dict(datadict) # temp = df we want to construct (with cols = datadict entries = temp.index)
    tempstr = pd.DataFrame.to_json(temp)
    spkfile = '%s/%s_spkStats.json' % (dataFolder, batchLabel)
    with open(spkfile,'w') as f:
        f.write(tempstr)
        f.close()

    ## PLOTS
    #spikecount
    plt.figure()
    plt.scatter(list(np.linspace(1, len(spkcount),len(spkcount))),list(spkcount.values()))
    plt.xlabel('cellnum'); plt.ylabel('num_spikes')
    plt.savefig(batchLabel+'_spkcounts'+'.png')
    plt.show()
    #first spike time
    plt.figure()
    plt.scatter(list(np.linspace(1, len(firstspk),len(firstspk))),list(firstspk.values()))
    plt.xlabel('cellnum'); plt.ylabel('first_spike (ms)')
    plt.savefig(batchLabel+'_firstspk'+'.png')
    plt.show()
    # avgRate (single point per amp_cellnum))
    # freq = instantaneous firing rate (plot over time) (line/trace per cell) 
            # 1 plot per amp_cellnum
            # overlay all amp_cellnums


    ############################################
    # ## additional metrics from Suter 
    # sfa_ratio = {} # spike freq adaptation ratio =(avg last 2 ISIs)/(avg 1st 2 ISIs)
    # rmp = {} # resting membrane potential (mV)
    # iResitance = [} # input resistance (mohm)
    # sag = {} # %
    # rheobase = {} # est rheobase (pA)
    # fIslope = {} # (hz/nA)
    # fILinIdx = {} # fi linearity idx 

    ## AP-related parameters - based on analysis of rmp and dV/dt(Suter et al, Neymotin et al)
    #APwidth = {} # ms
    #dvdtMax = {}   # max dV/dt mV/ms
    #dvdtMin = {}   # min dV/dt mV/ms
    #APslope = {} # abs diff btwn max/min 1st deriv of AP (Neymotin et al)
    #APpeak = {} # AP peak voltage = max depolarization (mV)
    #APthreshold = {} # APthreshold mV
    #APampltiude = {} # threshold to peak (mV)
    #deltaAPwidth = {} # % change in AP width - btwn 1st and 8th APs (Suter et al)
    #APdur = {}   # abs diff at 25 and 50% max. amplitude
    #APshape = {} # avg across allspikes(0.1*APthreshold + 0.15*APdur at 25% max amplitude + 0.25*AP dur at 50% max amplitude +0.25* AP peak)        

    # identifying depol blockade 
    #x = 0
    #i = 0
    #depolBlockcell = {}
   
    #for x in len(spktimes):
    #    tempspikes = {}
    #    strlabel = str(df.simLabel[x])
    #    tempspikes = spktimes[strlabel]
    #    if len(temp_spkt) ==1:
    #        # check if depol blockade
    #        if df.V_soma[x]['cell_0'][501] != df.V_soma[x]['cell_0'][500]:
    #            depolBlockcell[i] = strlabel
    #            i = i+1


        
        
