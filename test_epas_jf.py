#--------------------------------------------------------------------
# get epas and display for all cellnums. demonstrate steady state.
#--------------------------------------------------------------------
# load '_allData.json' Has {'params': params, 'data': data} for all cells. A single file with all data

import json
import matplotlib.pyplot as plt
from collections import OrderedDict

batchLabel = '21june25_B'; dataFolder = 'data' 
filename = '%s/%s_allData.json' % (dataFolder, batchLabel) 
with open(filename, 'r') as fileObj:
    output = json.load(fileObj, object_pairs_hook=OrderedDict) #odict_keys(['params', 'data'])
data = output['data']                                           #data[list(data.keys())[0]]
cellnums = output['params'][1]['values']                       #list of cellnums 0,114
epas = {} # initialize new var. Note that epas does not change per cellnum so can just use 114
pos_epas = {}
in_range = {}
above_range = {}
below_range = {}
i=0
j=0
k=0
l=0
for c in list(cellnums): 
    epas[c] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] # get 2nd val as 1st is preset in 'pas'
    if data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] > 0:
        print('>0')
        pos_epas[i] = cellnums[c]
        i=i+1
    else:
        if data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] > -100:
            print('< -100')
            below_range[l] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] > -100
            l=l+1
        else:  #<=-100
            print('in range')
            if data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] >= -70: #btwn -70 and -100
                in_range[j] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1]
                j=j+1
            if data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] < -70: # btwn -70 and 0
                print('btwn 0 and -70')
                above_range[k] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1]
                k=k+1
#for c in range (0, len(data.keys())):
#    epas[c] = data[list(data.keys())[c]]['simData']['epas']['cell_0'][1] # get 2nd val as 1st is preset in 'pas'
    
# PLOT FIGURE
plt.figure() # epas values for all cellnums
plt.scatter(list(epas),list(epas.values()))
plt.xlabel('cellnum'); plt.ylabel('mV')
plt.title('e_pas: ' + batchLabel)
plt.savefig(batchLabel+'_epas'+'.png')
plt.show()