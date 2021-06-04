from netpyne import sim
import json
import pandas as pd 
import numpy as np 

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
print("Finished sim.") 


def analyse(): 
    jfile = json.load(open(cfg.filename+'.json'))
    datafile = jfile['simData']
    idx = [cfg.cellnum]
    subset = {'Rate':datafile['avgRate'],'ttfs':datafile['spkt'][0]}
    df = pd.DataFrame.from_dict(subset,orient = 'index',columns=idx)
    print(df)
analyse()

# df.describe()


