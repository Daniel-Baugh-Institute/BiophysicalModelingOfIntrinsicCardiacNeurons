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


#run analysis.py --> generates simAllData which contains t, v, spikeRate, spikeTime, spikeCount, timeFirstSpike accessible by 'dataLoad'
# dataLoad: collections.OrderedDict
filename = '/Users/jessicafeldman/Desktop/ragp/ragp/simAllData.json'
with open(filename, 'r') as fileObj:
            dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)







