import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        # params['amp'] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5] # indexed
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        # params['phi']=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        # params['sze'] = [16,18,20,23,25,27,30] 
        # params['na'] = [0.1, 1]                 # log
        # params['h1'] =[0.0001, 0.00001]         # log


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22mar28a'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
