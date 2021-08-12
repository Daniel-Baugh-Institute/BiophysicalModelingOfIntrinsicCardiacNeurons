import sys, os
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.6, 1.0] #, 1.5]                                    
        params['cellnum'] = [x for x in range(115)]
        params['gkcna'] = [0.015, 0.03, 0.05, 0.1, 0.3, 0.5]
        params['gkcnc'] = [0.015, 0.03, 0.05, 0.1, 0.3, 0.5]
        
        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21aug12a' 
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
