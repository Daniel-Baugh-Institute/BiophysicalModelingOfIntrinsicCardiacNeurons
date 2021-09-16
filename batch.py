import sys, os
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.1, 0.6]	#[0.6, 1.0]
        params['cellnum'] = [0,1,2,6,7,9,11,14,18,19,22,24,25,27,30,35,38,47,52,54,55,56,58,59,60,64,70,72,75,77,79,83,85,94,98] #[x for x in range(101)]
        params['km'] = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006] 
        params['ka'] = [0, 0.11, 0.13, 0.15, 0.17, 0.19,0.2, 0.25] 

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21sep16a' 
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
