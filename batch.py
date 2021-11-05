import sys, os, inspect, netpyne, pdb
sys.path.insert(0,'/u/billl/nrniv/netpyne')
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

print('Netpyne batch from ', inspect.getsourcefile(netpyne.batch))

def batch():
    params = specs.ODict()
    params['amp'] = [0.3, 0.6] # indexed
    params['cellnum'] = [x for x in range(3)] # indexed
    params['rybak'] = [0, 0.01]  # , 0.03, 0.05, 0.07, 0.1, 0.12, 0.15] 
    params['ka'] = [0, 0.02, 0.04] # , 0.06, 0.08, 0.1, 0.12, 0.15] 

    b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = '21nov05a'
    b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
    b.method = 'grid'
    b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
    b.run()

batch()
