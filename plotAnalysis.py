import pandas as pd
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt

batchLabel = '21june21b'
dataFolder = 'data'
f =  '%s/%s_spkStats.pkl' % (dataFolder, batchLabel) 
def ldSpikeStats_pkl(f): 
    df = pd.read_pickle(f)
    return df

def ldSpikeStats_json(f): return pd.read_json(f)

def plotSpikeStats(df1):
    # spikcount

    # time of first spike

    # hz should == avgRate as spkcount/dur
    plt.scatter(df1.hz, df1.avgRate)

    # instantaneous firing rate - plots hz / time as timeseries
    plt.plot(df1.ifr) 






    #spk1
plt.figure()
plt.scatter(np.linspace(1,345, 345), dfss.spk1)
plt.title('time of 1st spike_' + batchLabel)
plt.xlabel('amp_cellnum')
plt.ylabel('t(ms)')
plt.savefig('spk1_'+ batchLabel +'.png')
plt.show()

#spkcounts
plt.figure()
plt.scatter(np.linspace(1,345, 345), dfss.scnt)
plt.title('spikecount_' + batchLabel)
plt.xlabel('amp_cellnum')
plt.ylabel('# spikes')
plt.savefig('scnt_'+ batchLabel +'.png')
plt.show()

# rate 
plt.figure()
plt.scatter(np.linspace(1,345, 345), dfss.hz)
plt.title('spike freq (rate)_' + batchLabel)
plt.xlabel('amp_cellnum')
plt.ylabel('Hz')
plt.savefig('rate_hz'+ batchLabel +'.png')
plt.show()

# f1
plt.figure()
plt.scatter(np.linspace(1,345, 345), dfss.f1)
plt.title('f1_' + batchLabel)
plt.xlabel('amp_cellnum')
plt.ylabel('Hz')
plt.savefig('f1'+ batchLabel +'.png')
plt.show()

plt.figure()
plt.scatter(np.linspace(1,345, 345), dfss.f2)
plt.title('f2_' + batchLabel)
plt.xlabel('amp_cellnum')
plt.ylabel('Hz')
plt.savefig('f2'+ batchLabel +'.png')
plt.show()