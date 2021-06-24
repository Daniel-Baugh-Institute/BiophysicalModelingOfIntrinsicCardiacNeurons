import pandas as pd
import pickle as pkl
import json
import matplotlib.pyplot as plt

filenamepkl =  '%s/%s_spkStats.pkl' % (dataFolder, batchLabel) 
def ldSpikeStats_pkl(f): return pd.read_pickle(f)

def ldSpikeStats_json(f): return pd.read_json(f)

def plotSpikeStats(df1):
    # spikcount

    # time of first spike

    # hz should == avgRate as spkcount/dur
    plt.scatter(df1.hz, df1.avgRate)

    # instantaneous firing rate - plots hz / time as timeseries
    plt.plot(df1.ifr) 