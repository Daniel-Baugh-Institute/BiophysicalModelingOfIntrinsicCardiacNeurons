#--------------------------------------------------------------------
# get epas and display for all cellnums. demonstrate steady state.
#--------------------------------------------------------------------
# load '_allData.json' Has {'params': params, 'data': data} for all cells. A single file with all data

import json
import matplotlib.pyplot as plt
from collections import OrderedDict

batchLabel = 'netParams_A'; dataFolder = 'data' 
filename = '%s/%s_allData.json' % (dataFolder, batchLabel) 
with open(filename, 'r') as fileObj:
    output = json.load(fileObj, object_pairs_hook=OrderedDict) #odict_keys(['params', 'data'])
data = output['data']                                           #data[list(data.keys())[0]]
cellnums = output['params'][1]['values'] #list of cellnums
epas = {} # initialize new vars
for c in list(cellnums):
    epas[c] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] # get 2nd val as 1st is preset in 'pas'
    
# PLOT FIGURE
plt.figure() # epas values for all cellnums
plt.scatter(list(epas),list(epas.values()))
plt.xlabel('cellnum'); plt.ylabel('mV')
plt.title('e_pas: ' + batchLabel)
plt.savefig(batchLabel+'_epas'+'.png')
plt.show()