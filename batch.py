import sys, os
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.6, 1.0]
        params['cellnum'] = [x for x in range(101)]
        params['ca1a'] = [0.00001, 0.0001, 0.001, 0.01]
        params['ca1b'] = [0.00001, 0.0001, 0.001, 0.01]
        params['ca1c'] = [0.00001, 0.0001, 0.001, 0.01]
        # params['ca1g'] = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1]
        # params['ca1i'] = [0.0000027,0.000027,0.00027,0.0027,0.027,0.27]

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21sep08a' 
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
