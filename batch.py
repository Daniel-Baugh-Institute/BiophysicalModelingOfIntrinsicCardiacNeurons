import sys, os
import numpy as np
from netpyne import specs 
from neuron import h
import sys, inspect
from netpyne.batch import Batch

print('SOURCE: %s'%(inspect.getsourcefile(Batch)))

def batch():
        params = specs.ODict()
        params['amp'] = [0.3, 0.6, 0.9]	
        params['cellnum'] = [x for x in range(4)] # 101
        # params['rybak'] = [0, 0.01, 0.03, 0.05, 0.07, 0.1, 0.12, 0.15] 
        params['ka'] = [0, 0.02] # , 0.04, 0.06, 0.08, 0.1, 0.12, 0.15] 

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21oct08a' 
        b.saveFolder = b.batchLabel
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
