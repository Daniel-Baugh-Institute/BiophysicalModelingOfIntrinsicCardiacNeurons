
import json
import pickle
import pandas as pd
import numpy as np
from collections import OrderedDict
from itertools import product
import matplotlib.pyplot as plt

batchLabel= '21jul04b'
newdataFolder = 'v_plots'

# df from _allData
filename = '/u/jessica/ragp/ragp/'+batchLabel + '_allData.json'

with open(filename, 'r') as fileObj: dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
params, data, df = dataLoad['params'], dataLoad['data'], toPandas(dataLoad['params'], dataLoad['data'])
  # '/u/jessica/ragp/ragp' 'v_plots'

cellnums = df.cellnum
for c in range(len(cellnums)):
    a= df.amp[c]
    print(str(c))
    if c >114:
        c = c - 115
    print(str(c))
    temp_t= df.t[c]
    temp_V= df.V_soma[c]['cell_0']
    fig=plt.figure()
    plt.plot(temp_t, temp_V)
    plt.savefig('voltage_'+str(a)+'_'+ str(c) +'.png')
    #plt.savefig('/'+newdataFolder+'/'+'voltage_'+str(a)+'_'+ str(c) +'.png')

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