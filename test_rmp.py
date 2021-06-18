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
from analysis import toPandas # imports pd module

#--------------------------------------------------------------------
# get rmp and display for all cellnums
#--------------------------------------------------------------------
# First check if steady state. eg - diff(v), plot diff(v), v = rmp
# load '_allData.json' Has {'params': params, 'data': data} for all cells. A single file with all data
def get_rmp()  
    # NOTE: THIS VERSION DOES NOT USE PANDAS 
    batchLabel = '21june17a'; dataFolder = 'data' 
    filename = '%s/%s_allData.json' % (dataFolder, batchLabel) 
    with open(filename, 'r') as fileObj:
        output = json.load(fileObj, object_pairs_hook=OrderedDict) #odict_keys(['params', 'data'])
    data = output['data']                                           #data[list(data.keys())[0]]
    cellnums = output['params'][1]['values'] #list of cellnums
    rmp = [] # initialize new var
    i = 0 
    for c in list(cellnums):
        print(str(cellnums[c]))
        curr_v = data[list(data.keys())[c]]['simData']['V_soma']['cell_0']
        # check for steady state
        if (curr_v[0] - curr_v[1]) == 0: # at ss
            rmp[i] = curr_v[0]
            i=i+1
        else:
            if (curr_v[0] - curr_v[1]) != 0: # not at ss
                rmp[i] = curr_v[100]
                i = i+1
        plt.figure() # create 1 figure for current cellnum
        x = cfg.recordStep # time step
        plt.Line2D(x, curr_v[1], x+x, curr_v[0]) #  plt.Line2D(curr_v[1]/x, curr_v[0]/x)
        # save plot

def plot_rmp()
# Plot rmp (scatter). Color code or shape to denote at ss v not at ss.
# alt: (y1-y0)/(x1-x0) for each cellnum, so 115 plott (in get_rmp() loop above)

# Main code
if __name__ == '__main__':
    get_rmp()
    plot_rmp()
  
# Pandas:
#dir(pd.DataFrame; df = pd.DataFrame(rows, columns=cols)
#df['simLabel'] = list(data.keys())
#df['V_soma'][0] #output is OrderedDict([('cell_0',[-61.0,etc....])]) - voltages
# df.keys--> index(['amp', 'cellnum', 'V_soma', 'avgRate', 'spkid', 'spkt', 't','simLabel'],dtype='object')
 #   for i in list(df.simLabel):
 #       temp_str = df.simLabel[i]
 #       delta_t = cfg.recordStep #0.1 ms
 #       v0 = df['V_soma'][i+1]
 #       v1 = df['V_soma'][i+2]
 #       delta_v = v1 - v0
 #       if delta_v != 0:
 #           #not at ss
 #           rmp[i] = []
 #       else:
 #           rmp[i] = v1