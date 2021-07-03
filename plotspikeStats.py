
import json
import pickle
import pandas as pd
import numpy as np
from collections import OrderedDict
from itertools import product
import matplotlib.pyplot as plt

batchLabel = '21june28f'
filenamepkl = batchLabel+ '_spkStats.pkl'

dir = '/u/jessica/ragp' #cd dir
df=pd.read_pickle(filenamepkl)

def ldSpikeStats(f=filenamepkl): return pd.read_pickle(f) 


def plt_ss():
    fig, ax = plt.subplots()
    ax.clear()
    for a,c in zip(set(df['amp']), ('b','g','r')): df.loc[df.amp==a].plot.scatter('cellnum', 'hz', color=c, ax=ax)
    plt.savefig(batchLabel + '_hz.png')
    plt.show()


    fig, ax = plt.subplots()
    ax.clear()
    for a,c in zip(set(df['amp']), ('b','g','r')): df.loc[df.amp==a].plot.scatter('cellnum', 'scnt', color=c, ax=ax)
    plt.savefig(batchLabel + '_scnt.png')
    plt.show()


    fig, ax = plt.subplots()
    ax.clear()
    for a,c in zip(set(df['amp']), ('b','g','r')): df.loc[df.amp==a].plot.scatter('cellnum', 'spk1', color=c, ax=ax)
    plt.savefig(batchLabel + '_spk1.png')
    plt.show()



    

