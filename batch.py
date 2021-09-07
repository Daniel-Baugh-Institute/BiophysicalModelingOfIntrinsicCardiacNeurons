import sys, os
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.6, 1.0]                                   
        params['cellnum'] = [x for x in range(101)]
        params['hcn1'] = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1]
        params['hcn2'] = [0.000009, 0.00009, 0.0009, 0.009, 0.09, 0.9]
        params['hcn3'] = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1]
        params['hcn4'] = [0.000002, 0.00002, 0.0002, 0.002, 0.02, 0.2]

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21sep07a' 
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
