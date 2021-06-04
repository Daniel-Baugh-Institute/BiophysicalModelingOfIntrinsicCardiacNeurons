from netpyne import sim
import json
import pandas as pd 
import numpy as np 

print("analysing") 


def analyse(): 
    jfile = json.load(open(cfg.filename+'.json'))
    datafile = jfile['simData']
    idx = [cfg.cellnum]
    subset = {'Rate':datafile['avgRate'],'ttfs':datafile['spkt'][0]}
    df = pd.DataFrame.from_dict(subset,orient = 'index',columns=idx)
    df.to_csv('test.csv',mode = 'a')
    print(df.describe)
analyse()




