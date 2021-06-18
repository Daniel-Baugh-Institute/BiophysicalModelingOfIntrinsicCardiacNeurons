"""
test_rmp.py
Functions to read saved voltages to assess if steady state achieved and extract and plot rmp set in init.py (seg.v)
"""
import json
import matplotlib.pyplot as plt
from collections import OrderedDict
from analysis import toPandas # imports pd module

#--------------------------------------------------------------------
# get rmp and display for all cellnums. demonstrate steady state.
#--------------------------------------------------------------------
# load '_allData.json' Has {'params': params, 'data': data} for all cells. A single file with all data
batchLabel = '21june18d'; dataFolder = 'data' 
filename = '%s/%s_allData.json' % (dataFolder, batchLabel) 
with open(filename, 'r') as fileObj:
    output = json.load(fileObj, object_pairs_hook=OrderedDict) #odict_keys(['params', 'data'])
data = output['data']                                           #data[list(data.keys())[0]]
cellnums = output['params'][1]['values'] #list of cellnums
rmp = {} # initialize new vars
delta_rmp = {}
curr_v = {}
for c in list(cellnums):
    #print(str(cellnums[c]))
    curr_v[c] = data[list(data.keys())[c]]['simData']['V_soma']['cell_0']
    data[list(data.keys())[c]]['epas']
    # check for steady state
    if (curr_v[c][0] - curr_v[c][1]) == 0: # at ss
        rmp[c] = curr_v[c][1]
        delta_rmp[c] = curr_v[c][0] - curr_v[c][1]
    else:
        print('ERROR! NOT AT SS') 

# PLOT FIGURES
plt.figure() # delta_rmp - should be 0s
plt.scatter(list(delta_rmp),list(delta_rmp.values()))
plt.xlabel('cellnum'); plt.ylabel('mV')
plt.savefig(batchLabel+'_delta_rmp'+'.png')
plt.show()

plt.figure() # rmp in mV
plt.plot(list(delta_rmp), list(rmp.values()))
plt.xlabel('cellnum'); plt.ylabel('mV')
plt.savefig(batchLabel+'_rmp'+'.png')
plt.show()