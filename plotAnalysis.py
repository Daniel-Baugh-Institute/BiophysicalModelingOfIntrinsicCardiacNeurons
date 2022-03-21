import pandas as pd
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt

batchLabel = '21june25_A'
dataFolder = 'data'
f =  '%s/%s_spkStats.pkl' % (dataFolder, batchLabel) 
def ldSpikeStats_pkl(f): 
    df = pd.read_pickle(f)
    return df

def ldSpikeStats_json(f): return pd.read_json(f)

def plotSpikeStats(df1):
   
df.loc[row_indexer,column_indexer]

# time of first spike
# spike count
# rate
ø

# identifying depol blockade 





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
plt.show()[]

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




##################################################################
# IN PROGRESS - MAY MOVE TO DIFF SCRIPT 
##################################################################
# identifying class of cells that return 1st spike time -1. Appear as APs but DO NOT REACH THRESHOLD. NOT A SPIKE.
for i in dfss.spk1: 
    if dfss.spk1[i] == -1:
        print(['amp=' + str(dfss.amp[i])]) # i=8 0_8, 0_13, 0_19, 0_28, 0_31, 0_35, 0_37, 0_38, 0_41, 0_46, 0_54, 0_56, 0_59, 0_61, 0_69, 0_83, 0_85, 0_87, 0_90,0_97, 0_103, 
        print(['cellnum=' + str(dfss.cellnum[i])])