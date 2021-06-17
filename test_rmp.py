#purpose: to extract set rmp value for all cellnums and create plot showing rmp for each cellnum
#load json file to extract v (seg.v) = RMP
# or (delta y)/(delta x), where y is voltage and x is time. Expect to yield 0 if steady state achieved
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
# get rmp and save 
#--------------------------------------------------------------------
# First check if steady state 
# diff(v)
# plot diff(v)


#df['V_soma'][0] #output is OrderedDict([('cell_0',[-61.0,etc....])]) - voltages
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
        v0 = df['V_soma'][i+1]
        v1 = df['V_soma'][i+2]
        delta_v = v1 - v0
        if delta_v != 0:
            #not at ss
            rmp[i] = []
        else:
            rmp[i] = v1
        
