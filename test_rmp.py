"""
test_rmp.py
Functions to read saved voltages to assess if steady state achieved and extract and plot rmp set in init.py (seg.v)

"""
import json
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from itertools import product
from netpyne import specs
from collections import OrderedDict
#from analysis import toPandas # imports pd module

#--------------------------------------------------------------------
# get rmp and display for all cellnums
#--------------------------------------------------------------------
# load '_allData.json' Has {'params': params, 'data': data} for all cells. A single file with all data
def getrmp() 
    batchLabel = '21june18d'
    dataFolder = 'data' 
    filename = '%s/%s_allData.json' % (dataFolder, batchLabel) 
    with open(filename, 'r') as fileObj:
        output = json.load(fileObj, object_pairs_hook=OrderedDict) #odict_keys(['params', 'data'])
    data = output['data']                                           #data[list(data.keys())[0]]
    cellnums = output['params'][1]['values'] #list of cellnums
    rmp = {} # initialize new var
    delta_rmp = {}
    curr_v = {}
    for c in list(cellnums):
        print(str(cellnums[c]))
        curr_v[c] = data[list(data.keys())[c]]['simData']['V_soma']['cell_0']
        # check for steady state
        if (curr_v[c][0] - curr_v[c][1]) == 0: # at ss
            rmp[c] = curr_v[c][1]
            delta_rmp[c] = curr_v[c][0] - curr_v[c][1]
        else:
            print('ERROR! NOT AT SS') 

def plotrmp()
    plt.figure()
    plt.scatter(list(delta_rmp),list(delta_rmp.values()))
    plt.xlabel('cellnum')
    plt.ylabel('mV')
    plt.show()
    plt.savefig(batchLabel+'_delta_rmp'+'.png')

    plt.figure()
    plt.plot(list(delta_rmp), list(rmp.values()))
    plt.xlabel('cellnum')
    plt.ylabel('mV')
    plt.savefig(batchLabel+'_rmp'+'.png')

# Main code
getrmp()
plotrmp()
  