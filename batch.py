import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        # params['amp'] = [0.6] # indexed
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]
        # params['phi']=[0.1,0.2,0.4] # indexed
        # params['kc'] = [0.011, 0.015, 0.03, 0.05, 0.08, 0.1]
        # params['kj'] = [0.001,0.003,0.005,0.007,0.009]
        params['c1i'] = [0.05,0.03,0.01,0.007,0.005,0.001,0.0008,0.0005]


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22mar30e'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
