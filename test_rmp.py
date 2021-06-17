#purpose: to show rmp. Creates scatter plot w/ one point for the rmp for each of 115 cellnums
#load json file to extract v and time
#(y1-y0)/(x1-x0)

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from itertools import product
from netpyne import specs
from collections import OrderedDict
from pprint import pprint
#import seaborn as sb <<< deprecated 
from analysis.py import toPandas


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
    #df['V_soma'][0] #output is OrderedDict([('cell_0',[-61.0,etc....])]) - voltages


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
# get rmp and save --- 
#--------------------------------------------------------------------
    #df = pd.DataFrame(rows, columns=cols)
    #df['simLabel'] = list(data.keys())
    #df['V_soma'][0] #output is OrderedDict([('cell_0',[-61.0,etc....])]) - voltages
def get_rmp()
    # df = pd.DataFrame(rows, columns=col
    # df['simLabel'] = list(data.keys())
    # df.keys>>>> index(['amp', 'cellnum', 'V_soma', 'avgRate', 'spkid', 'spkt', 't','simLabel'],dtype='object')
    for i in list(df.simLabel):
        temp_str = df.simLabel[i]
        delta_t = cfg.recordStep #0.1 ms
        v0 = df['V_soma'][i]
        v1 = df['V_soma'][i+1]


        

# Main code
if __name__ == '__main__':
    get_rmp()




